import numpy as np
from typing import Union, Tuple, List, Optional
import logging
from scipy.signal import find_peaks

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pre-compute common windows for typical radar data sizes
_WINDOW_CACHE = {}

def create_window(size: int) -> np.ndarray:
    """
    Create or retrieve a cached Blackman window of specified size.
    
    Args:
        size: Length of the window
        
    Returns:
        Blackman window array of specified size
        
    Example:
        >>> window = create_window(256)  # Creates window for 256-point FFT
        >>> window.shape
        (256,)
    """
    if size not in _WINDOW_CACHE:
        _WINDOW_CACHE[size] = np.blackman(size)
    return _WINDOW_CACHE[size]

def suggest_padding_size(data_shape: tuple, min_range_res: float = 0.1, 
                        min_doppler_res: float = 0.1) -> List[int]:
    """
    Suggest optimal FFT padding sizes based on input dimensions and desired resolution.
    
    If dimensions are already powers of 2, no padding is needed for FFT efficiency.
    Padding is only suggested when:
    1. A dimension is not a power of 2 AND close to the next power of 2
    2. Additional frequency resolution is desired
    
    Args:
        data_shape: Shape of input data [samples, antennas, chirps]
        min_range_res: Minimum desired range resolution in meters
        min_doppler_res: Minimum desired doppler resolution in m/s
        
    Returns:
        List of suggested padding sizes [range_pad, angle_pad, doppler_pad]
        
    Example:
        >>> data = np.random.random((256, 4, 16))  # Example radar data (all powers of 2)
        >>> padding = suggest_padding_size(data.shape)
        >>> print(f"Suggested padding: {padding}")
        Suggested padding: [256, 4, 16]  # No padding needed
    """
    num_samples, num_antennas, num_chirps = data_shape
    
    def is_power_of_2(n: int) -> bool:
        return n > 0 and (n & (n - 1)) == 0
    
    # For range dimension
    if is_power_of_2(num_samples):
        range_padding = num_samples  # Already optimal
    else:
        next_pow2 = 2 ** np.ceil(np.log2(num_samples)).astype(int)
        if next_pow2 - num_samples <= num_samples * 0.1:  # Within 10%
            range_padding = next_pow2
        else:
            # Round up to nearest multiple of 8 for SIMD optimization
            range_padding = ((num_samples + 7) // 8) * 8
    
    # For angle dimension
    if is_power_of_2(num_antennas):
        angle_padding = num_antennas  # Already optimal
    else:
        next_pow2 = 2 ** np.ceil(np.log2(num_antennas)).astype(int)
        if next_pow2 - num_antennas <= num_antennas * 0.1:  # Within 10%
            angle_padding = next_pow2
        else:
            angle_padding = num_antennas  # Keep original size
    
    # For doppler dimension
    if is_power_of_2(num_chirps):
        doppler_padding = num_chirps  # Already optimal
    else:
        next_pow2 = 2 ** np.ceil(np.log2(num_chirps)).astype(int)
        if next_pow2 - num_chirps <= num_chirps * 0.1:  # Within 10%
            doppler_padding = next_pow2
        else:
            doppler_padding = num_chirps  # Keep original size
    
    return [range_padding, angle_padding, doppler_padding]

def validate_input(radar_data: np.ndarray) -> bool:
    """Validate input data shape and type."""
    if not isinstance(radar_data, np.ndarray):
        raise TypeError("Input must be a numpy array")
    if len(radar_data.shape) != 3:
        raise ValueError("Input must be 3D array [samples, antennas, chirps]")
    if not np.issubdtype(radar_data.dtype, np.complexfloating) and not np.issubdtype(radar_data.dtype, np.floating):
        raise ValueError("Input must be floating point or complex type")
    return True

def calculate_range_profile(radar_data: np.ndarray, mode: int = 0, 
                          padding_size: Optional[Union[int, List[int]]] = None) -> Union[np.ndarray, List[np.ndarray]]:
    """
    Compute Range Profile from radar data.
    
    Args:
        radar_data: Input array with shape [samples, antennas, chirps]
        mode: Output format mode (0: raw, 1: abs with fft shift, 2: both)
        padding_size: FFT padding size for better resolution. If None, will be auto-suggested.
        
    Returns:
        Range profile data in specified format
        Shape for mode 0: [padded_samples, antennas, chirps]
        Shape for mode 1: [padded_samples]
        Shape for mode 2: [raw_data, abs_data]
    """
    try:
        validate_input(radar_data)
        
        # Get dimensions
        num_samples = radar_data.shape[0]
        num_rx = radar_data.shape[1]
        num_chirps = radar_data.shape[2]
        
        # Create window
        window = create_window(num_samples)
        
        # Determine FFT size with auto-suggestion
        if padding_size is None:
            fft_size = suggest_padding_size(radar_data.shape)[0]  # Use suggested range padding
        else:
            fft_size = padding_size[0] if isinstance(padding_size, (list, tuple)) else padding_size
        
        # Initialize output array
        range_fft = np.zeros((fft_size, num_rx, num_chirps), dtype=np.complex128)
        
        # Process each receiver and chirp combination separately
        for rx in range(num_rx):
            for chirp in range(num_chirps):
                # Get data for this receiver/chirp combination
                data = radar_data[:, rx, chirp]
                
                # Remove DC component
                data = data - np.mean(data)
                
                # Apply windowing
                windowed_data = data * window
                
                # Perform Range FFT
                range_fft[:, rx, chirp] = np.fft.fft(windowed_data, n=fft_size)
        
        if mode == 0:
            return range_fft
        elif mode == 1:
            # Don't use fftshift for range profile - range should start from zero
            return np.abs(range_fft)
        elif mode == 2:
            magnitude = np.abs(range_fft)
            return [range_fft, magnitude]
        else:
            raise ValueError(f"Invalid mode: {mode}")
            
    except Exception as e:
        logger.error(f"Error in calculate_range_profile: {str(e)}")
        raise

def calculate_range_doppler(radar_data: np.ndarray, mode: int = 0,
                          padding_size: Optional[List[int]] = None) -> Union[np.ndarray, List[np.ndarray]]:
    """
    Compute Range-Doppler Image from radar data.
    
    Args:
        radar_data: Input array with shape [samples, antennas, chirps]
        mode: Output format mode (0: raw, 1: abs with fft shift, 2: both)
        padding_size: List of FFT padding sizes [range_pad, doppler_pad]. If None, will be auto-suggested.
        
    Returns:
        RDI data in specified format
        Shape for mode 0: [padded_samples, antennas, padded_chirps]
        Shape for mode 1: [padded_samples, padded_chirps, antennas]
        Shape for mode 2: [raw_data, abs_data]
    """
    try:
        validate_input(radar_data)
        
        # Get dimensions
        num_samples = radar_data.shape[0]
        num_rx = radar_data.shape[1]
        num_chirps = radar_data.shape[2]
        
        # Create windows
        range_window = create_window(num_samples)
        doppler_window = create_window(num_chirps)
        
        # Get padding sizes with auto-suggestion
        if padding_size is None:
            suggested_padding = suggest_padding_size(radar_data.shape)
            range_padding = suggested_padding[0]
            doppler_padding = suggested_padding[2]  # Use doppler padding from suggestions
        else:
            range_padding = padding_size[0]
            doppler_padding = padding_size[1]
            
        # Initialize output array
        range_doppler_fft = np.zeros((range_padding, num_rx, doppler_padding), dtype=np.complex128)
        
        # First perform range FFT for each receiver/chirp combination
        range_fft = np.zeros((range_padding, num_rx, num_chirps), dtype=np.complex128)
        for rx in range(num_rx):
            for chirp in range(num_chirps):
                # Get data for this receiver/chirp combination
                data = radar_data[:, rx, chirp]
                
                # Remove DC component
                data = data - np.mean(data)
                
                # Apply range windowing
                windowed_data = data * range_window
                
                # Perform Range FFT
                range_fft[:, rx, chirp] = np.fft.fft(windowed_data, n=range_padding)
        
        # Then perform Doppler FFT for each receiver and range bin
        for rx in range(num_rx):
            for range_bin in range(range_padding):
                # Get data for this receiver/range bin combination and reshape to column
                data = range_fft[range_bin, rx, :].reshape(-1)
                
                # Apply doppler windowing
                windowed_data = data * doppler_window
                
                # Perform Doppler FFT with fftshift
                range_doppler_fft[range_bin, rx, :] = np.fft.fftshift(
                    np.fft.fft(windowed_data, n=doppler_padding)
                )
        
        if mode == 0:
            return range_doppler_fft
        elif mode == 1:
            # Convert to magnitude
            magnitude = np.abs(range_doppler_fft)
            
            # Flip range axis to match example orientation
            flipped_magnitude = np.flipud(magnitude)
            
            return flipped_magnitude
        elif mode == 2:
            magnitude = np.abs(range_doppler_fft)
            centered_magnitude = np.fft.fftshift(magnitude, axes=2)
            transposed_magnitude = np.transpose(centered_magnitude, [0, 2, 1])
            flipped_magnitude = np.flip(transposed_magnitude, axis=0)
            return [range_doppler_fft, flipped_magnitude]
        else:
            raise ValueError(f"Invalid mode: {mode}")
            
    except Exception as e:
        logger.error(f"Error in calculate_range_doppler: {str(e)}")
        raise

def calculate_range_angle(radar_data: np.ndarray, mode: int = 0,
                        padding_size: Optional[List[int]] = None) -> Union[np.ndarray, List[np.ndarray]]:
    """
    Compute Range-Angle Image from radar data.
    
    Args:
        radar_data: Input array with shape [samples, antennas, chirps]
        mode: Output format mode (0: raw, 1: abs with fft shift, 2: both)
        padding_size: List of FFT padding sizes [range_pad, angle_pad]. If None, will be auto-suggested.
        
    Returns:
        RAI data in specified format
        Shape for mode 0: [padded_samples, padded_antennas, chirps]
        Shape for mode 1: [padded_samples, padded_antennas, chirps]
        Shape for mode 2: [raw_data, abs_data]
    """
    try:
        validate_input(radar_data)
        
        # Get dimensions
        num_samples = radar_data.shape[0]
        num_rx = radar_data.shape[1]
        num_chirps = radar_data.shape[2]
        
        # Create window for angle FFT
        angle_window = create_window(num_rx)
        
        # Get padding sizes with auto-suggestion
        if padding_size is None:
            padding_size = suggest_padding_size(radar_data.shape)
            
        angle_padding = padding_size[1]
        
        # Initialize output array
        angle_fft = np.zeros((num_samples, angle_padding, num_chirps), dtype=np.complex128)
        
        # Process each range bin and chirp combination separately
        for chirp in range(num_chirps):
            for range_bin in range(num_samples):
                # Get data for this range/chirp combination and reshape to column
                data = radar_data[range_bin, :, chirp].reshape(-1)
                
                # Apply angle windowing
                windowed_data = data * angle_window
                
                # Perform Angle FFT with fftshift
                angle_fft[range_bin, :, chirp] = np.fft.fftshift(
                    np.fft.fft(windowed_data, n=angle_padding)
                )
        
        if mode == 0:
            return angle_fft
        elif mode == 1:
            # Convert to magnitude
            magnitude = np.abs(angle_fft)
            return magnitude
        elif mode == 2:
            magnitude = np.abs(angle_fft)
            return [angle_fft, magnitude]
        else:
            raise ValueError(f"Invalid mode: {mode}")
            
    except Exception as e:
        logger.error(f"Error in calculate_range_angle: {str(e)}")
        raise

def detect_cfar(signal: np.ndarray, num_train: int = 8, num_guard: int = 2,
                pfa: float = 1e-3, min_signal: float = -40) -> Tuple[np.ndarray, np.ndarray]:
    """
    Implements Enhanced Cell Averaging CFAR (CA-CFAR) for target detection.
    Uses vectorized operations and efficient array manipulations for better performance.
    
    Args:
        signal: Input signal to perform CFAR on
        num_train: Number of training cells on each side
        num_guard: Number of guard cells on each side
        pfa: Probability of false alarm (determines threshold factor)
        min_signal: Minimum signal strength in dB to consider for detection
        
    Returns:
        Tuple of (detection_indices, thresholds)
    """
    try:
        if not isinstance(signal, np.ndarray):
            signal = np.array(signal)
            
        if signal.ndim != 1:
            raise ValueError("Signal must be 1-dimensional")
            
        signal_length = len(signal)
        if signal_length < 2 * (num_train + num_guard) + 1:
            raise ValueError("Signal length must be greater than window size")
            
        # Calculate threshold factor based on desired probability of false alarm
        # Reduced factor for better detection of close targets
        threshold_factor = num_train * (pfa ** (-1/num_train) - 1) * 0.25
        
        # Initialize arrays
        detections = np.zeros(signal_length, dtype=bool)
        thresholds = np.zeros(signal_length)
        
        # Create padded signal for edge handling
        padded_signal = np.pad(signal, (num_train + num_guard,), mode='reflect')
        
        # Create sliding windows using stride tricks for better performance
        window_size = num_train * 2 + 2 * num_guard + 1
        shape = (signal_length - 2*(num_train + num_guard), window_size)
        strides = (padded_signal.strides[0], padded_signal.strides[0])
        windows = np.lib.stride_tricks.as_strided(padded_signal, shape=shape, strides=strides)
        
        # Extract training cells using vectorized operations
        left_train = windows[:, :num_train]
        right_train = windows[:, -num_train:]
        train_cells = np.concatenate([left_train, right_train], axis=1)
        
        # Calculate noise levels using vectorized operations
        sorted_cells = np.sort(train_cells, axis=1)
        noise_levels = np.mean(sorted_cells[:, 2:-2], axis=1)  # Trimmed mean
        
        # Calculate adaptive thresholds
        center_indices = slice(num_train + num_guard, signal_length - (num_train + num_guard))
        local_snr = signal[center_indices] / (noise_levels + 1e-10)
        adaptive_threshold = threshold_factor * (1 + 0.1 * np.log10(local_snr + 1))
        thresholds[center_indices] = adaptive_threshold * noise_levels
        
        # Apply detection
        detections[center_indices] = signal[center_indices] > thresholds[center_indices]
        
        # Merge nearby detections
        detection_indices = np.where(detections)[0]
        if len(detection_indices) > 1:
            gaps = np.diff(detection_indices)
            merge_mask = gaps <= 2  # Merge detections within 2 samples
            for i in range(len(merge_mask)):
                if merge_mask[i]:
                    mid_point = detection_indices[i] + gaps[i]//2
                    detections[detection_indices[i]:detection_indices[i+1]+1] = False
                    detections[mid_point] = True
        
        return detections, thresholds
        
    except Exception as e:
        logger.error(f"Error in detect_cfar: {str(e)}")
        raise
