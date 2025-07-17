# Appendix: Real-Time Radar System User Guide

This appendix provides comprehensive documentation for the Real-Time Radar processing system developed in this thesis, including setup instructions, reference information, and system architecture details.

## A.1 Hardware Requirements

### A.1.1 Essential Hardware
- **Texas Instruments XWR1843 EVM** (Evaluation Module)
- **DCA1000 EVM** (Data Capture Card)
- **MMWAVEICBOOST** adapter board (for connecting XWR1843 to DCA1000)
- **Computer** with:
  - Windows 10 operating system
  - Ethernet port (for DCA1000 connection)
  - USB port (for XWR1843 serial configuration)
- **Ethernet cable** (CAT5e or better recommended)
- **USB-A to Micro-USB cable** (for XWR1843 configuration)
- **Power supply** for the radar module (12V DC, 2.5A minimum)

### A.1.2 Software Requirements
- **Python 3.7 or higher** (3.7.9 recommended for best compatibility)
- **Python packages** (installed via requirements.txt):
  - numpy==1.18.5
  - matplotlib==3.2.2
  - PyQt5==5.15.1
  - PyQt5-sip==12.8.1
  - pyqtgraph==0.11.0
  - pyserial==3.4
  - scipy==1.4.1
  - pyfftw==0.13.1
  - psutil==5.9.5

## A.2 Hardware Setup

### A.2.1 Physical Connections

1. **Prepare the hardware components**:
   - Ensure all components are powered off
   - Place the radar module on a stable surface or mount it on a tripod

2. **Connect XWR1843 EVM to DCA1000 EVM**:
   - Attach the MMWAVEICBOOST adapter board to the XWR1843 EVM
   - Connect the MMWAVEICBOOST to the DCA1000 EVM using the provided ribbon cables
   - Ensure all connections are secure and properly aligned

3. **Connect DCA1000 EVM to computer**:
   - Connect one end of the Ethernet cable to the DCA1000 EVM
   - Connect the other end to the Ethernet port on your computer

4. **Connect XWR1843 EVM to computer**:
   - Connect the Micro-USB end of the cable to the XWR1843 EVM's "XDS110" port
   - Connect the USB-A end to an available USB port on your computer

5. **Power connections**:
   - Connect the 12V power supply to the XWR1843 EVM
   - Ensure the DCA1000 EVM is powered (either through the MMWAVEICBOOST or its own power supply)

### A.2.2 Network Configuration

1. **Configure network adapter**:
   - Open Windows Control Panel > Network and Internet > Network Connections
   - Right-click on the Ethernet adapter connected to the DCA1000 and select "Properties"
   - Select "Internet Protocol Version 4 (TCP/IPv4)" and click "Properties"
   - Select "Use the following IP address" and enter:
     - IP Address: 192.168.33.30
     - Subnet Mask: 255.255.255.0
     - Default Gateway: (leave empty)
   - Click "OK" to save the settings

2. **Configure Windows Firewall**:
   - Open Windows Defender Firewall with Advanced Security
   - Create inbound and outbound rules for UDP ports 4096 and 4098

## A.3 Software Installation

