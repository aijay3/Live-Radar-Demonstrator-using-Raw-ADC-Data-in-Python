# Challenges and Solutions Report: Real-Time Radar Data Processing

## Executive Summary

This report documents the significant challenges encountered while working with Texas Instruments (TI) mmWave radar hardware and software tools, particularly the mmWave Studio GUI and DCA1000EVM data capture card. It details how these challenges were overcome through the development of a custom real-time radar processing solution that bypasses many of the limitations of the TI software stack.

The custom solution provides a more robust, user-friendly interface for radar data capture and visualization, with real-time processing capabilities that were not feasible with the original TI tools. This report highlights the technical hurdles faced, the architectural decisions made to address them, and the resulting improvements in functionality and usability.

## 1. Introduction

### 1.1 Background

Texas Instruments' mmWave radar technology offers powerful capabilities for sensing applications, but working with the hardware presents significant challenges, particularly in the areas of:

- Hardware configuration and setup
- Software compatibility and installation
- Data capture and processing
- Real-time visualization

The original workflow using TI's mmWave Studio and DCA1000EVM tools involved a complex, multi-step process that was prone to errors and offered limited real-time processing capabilities.

### 1.2 Project Objectives

The primary objectives of this project were to:

1. Develop a more reliable and user-friendly interface for radar data capture
2. Enable real-time processing and visualization of radar data
3. Overcome the limitations and challenges of the TI software stack
4. Create a modular, extensible architecture for different radar processing modes

## 2. Challenges with TI Software and Hardware

### 2.1 Hardware Integration and Setup Challenges

#### 2.1.1 Switch Settings and Board Configuration

One of the most significant challenges was understanding and correctly configuring the various switch settings on the radar and data capture boards. The TI documentation provided limited guidance on these settings, and incorrect configurations often resulted in silent failures or cryptic error messages.

**Specific Issues:**
- DIP switch settings on the DCA1000EVM were particularly problematic, with SW2.5 needing to be in "software mode" (CONFIG_VIA_SW) for operation with mmWave Studio
- SOP (Serial Output Programming) switches on the radar EVM had to be set to development mode (SOP0 and SOP1 closed, SOP2 open)
- Power selection switch (SW3) configuration was critical but poorly documented

**Impact:**
Incorrect switch settings frequently resulted in:
- "Timeout Error! System disconnected" messages
- Empty data files despite successful configuration
- Inability to establish communication with the radar

#### 2.1.2 USB and COM Port Detection

The DCA1000EVM relies on multiple USB interfaces for control and configuration, with the host PC needing to recognize several COM ports upon connection.

**Specific Issues:**
- Not all expected COM ports would appear in Windows Device Manager
- FTDI driver compatibility issues with Windows 10
- Inconsistent USB port behavior, especially when using docking stations or hubs

**Impact:**
- Inability to establish communication with the radar
- Intermittent connection losses during operation
- Need for frequent hardware resets

### 2.2 Software and Firmware Challenges

#### 2.2.1 Firmware Version Compatibility

Firmware version mismatches between the radar EVM and mmWave Studio were a persistent issue.

**Specific Issues:**
- Loading incompatible BSS/MSS firmware binaries caused the device to report incorrect versions or fail SPI connection attempts
- FPGA firmware corruption after power interruptions
- Difficulty identifying the correct firmware version for specific hardware variants

**Impact:**
- Failed connections and initialization
- Need for complex firmware flashing procedures using UniFlash
- Time-consuming trial-and-error process to find compatible firmware

#### 2.2.2 Software Installation and Dependencies

mmWave Studio has complex dependencies and installation requirements.

**Specific Issues:**
- Required installation on the primary C:\ drive
- Needed specific versions of MATLAB runtime
- Required Microsoft Visual C++ 2013 Redistributable package
- Path conflicts with multiple versions of dependencies

**Impact:**
- Installation failures
- Runtime errors when launching mmWave Studio
- Missing components causing cryptic error messages

### 2.3 Network and Communication Issues

#### 2.3.1 Ethernet Configuration

The DCA1000EVM streams ADC data over Ethernet using a static IP address, requiring specific network configuration.

