"""
Real-time processing module for radar data.
Handles UDP data reception and processing for radar visualization.
"""

import threading as th
import numpy as np
import socket
import dsp
import logging
from typing import List, Tuple, Optional
from queue import Queue, Empty

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
HEADER_SIZE = 10  # Size of UDP packet header in bytes
SOCKET_TIMEOUT = 0.1  # seconds
QUEUE_TIMEOUT = 0.5  # seconds
LOG_INTERVAL = 100  # frames

# Import padding suggestion function from dsp module
from dsp import suggest_padding_size

class UdpListener(th.Thread):
    """Thread class for receiving and processing UDP data streams from radar."""
    
    def __init__(self, name: str, binary_data_queue: Queue, frame_length: int, 
                 data_address: Tuple[str, int], buffer_size: int):
        """
        Initialize UDP listener thread.
        
        Args:
            name: Thread name
            binary_data_queue: Queue to store ADC data from UDP stream
            frame_length: Length of a single frame
            data_address: Tuple of (host IP address, port)
            buffer_size: Socket buffer size
        """
        self._stop_event = th.Event()
        super().__init__(name=name)
        self.binary_data_queue = binary_data_queue
        self.frame_length = frame_length
        self.data_address = data_address
        self.buffer_size = buffer_size
        self.data_socket = None

    def stop(self):
        """Signal the thread to stop and cleanup resources."""
        self._stop_event.set()
        if self.data_socket:
            try:
                self.data_socket.close()
            except Exception as e:
                logger.error(f"Error closing socket: {e}")

    def run(self):
        """Main thread execution loop for receiving UDP data."""
        try:
            # Configure data type for binary conversion
            data_type = np.dtype(np.int16).newbyteorder('<')
            frame_buffer = []
            frame_count = 0
            
            # Initialize socket with error handling
            try:
                self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.data_socket.bind(self.data_address)
                self.data_socket.settimeout(SOCKET_TIMEOUT)
                logger.info("UDP socket created successfully")
                logger.info("Starting data stream reception")
            except socket.error as e:
                logger.error(f"Socket initialization failed: {e}")
                return
            
            # Main reception loop
            while not self._stop_event.is_set():
                try:
                    packet_data, _ = self.data_socket.recvfrom(self.buffer_size)
                    
                    # Validate packet size
                    if len(packet_data) <= HEADER_SIZE:
                        logger.warning(f"Received undersized packet: {len(packet_data)} bytes")
                        continue
                    
                    # Process packet
                    frame_data = packet_data[HEADER_SIZE:]  # Remove header
                    frame_buffer.extend(np.frombuffer(frame_data, dtype=data_type))
                    
                    # Process complete frames
                    while len(frame_buffer) >= self.frame_length:
                        frame_count += 1
                        current_frame = frame_buffer[:self.frame_length]
                        frame_buffer = frame_buffer[self.frame_length:]
                        
                        try:
                            self.binary_data_queue.put(current_frame, timeout=QUEUE_TIMEOUT)
                            if frame_count % LOG_INTERVAL == 0:
                                logger.debug(f"Processed frame {frame_count}")
                        except Queue.Full:
                            logger.warning("Queue full, dropping frame")
                            
                except socket.timeout:
                    continue
                except Exception as e:
                    logger.error(f"Error processing UDP data: {e}")
                    
        except Exception as e:
            logger.error(f"Fatal error in UdpListener: {e}")
        finally:
            if self.data_socket:
                try:
                    self.data_socket.close()
                    logger.info("UDP socket closed")
                except Exception as e:
                    logger.error(f"Error closing socket: {e}")

