# Real Time Radar System Architecture Overview

This document provides a high-level overview of the Real Time Radar system architecture, explaining how the hardware and software components interact to capture and process radar data in real-time.

## System Components

![System Architecture](Demo.PNG)

### Hardware Components

1. **XWR1843 EVM (Evaluation Module)**
   - 77 GHz FMCW radar sensor
   - Integrated DSP and MCU for basic processing
   - 4 TX and 4 RX channels for MIMO operation
   - Configurable via serial interface (UART)

2. **DCA1000 EVM (Data Capture Card)**
   - High-speed data capture for raw ADC samples
   - Ethernet interface for data streaming
   - FPGA-based for real-time data handling
   - Connects to XWR1843 via MMWAVEICBOOST adapter

3. **Host Computer**
   - Windows 10 PC with Ethernet and USB ports
   - Runs the Real Time Radar software
   - Performs signal processing and visualization
   - Configures the radar via serial interface

### Software Components

The software is organized into three main applications, each focusing on a different radar processing domain:

1. **Range Profile Application**
   - 1D radar processing (range domain)
   - Detects object distance
   - Displays signal power vs. range

2. **Range Doppler Application**
   - 2D radar processing (range-velocity domain)
   - Detects object distance and velocity
   - Displays range-Doppler heatmap

3. **Range Angle Application**
   - 2D radar processing (range-azimuth domain)
   - Detects object distance and angle
   - Displays range-angle heatmap

Each application shares common components:
- Configuration interface
- Data acquisition module
- Signal processing pipeline
- Visualization interface

## Data Flow

The data flow through the system follows these steps:

1. **Configuration**
   - User selects radar parameters via the application GUI
   - Parameters are sent to XWR1843 via serial interface
   - DCA1000 is configured via Ethernet for data capture

2. **Data Acquisition**
   - XWR1843 transmits FMCW chirps
   - Received signals are sampled by ADCs
   - Raw ADC samples are streamed to DCA1000
   - DCA1000 forwards data to host PC via Ethernet (UDP)

3. **Signal Processing**
   - Raw ADC data is received by UDP listener
   - Data is organized into frames and channels
   - Signal processing is performed based on application type:
     - Range Profile: 1D FFT for range detection
     - Range Doppler: 2D FFT for range and velocity
     - Range Angle: 2D FFT and beamforming for range and angle
   - CFAR detection identifies targets in processed data

4. **Visualization**
   - Processed data is displayed in real-time
   - Different visualization types based on application:
     - Range Profile: 1D plot of signal power vs. range
     - Range Doppler: 2D heatmap of range vs. velocity
     - Range Angle: 2D heatmap of range vs. angle
   - Detected targets are highlighted and listed in data table

## Software Architecture

### Common Components

1. **Launcher (`launcher.py`)**
   - Main entry point for the application suite
   - Provides GUI to select and launch specific applications
   - Manages application lifecycle

2. **Radar Configuration**
   - `radar_config.py`: Serial interface to configure XWR1843
   - `radar_config_params.py`: Configuration parameter definitions
   - `radar_parameters.py`: Radar operational parameters calculation

### Application-Specific Components

Each application (Range Profile, Range Doppler, Range Angle) follows a similar structure:

1. **Main Application Module** (`xx_main.py`)
   - Initializes the application
   - Sets up the GUI
   - Manages the application lifecycle

2. **DSP Module** (`xx_dsp.py`)
   - Implements signal processing algorithms
   - Performs FFT processing
   - Implements CFAR detection
   - Handles clutter removal

3. **Real-Time Processing Module** (`xx_real_time_process.py`)
   - Manages data acquisition via UDP
   - Handles real-time processing pipeline
   - Synchronizes data flow between acquisition and processing

4. **Application Layout Module** (`xx_app_layout.py`)
   - Defines the GUI layout
   - Implements visualization components
   - Handles user interaction

## Signal Processing Pipeline

### Range Profile Processing

1. **Data Organization**
   - Raw ADC data is organized by RX channel and chirp
   - Data is converted from 16-bit integers to complex values

2. **Range Processing**
   - Window function is applied to reduce sidelobes
   - Range FFT is performed on each chirp and channel
   - Optional zero-padding for better range resolution
   - Channels are combined (summed or selected)

3. **Detection**
   - CFAR detection identifies targets in range domain
   - Peak grouping combines nearby detections
   - Range and magnitude of targets are calculated

### Range Doppler Processing

1. **Range Processing**
   - Same as Range Profile processing
   - Results in range-time data cube

2. **Doppler Processing**
   - Second FFT across chirps (slow-time dimension)
   - Results in range-velocity data
   - Static clutter removal (optional)

3. **Detection**
   - 2D CFAR detection in range-Doppler domain
   - Targets identified by range and velocity

### Range Angle Processing

1. **Range Processing**
   - Same as Range Profile processing
   - Results in range data for each channel

2. **Angle Processing**
   - Virtual array formation using MIMO principle
   - Beamforming or FFT-based angle estimation
   - Results in range-angle data

3. **Detection**
   - 2D CFAR detection in range-angle domain
   - Targets identified by range and angle
   - Coordinate transformation to Cartesian space

## Performance Considerations

1. **Real-Time Processing**
   - Multithreaded design for parallel processing
   - Optimized FFT implementation using pyfftw
   - Queue-based data flow for efficient producer-consumer pattern

2. **Memory Management**
   - Efficient buffer management for continuous data flow
   - Pre-allocated arrays to minimize memory allocation overhead
   - Circular buffers for continuous processing

3. **Visualization Performance**
   - OpenGL acceleration for real-time plotting
   - Adaptive update rate based on system performance
   - Efficient data transfer between processing and visualization

## Customization and Extension

The system is designed to be modular and extensible:

1. **Configuration Files**
   - Custom radar configurations can be created
   - Different parameter sets for various scenarios

2. **Processing Parameters**
   - Window functions can be selected
   - Range padding can be adjusted
   - CFAR parameters can be tuned

3. **Visualization Options**
   - Channel selection for detailed analysis
   - Different visualization modes
   - Data table for quantitative analysis

## System Requirements and Limitations

1. **Hardware Requirements**
   - Windows 10 PC with Ethernet and USB ports
   - Sufficient CPU power for real-time processing
   - Adequate memory for data buffers

2. **Performance Limitations**
   - Maximum frame rate depends on processing complexity
   - Range resolution limited by bandwidth
   - Angular resolution limited by array size
   - Velocity resolution limited by chirp count

3. **Known Constraints**
   - Fixed IP address requirement for DCA1000
   - UDP packet loss can occur under heavy network load
   - Processing delay increases with higher resolution settings