**Specific Issues:**
- Need for static IP configuration (192.168.33.30 for PC, 192.168.33.180 for DCA1000EVM)
- Conflicts with existing network configurations
- Issues with network interface selection when multiple adapters were present

**Impact:**
- "Ethernet Cable is disconnected" errors
- Data loss during capture
- Inability to receive radar data

#### 2.3.2 UDP Packet Loss and Sequencing

The DCA1000EVM transmits data via UDP, which is inherently unreliable.

**Specific Issues:**
- Packet loss during high-throughput data capture
- Out-of-sequence packets causing data corruption
- Buffer overflows with default packet delay settings

**Impact:**
- Incomplete or corrupted data files
- "RECORD_PKT_OUT_OF_SEQ_ERROR_CODE" errors
- Unusable data for processing

### 2.4 Data Capture and Processing Limitations

#### 2.4.1 Real-Time Processing Constraints

mmWave Studio employs a file-based capture architecture that prevents true real-time analysis.

**Specific Issues:**
- Data written to binary files that remain locked until capture completes
- Significant latency between data acquisition and processing
- Hardcoded sleep commands in Lua scripts exacerbating latency

**Impact:**
- Inability to visualize radar data in real-time
- Long wait times between capture and visualization
- Limited interactive analysis capabilities

#### 2.4.2 Empty Data Files and Timeout Errors

A frequent complaint was the generation of empty data files after triggering data capture.

**Specific Issues:**
- Empty "adc_data.bin" files despite normal status indicators
- Timeout errors during data capture
- Inconsistent behavior with identical settings

**Impact:**
- Wasted time on failed captures
- Difficulty diagnosing root causes
- Unreliable data collection process

## 3. Solution Architecture and Design

### 3.1 System Architecture Overview

To overcome the challenges with TI software, a custom solution was developed with a modular, layered architecture:

1. **Hardware Interface Layer**: Direct communication with radar hardware via UART and UDP
2. **Data Acquisition Layer**: Reliable UDP data reception and packet processing
3. **Signal Processing Layer**: Real-time DSP algorithms for radar data processing
4. **Visualization Layer**: Interactive GUI for data display and parameter adjustment

This architecture provides several advantages:
- Bypasses many of the limitations of mmWave Studio
- Enables true real-time processing and visualization
- Offers a more user-friendly interface
- Provides modular components that can be independently developed and tested

### 3.2 Hardware Interface Implementation

#### 3.2.1 Direct UART Communication

Instead of relying on mmWave Studio's complex interface, the solution implements direct UART communication with the radar using Python's serial library.

**Key Components:**
- `SerialConfig` class in `radar_config.py` handles all UART communication
- Commands are sent directly to the radar using simple text-based protocol
- Configuration files are parsed and sent line by line to the radar

**Benefits:**
- Eliminates dependency on mmWave Studio
- Provides more direct control over radar configuration
- Simplifies the initialization process

#### 3.2.2 FPGA Command Interface

A critical innovation was the implementation of direct UDP communication with the DCA1000EVM's FPGA, bypassing the need for TI's proprietary tools.

**Key Components:**
- Custom FPGA command packets defined in `rp_main.py`
- Socket-based communication for configuration and control
- Structured command sequence for initialization and data capture

**Benefits:**
- Direct control over the data capture process
- Elimination of dependency on TI's CLI tools
- More reliable error handling and recovery

### 3.3 Data Acquisition System

#### 3.3.1 Robust UDP Listener

A dedicated UDP listener thread (`UdpListener` class in `rp_real_time_process.py`) was implemented to handle the reception of radar data packets.

**Key Features:**
- Timeout-based socket operations to prevent blocking
- Proper error handling for network issues
- Frame assembly from multiple UDP packets
- Queue-based data passing to processing threads

**Benefits:**
- Resilience to network interruptions
- Better handling of packet loss
- Efficient data transfer to processing components

#### 3.3.2 Data Processing Pipeline

The data processing pipeline (`DataProcessor` class) implements a multi-stage approach to radar signal processing.