class DataProcessor(th.Thread):
    """Thread class for processing radar data and generating visualizations."""
    
    def __init__(self, name: str, config: List[int], 
                 binary_queue: Queue, range_doppler_queue: Queue, 
                 range_angle_queue: Queue, range_profile_queue: Queue,
                 selected_channel: int = 0):
        """
        Initialize data processor thread.
        
        Args:
            name: Thread name
            config: Radar configuration [samples, chirps, tx_antennas, rx_antennas]
            binary_queue: Queue for raw binary data
            range_doppler_queue: Queue for Range-Doppler Images
            range_angle_queue: Queue for Range-Angle Images
            range_profile_queue: Queue for Range Profiles
            selected_channel: Index of the selected RX channel (0-3)
        """
        self._stop_event = th.Event()
        super().__init__(name=name)
        
        # Configuration parameters
        self.num_adc_samples = config[0]
        self.num_chirps = config[1]
        self.num_tx_channels = config[2]
        self.num_rx_channels = config[3]
        
        # Data queues
        self.binary_queue = binary_queue
        self.range_doppler_queue = range_doppler_queue
        self.range_angle_queue = range_angle_queue
        self.range_profile_queue = range_profile_queue
        self.selected_channel = selected_channel
        
        # Pre-allocate arrays for efficiency
        self.reshape_size = [-1, 4]
        self.complex_view = slice(0, None, 2)
        
        logger.info(f"Initialized DataProcessor with config: "
                   f"samples={self.num_adc_samples}, "
                   f"chirps={self.num_chirps}, "
                   f"tx={self.num_tx_channels}, "
                   f"rx={self.num_rx_channels}")

    def stop(self):
        """Signal the thread to stop processing."""
        self._stop_event.set()

    def set_channel(self, channel: int):
        """Set the selected channel for range profile calculation."""
        if 0 <= channel < self.num_rx_channels:
            self.selected_channel = channel
            logger.info(f"Selected channel changed to {channel}")
        else:
            logger.error(f"Invalid channel selection: {channel}")

    def _process_frame(self, raw_data: np.ndarray) -> np.ndarray:
        """
        Process a single frame of radar data.
        
        Args:
            raw_data: Raw ADC data
            
        Returns:
            Processed data in format [samples, antennas, chirps]
        """
        try:
            # Reshape for complex conversion
            frame_data = np.reshape(raw_data, self.reshape_size)
            
            # Convert to complex (optimize by avoiding concatenation)
            complex_data = frame_data[:, self.complex_view] + 1j * frame_data[:, 2:]
            
            # Reshape to final format
            reshaped_data = np.reshape(complex_data, [self.num_chirps, -1, self.num_adc_samples])
            final_data = np.transpose(reshaped_data, [2, 1, 0])  # [samples, antennas, chirps]
            
            return final_data
            
        except Exception as e:
            logger.error(f"Error processing frame: {e}")
            raise

    def run(self):
        """Main processing loop."""
        frame_count = 0
        
        while not self._stop_event.is_set():
            try:
                # Get data with timeout
                raw_frame = self.binary_queue.get(timeout=SOCKET_TIMEOUT)
                
                # Process frame
                try:
                    processed_data = self._process_frame(raw_frame)
                    frame_count += 1
                    
                    # Get suggested padding sizes
                    padding = dsp.suggest_padding_size(processed_data.shape)
                    
                    # Generate visualizations with explicit padding sizes
                    # Calculate range profile for all channels
                    range_profile = dsp.calculate_range_profile(processed_data, mode=1, 
                                                              padding_size=padding[0])
                    range_doppler = dsp.calculate_range_doppler(processed_data, mode=1, 
                                                              padding_size=[padding[0], padding[2]])
                    range_angle = dsp.calculate_range_angle(processed_data, mode=1, 
                                                          padding_size=padding)
                    
                    # Queue results with timeout
                    self.range_doppler_queue.put(range_doppler, timeout=QUEUE_TIMEOUT)
                    self.range_angle_queue.put(range_angle, timeout=QUEUE_TIMEOUT)
                    self.range_profile_queue.put(range_profile, timeout=QUEUE_TIMEOUT)
                    
                    if frame_count % LOG_INTERVAL == 0:
                        logger.debug(f"Processed {frame_count} frames")
                        
                except Exception as e:
                    logger.error(f"Error in frame processing: {e}")
                    continue
                    
            except Empty:
                continue  # Queue timeout, check stop condition
            except Exception as e:
                logger.error(f"Error in main processing loop: {e}")
                continue
                
        logger.info(f"DataProcessor stopped after processing {frame_count} frames")