1. **Install Python**:
   - Download Python 3.7.9 from [python.org](https://www.python.org/downloads/release/python-379/)
   - Run the installer and check "Add Python to PATH"

2. **Create a virtual environment** (recommended):
   ```bash
   # Create a virtual environment
   python -m venv radar_env

   # Activate the virtual environment
   radar_env\Scripts\activate
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## A.4 System Architecture

### A.4.1 Software Components

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

#### Common Components

1. **Launcher (`launcher.py`)**
   - Main entry point for the application suite
   - Provides GUI to select and launch specific applications
   - Manages application lifecycle

2. **Radar Configuration**
   - `radar_config.py`: Serial interface to configure XWR1843
   - `radar_config_params.py`: Configuration parameter definitions
   - `radar_parameters.py`: Radar operational parameters calculation

#### Application-Specific Components

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

### A.4.2 Data Flow

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

### A.4.3 Signal Processing Pipeline

#### Range Profile Processing

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

#### Range Doppler Processing

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

#### Range Angle Processing

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

## A.5 Configuration Files

### A.5.1 Default Configuration

The default radar configuration file is located at:
```
config/AWR1843_cfg.cfg
```

This file contains the radar parameters for the XWR1843 EVM, including:
- Frequency range (77 GHz)
- Chirp configuration
- Frame configuration
- ADC configuration
- Data output format

The default configuration provides:
- Range Resolution: 0.044 m
- Maximum Range: 9.02 m
- Maximum Radial Velocity: 1 m/s
- Velocity Resolution: 0.13 m/s
- Frame Duration: 100 ms

Example of the default configuration file:
```
% Platform: xWR18xx_AOP
% Scene Classifier: best_range_res
% Azimuth Resolution(deg): 30 + 38
% Range Resolution(m): 0.044
% Maximum unambiguous Range(m): 9.02
% Maximum Radial Velocity(m/s): 1
% Radial velocity resolution(m/s): 0.13
% Frame Duration(msec): 100

sensorStop
flushCfg
dfeDataOutputMode 1
channelCfg 15 7 0
adcCfg 2 1
adcbufCfg -1 0 1 1 1
profileCfg 0 77 267 7 57.14 0 0 70 1 256 5209 0 0 30
chirpCfg 0 0 0 0 0 0 0 1
chirpCfg 1 1 0 0 0 0 0 2
chirpCfg 2 2 0 0 0 0 0 4
frameCfg 0 2 16 0 100 1 0
...
```

### A.5.2 Key Configuration Parameters

| Parameter | Description | Example Value | Impact |
|-----------|-------------|---------------|--------|
| startFreq | Starting frequency (GHz) | 77 | Center frequency of radar operation |
| freqSlopeConst | Frequency slope (MHz/μs) | 70 | Affects bandwidth and range resolution |
| numAdcSamples | ADC samples per chirp | 256 | Affects maximum range |
| numChirpsPerFrame | Chirps per frame | 16 | Affects velocity resolution |
| framePeriodicity | Frame period (ms) | 100 | Controls update rate |
| txMask | TX antenna mask | 15 (all 4 TX) | Controls which TX antennas are used |
| rxMask | RX antenna mask | 7 (first 3 RX) | Controls which RX antennas are used |

## A.6 Running the Software

### A.6.1 Using the Launcher

1. **Start the launcher**:
   - Navigate to the project directory
   - Activate the virtual environment if using one
   - Run:
   ```bash
   python launcher.py
   ```

2. **Using the launcher interface**:
   - The launcher provides buttons for each application:
     - **Range Profile**: 1D radar processing for distance detection
     - **Range Doppler**: 2D processing for distance and velocity
     - **Range Angle**: 2D processing for distance and angle
   - Click on the desired application to launch it

### A.6.2 Running Individual Applications

You can also run each application directly:

1. **Range Profile Application**:
   ```bash
   python "Range Profile/rp_main.py"
   ```

2. **Range Angle Application**:
   ```bash
   python "Range Angle/ra_main.py"
   ```

3. **Range Doppler Application**:
   ```bash
   python "Range Doppler/rd_main.py"
   ```

4. **Application usage**:
   - Select the COM port connected to the XWR1843 EVM
   - Verify or browse for the configuration file
   - Click "Send Radar Config" to start data capture and processing
   - Adjust processing parameters as needed:
     - Window type (Blackman-Harris, Hamming, etc.)
     - Range padding (for better resolution)
     - Channel selection
     - CFAR detection parameters

## A.7 Troubleshooting

### A.7.1 COM Port Issues

1. **Problem**: Cannot find or connect to COM port
   - **Solution**:
     - Check Device Manager to verify the COM port number
     - Ensure the USB cable is properly connected
     - Try a different USB port
     - Reinstall FTDI drivers

2. **Problem**: COM port found but connection fails
   - **Solution**:
     - Ensure no other application is using the COM port
     - Try closing and reopening the application
     - Restart the computer and the XWR1843 EVM

### A.7.2 Network Connection Issues

1. **Problem**: Cannot ping the DCA1000 EVM
   - **Solution**:
     - Verify Ethernet cable connections
     - Check IP address configuration (should be 192.168.33.30)
     - Ensure the DCA1000 EVM is powered on
     - Try resetting the DCA1000 EVM by cycling power

2. **Problem**: Ping works but no data is received
   - **Solution**:
     - Check firewall settings for UDP ports 4096 and 4098
     - Verify that no other application is using these ports
     - Try running the application as Administrator

### A.7.3 Data Capture Issues

1. **Problem**: No data is being received or processed
   - **Solution**:
     - Ensure the radar is properly configured and started
     - Check that the DCA1000 is properly connected and powered
     - Verify the configuration file parameters match your hardware setup
     - Try restarting the application and hardware

2. **Problem**: Data is received but visualization is not updating
   - **Solution**:
     - Check CPU usage (high CPU usage may cause display lag)
     - Reduce range padding to decrease processing load
     - Close other applications to free up system resources
     - Try updating graphics drivers

## A.8 Performance Optimization

1. **Processing Speed**:
   - Use lower range padding factors
   - Select simpler window functions (e.g., Rectangular)
   - Close other applications to free up CPU resources

2. **Detection Sensitivity**:
   - Adjust CFAR parameters (lower false alarm rate for fewer false detections)
   - Enable static clutter removal for better detection of moving targets
   - Use Blackman-Harris window for better dynamic range

3. **Range Resolution**:
   - Increase bandwidth (higher frequency slope)
   - Use higher range padding factors for interpolated display

4. **Velocity Resolution**:
   - Increase number of chirps per frame
   - Ensure longer frame duration