**Key Components:**
- Thread-based processing for non-blocking operation
- Configurable processing parameters (window type, padding, etc.)
- CFAR detection for object identification
- Clutter removal capabilities

**Benefits:**
- Real-time processing of radar data
- Configurable processing parameters
- Improved signal quality through advanced processing techniques

### 3.4 Visualization and User Interface

#### 3.4.1 Modular Application Structure

The solution implements a modular application structure with separate visualization modes:

- Range Profile: 1D radar processing for distance detection
- Range Doppler: 2D processing for distance and velocity
- Range Angle: 2D processing for distance and angle

**Key Components:**
- Launcher application (`launcher.py`) for selecting visualization modes
- Dedicated application modules for each mode
- Shared core components for radar configuration and data processing

**Benefits:**
- Focused interfaces for specific visualization needs
- Simplified user experience
- Code reuse across visualization modes

#### 3.4.2 Interactive GUI

Each visualization mode provides an interactive GUI with real-time parameter adjustment.

**Key Features:**
- Real-time visualization of radar data
- Interactive parameter adjustment (window type, padding, etc.)
- CFAR parameter configuration
- Channel selection and display options

**Benefits:**
- Immediate feedback on parameter changes
- Better understanding of radar data
- More efficient parameter tuning

## 4. Overcoming Specific Challenges

### 4.1 Solving Hardware Configuration Issues

#### 4.1.1 Eliminating Switch Setting Dependencies

The custom solution significantly reduces dependency on correct switch settings by:

1. Implementing more robust error detection and reporting
2. Providing clear error messages that indicate potential switch setting issues
3. Attempting automatic recovery from common configuration errors

**Implementation Details:**
- Error detection in FPGA communication
- Retry mechanisms for failed connections
- Detailed logging of communication attempts

#### 4.1.2 COM Port Management

The solution improves COM port handling through:

1. Automatic detection of available COM ports
2. User-friendly port selection in the GUI
3. Graceful handling of connection failures

**Implementation Details:**
- `get_available_com_ports()` function for dynamic port detection
- Clear error reporting for connection issues
- Automatic retry mechanisms

### 4.2 Addressing Software and Firmware Challenges

#### 4.2.1 Eliminating Dependency on mmWave Studio

The solution completely eliminates dependency on mmWave Studio by:

1. Implementing direct communication with the radar hardware
2. Parsing and sending configuration files directly
3. Handling all data capture and processing within the application

**Implementation Details:**
- Direct UART communication for radar configuration
- Custom UDP communication for data capture
- Integrated processing pipeline

#### 4.2.2 Simplified Configuration Management

Configuration management is simplified through:

1. Direct parsing of standard TI configuration files
2. Extraction of key parameters for processing
3. Calculation of derived parameters for visualization

**Implementation Details:**
- `RadarParameters` class for configuration parsing and parameter calculation
- User-friendly configuration file selection
- Display of calculated parameters for verification

### 4.3 Resolving Network and Communication Issues

#### 4.3.1 Robust UDP Communication

The solution implements robust UDP communication through:

1. Timeout-based socket operations
2. Proper error handling for network issues
3. Frame assembly with sequence checking

**Implementation Details:**
- Socket timeout configuration to prevent blocking
- Error recovery mechanisms for network interruptions
- Packet validation and assembly logic

#### 4.3.2 Efficient Data Transfer

Data transfer efficiency is improved through:

1. Queue-based communication between threads
2. Non-blocking operations throughout the pipeline
3. Proper resource management and cleanup

**Implementation Details:**
- Thread-safe queues for data passing
- Timeout-based queue operations
- Graceful thread termination and resource cleanup

### 4.4 Enabling Real-Time Processing

#### 4.4.1 Threaded Processing Architecture

Real-time processing is achieved through a threaded architecture:

1. Dedicated threads for data reception and processing
2. Non-blocking queue-based communication
3. Efficient signal processing algorithms

**Implementation Details:**
- `UdpListener` thread for data reception
- `DataProcessor` thread for signal processing
- Queue-based communication between components

#### 4.4.2 Optimized Signal Processing

Signal processing is optimized through:

1. Use of efficient libraries (NumPy, SciPy, PyFFTW)
2. Caching of intermediate results and plans
3. Parallelized processing where applicable

**Implementation Details:**
- PyFFTW for accelerated FFT operations
- Plan caching for repeated operations
- Thread pool for parallel processing

## 5. FPGA Command Interface Details

### 5.1 FPGA Command Structure

The solution implements a custom FPGA command interface that directly communicates with the DCA1000EVM's FPGA. This approach bypasses the need for TI's proprietary tools and provides more direct control over the data capture process.

#### 5.1.1 Command Packet Format

Each command packet follows a specific format:

```
[Header (2 bytes)] [Command Code (2 bytes)] [Payload Size (2 bytes)] [Payload (variable)] [Footer (2 bytes)]
```

Where:
- Header: Fixed value `0xA55A` (little-endian)
- Command Code: Specific code for the desired operation
- Payload Size: Size of the payload in bytes
- Payload: Command-specific data (if any)
- Footer: Fixed value `0xEEAA` (little-endian)

**Implementation:**
```python
def create_command_packet(command_code: str) -> bytes:
    """Create a command packet for FPGA communication."""
    if command_code == '9':
        return PACKET_HEADER + CMD_CONNECT + PACKET_SIZE_ZERO + PACKET_FOOTER
    elif command_code == 'E':
        return PACKET_HEADER + CMD_GET_VERSION + PACKET_SIZE_ZERO + PACKET_FOOTER
    elif command_code == '3':
        return PACKET_HEADER + CMD_SET_FPGA + PACKET_SIZE_SIX + FPGA_CONFIG_DATA + PACKET_FOOTER
    elif command_code == 'B':
        return PACKET_HEADER + CMD_SET_PACKET + PACKET_SIZE_SIX + PACKET_CONFIG_DATA + PACKET_FOOTER
    elif command_code == '5':
        return PACKET_HEADER + CMD_START + PACKET_SIZE_ZERO + PACKET_FOOTER
    elif command_code == '6':
        return PACKET_HEADER + CMD_STOP + PACKET_SIZE_ZERO + PACKET_FOOTER
    else:
        return b'NULL'
```

#### 5.1.2 Command Codes

The solution defines a comprehensive set of command codes for FPGA communication:

```python
# FPGA Command Codes
CMD_INIT = (0x01).to_bytes(2, byteorder='little', signed=False)
CMD_CONFIG = (0x02).to_bytes(2, byteorder='little', signed=False)
CMD_SET_FPGA = (0x03).to_bytes(2, byteorder='little', signed=False)
CMD_GET_STATUS = (0x04).to_bytes(2, byteorder='little', signed=False)
CMD_START = (0x05).to_bytes(2, byteorder='little', signed=False)
CMD_STOP = (0x06).to_bytes(2, byteorder='little', signed=False)
CMD_RESET = (0x07).to_bytes(2, byteorder='little', signed=False)
CMD_DEBUG = (0x08).to_bytes(2, byteorder='little', signed=False)
CMD_CONNECT = (0x09).to_bytes(2, byteorder='little', signed=False)
CMD_SET_MODE = (0x0A).to_bytes(2, byteorder='little', signed=False)
CMD_SET_PACKET = (0x0B).to_bytes(2, byteorder='little', signed=False)
CMD_GET_CONFIG = (0x0C).to_bytes(2, byteorder='little', signed=False)
CMD_SET_PARAMS = (0x0D).to_bytes(2, byteorder='little', signed=False)
CMD_GET_VERSION = (0x0E).to_bytes(2, byteorder='little', signed=False)
```

### 5.2 FPGA Initialization Sequence

The FPGA initialization process follows a specific sequence of commands to establish communication and configure the data capture process.

#### 5.2.1 Initialization Procedure

The initialization procedure is implemented in the `initialize_fpga()` function:

```python
def initialize_fpga() -> socket.socket:
    """Initialize FPGA with retry mechanism and proper error handling."""
    command_sequence = ['9', 'E', '3', 'B', '5', '6']
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            sock.bind(config_address)
        except OSError as e:
            logger.error(f"Failed to bind socket: {e}")
            try:
                import psutil
                current_pid = os.getpid()
                for proc in psutil.process_iter(['pid', 'name', 'connections']):
                    if proc.info['name'] == 'python.exe' and proc.pid != current_pid:
                        try:
                            connections = proc.connections()
                            for conn in connections:
                                if conn.laddr.port == config_address[1]:
                                    logger.info(f"Terminating process {proc.pid}")
                                    proc.terminate()
                                    proc.wait(timeout=3)
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                
                time.sleep(1)
                sock.bind(config_address)
            except Exception as bind_error:
                logger.error(f"Could not bind socket: {bind_error}")
                raise
        
        for command in command_sequence[:5]:
            sock.sendto(create_command_packet(command), fpga_address)
            try:
                msg, server = sock.recvfrom(2048)
            except socket.timeout:
                logger.warning(f"Timeout waiting for FPGA response on command {command}")
            time.sleep(0.1)
        
        return sock
    
    except Exception as e:
        logger.error(f"Failed to initialize FPGA: {e}")
        if 'sock' in locals():
            sock.close()
        raise
```

#### 5.2.2 Command Sequence Explanation

The initialization sequence consists of the following commands:

1. **Connect (0x09)**: Establishes initial connection with the FPGA
2. **Get Version (0x0E)**: Retrieves the FPGA firmware version
3. **Set FPGA (0x03)**: Configures the FPGA with specific parameters
4. **Set Packet (0x0B)**: Configures the packet format for data transfer
5. **Start (0x05)**: Starts the data capture process

This sequence ensures proper initialization and configuration of the FPGA before data capture begins.

### 5.3 Benefits of Direct FPGA Communication

The direct FPGA communication approach provides several significant benefits:

#### 5.3.1 Improved Reliability

- Eliminates dependency on TI's proprietary tools
- Provides more direct control over the data capture process
- Enables better error handling and recovery

#### 5.3.2 Enhanced Flexibility

- Allows customization of data capture parameters
- Enables integration with custom processing pipeline
- Facilitates real-time data processing and visualization

#### 5.3.3 Simplified Workflow

- Reduces the number of tools and steps required
- Provides a more integrated user experience
- Eliminates many common points of failure

## 6. Results and Benefits

### 6.1 Improved Reliability

The custom solution significantly improves reliability compared to the TI software stack:

- Reduced dependency on correct switch settings
- More robust error handling and recovery
- Simplified configuration and initialization process

### 6.2 Real-Time Processing Capabilities

The solution enables true real-time processing and visualization:

- Immediate visualization of radar data
- Interactive parameter adjustment
- Responsive user interface

### 6.3 Enhanced User Experience

The user experience is significantly enhanced through:

- Intuitive, modern user interface
- Clear visualization of radar data
- Simplified workflow for configuration and operation

### 6.4 Modular, Extensible Architecture

The modular architecture provides a foundation for future enhancements:

- Easy addition of new visualization modes
- Simple integration of new processing algorithms
- Flexible configuration options

## 7. Conclusion

The development of a custom real-time radar processing solution has successfully overcome the significant challenges associated with TI's mmWave radar hardware and software tools. By implementing direct communication with the radar and data capture hardware, a robust data acquisition system, and an efficient processing pipeline, the solution provides a more reliable, user-friendly interface for radar data capture and visualization.

The key innovations include:

1. Direct UART and UDP communication with radar hardware
2. Custom FPGA command interface for data capture control
3. Robust UDP listener for reliable data reception
4. Efficient, threaded processing architecture for real-time operation
5. Interactive, modular visualization interface

These innovations have transformed a complex, error-prone process into a streamlined, reliable workflow that enables real-time radar data processing and visualization. The solution not only overcomes the limitations of the TI software stack but also provides a foundation for future enhancements and extensions.

## 8. Future Work

Potential areas for future enhancement include:

1. Integration of machine learning algorithms for object classification
2. Implementation of additional visualization modes
3. Support for additional radar hardware variants
4. Enhanced data recording and playback capabilities
5. Integration with other sensing modalities for multi-sensor fusion
