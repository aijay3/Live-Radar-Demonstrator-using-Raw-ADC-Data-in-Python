# Comprehensive Guide for Real Time Radar System

This guide provides complete documentation for the Real Time Radar processing tool for TI mmWave radar XWR1843 EVM with DCA1000 EVM, including setup instructions, reference information, and system architecture details.

## Table of Contents
1. [Introduction](#1-introduction)
2. [Hardware Requirements](#2-hardware-requirements)
3. [Software Requirements](#3-software-requirements)
4. [Hardware Setup](#4-hardware-setup)
   - [Physical Connections](#41-physical-connections)
   - [Flashing the Radar](#42-flashing-the-radar)
5. [Network Configuration](#5-network-configuration)
   - [Ethernet Setup](#51-ethernet-setup)
   - [Firewall Configuration](#52-firewall-configuration)
6. [Software Installation](#6-software-installation)
   - [Python Environment Setup](#61-python-environment-setup)
   - [Installing Dependencies](#62-installing-dependencies)
   - [Verifying Installation](#63-verifying-installation)
7. [System Architecture](#7-system-architecture)
   - [Hardware Components](#71-hardware-components)
   - [Software Components](#72-software-components)
   - [Data Flow](#73-data-flow)
   - [Signal Processing Pipeline](#74-signal-processing-pipeline)
8. [Configuration Files](#8-configuration-files)
   - [Default Configuration](#81-default-configuration)
   - [Custom Configuration](#82-custom-configuration)
   - [Radar Parameter Impacts](#83-radar-parameter-impacts)
9. [Running the Software](#9-running-the-software)
   - [Using the Launcher](#91-using-the-launcher)
   - [Running Individual Applications](#92-running-individual-applications)
10. [Quick Reference](#10-quick-reference)
    - [Essential Commands](#101-essential-commands)
    - [Key Configuration Parameters](#102-key-configuration-parameters)
    - [Common Configuration Scenarios](#103-common-configuration-scenarios)
    - [Processing Parameters](#104-processing-parameters)
11. [Troubleshooting](#11-troubleshooting)
    - [COM Port Issues](#111-com-port-issues)
    - [Network Connection Issues](#112-network-connection-issues)
    - [Data Capture Issues](#113-data-capture-issues)
    - [Application Crashes](#114-application-crashes)
12. [Performance Optimization](#12-performance-optimization)
13. [Updating the Software](#13-updating-the-software)
14. [Support and Contact](#14-support-and-contact)
15. [Acknowledgements and Citation](#15-acknowledgements-and-citation)

## 1. Introduction

The Real Time Radar system is a real-time ADC sample capture and processing tool to obtain and analyze raw data from TI mmWave radar XWR1843 EVM cascading with DCA1000 EVM using Python. The tool enables real-time processing to generate Range Profile, Range-Doppler, and Range-Angle images under 1 Transmitter and 4 Receiver setting without using mmWave studio.

The system provides three main applications:
- **Range Profile**: 1D radar processing to detect object distance
- **Range Doppler**: 2D radar processing to detect object distance and velocity
- **Range Angle**: 2D radar processing to detect object distance and angle

## 2. Hardware Requirements

### Essential Hardware:
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

### Optional Hardware:
- **Tripod or mounting fixture** for stable radar positioning
- **Additional USB hub** if computer ports are limited
- **Oscilloscope** for debugging (if available)

## 3. Software Requirements

### Required Software:
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
  - cycler==0.10.0
  - kiwisolver==1.2.0
  - pyparsing==2.4.7
  - python-dateutil==2.8.1
  - six==1.15.0

### Additional Software:
- **TI UniFlash** for flashing the XWR1843 EVM (download from Texas Instruments website)
- **FTDI drivers** for the XWR1843 EVM serial communication
- **Git** (optional, for cloning the repository)

## 4. Hardware Setup

### 4.1 Physical Connections

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

6. **Verify connections**:
   - Check that all cables are securely connected
   - Ensure power indicators are lit on both the XWR1843 and DCA1000 EVMs

### 4.2 Flashing the Radar

1. **Install TI UniFlash**:
   - Download UniFlash from the [Texas Instruments website](https://www.ti.com/tool/UNIFLASH)
   - Install following the provided instructions

2. **Prepare for flashing**:
   - Ensure the XWR1843 EVM is connected to your computer via USB
   - Power on the XWR1843 EVM

3. **Flash the firmware**:
   - Launch UniFlash
   - Select "xWR1843" from the device list
   - Choose the appropriate firmware file (typically a .bin file provided by TI)
   - Click "Load Image" to flash the firmware
   - Wait for the flashing process to complete (typically 2-5 minutes)

4. **Verify successful flashing**:
   - Check for any error messages in UniFlash
   - Verify that the LEDs on the XWR1843 EVM are functioning correctly
   - Restart the XWR1843 EVM by cycling power

## 5. Network Configuration

### 5.1 Ethernet Setup

1. **Configure network adapter**:
   - Open Windows Control Panel > Network and Internet > Network Connections
   - Right-click on the Ethernet adapter connected to the DCA1000 and select "Properties"
   - Select "Internet Protocol Version 4 (TCP/IPv4)" and click "Properties"
   - Select "Use the following IP address" and enter:
     - IP Address: 192.168.33.30
     - Subnet Mask: 255.255.255.0
     - Default Gateway: (leave empty)
   - Click "OK" to save the settings

2. **Verify connection**:
   - Open Command Prompt
   - Type `ping 192.168.33.180` and press Enter
   - Verify that you receive replies from the DCA1000 EVM
   - If no replies, check physical connections and IP configuration

### 5.2 Firewall Configuration

1. **Configure Windows Firewall**:
   - Open Windows Defender Firewall with Advanced Security
   - Select "Inbound Rules" and click "New Rule"
   - Select "Port" and click "Next"
   - Select "UDP" and enter "4096,4098" in the "Specific local ports" field
   - Click "Next", select "Allow the connection", and click "Next" again
   - Select all network types (Domain, Private, Public) and click "Next"
   - Name the rule "DCA1000 Data Capture" and click "Finish"

2. **Repeat for outbound rules**:
   - Select "Outbound Rules" and create a similar rule for UDP ports 4096 and 4098

## 6. Software Installation

### 6.1 Python Environment Setup

1. **Install Python**:
   - Download Python 3.7.9 from [python.org](https://www.python.org/downloads/release/python-379/)
   - Run the installer and check "Add Python to PATH"
   - Complete the installation

2. **Verify Python installation**:
   - Open Command Prompt
   - Type `python --version` and press Enter
   - Verify that the output shows "Python 3.7.9"

3. **Create a virtual environment** (recommended):
   - Navigate to your desired project directory
   - Open Command Prompt in that directory
   - Run the following commands:
   ```bash
   # Create a virtual environment
   python -m venv radar_env

   # Activate the virtual environment
   radar_env\Scripts\activate
   ```

### 6.2 Installing Dependencies

1. **Download the project**:
   - Download the Real Time Radar project files
   - Extract to a convenient location (e.g., C:\Users\username\Desktop\Real Time Radar)

2. **Install required packages**:
   - With the virtual environment activated, navigate to the project directory
   - Run the following command:
   ```bash
   pip install -r requirements.txt
   ```
   - Wait for all dependencies to install (this may take several minutes)

3. **Install additional dependencies** (if needed):
   - Some systems may require additional packages for OpenGL support:
   ```bash
   pip install PyOpenGL PyOpenGL_accelerate
   ```

### 6.3 Verifying Installation

1. **Verify package installation**:
   - Run the following command to list installed packages:
   ```bash
   pip list
   ```
   - Verify that all packages from requirements.txt are listed

2. **Test basic functionality**:
   - Navigate to the project directory
   - Run the launcher with:
   ```bash
   python launcher.py
   ```
   - Verify that the launcher GUI opens without errors

## 7. System Architecture

### 7.1 Hardware Components

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

### 7.2 Software Components

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

### 7.3 Data Flow

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

### 7.4 Signal Processing Pipeline

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

## 8. Configuration Files

### 8.1 Default Configuration

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
- Detection Thresholds: 15 dB for both Range and Doppler

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

### 8.2 Custom Configuration

1. **Creating custom configurations**:
   - Copy the default configuration file to create a new one
   - Edit the parameters according to your requirements
   - Save with a descriptive name (e.g., `custom_long_range.cfg`)

2. **Important parameters to consider**:
   - `channelCfg`: Configures TX/RX channels (format: `channelCfg <txMask> <rxMask> <cascading>`)
     - Example: `channelCfg 15 7 0` enables TX channels 0-3 and RX channels 0-2
   
   - `profileCfg`: Configures the chirp profile (format: `profileCfg <profileId> <startFreq> <idleTime> <adcStartTime> <rampEndTime> <txOutPower> <txPhaseShifter> <freqSlopeConst> <txStartTime> <numAdcSamples> <digOutSampleRate> <hpfCornerFreq1> <hpfCornerFreq2> <rxGain>`)
     - Example: `profileCfg 0 77 267 7 57.14 0 0 70 1 256 5209 0 0 30`
       - `startFreq`: 77 GHz
       - `idleTime`: 267 μs
       - `adcStartTime`: 7 μs
       - `rampEndTime`: 57.14 μs
       - `freqSlopeConst`: 70 MHz/μs
       - `numAdcSamples`: 256 samples
       - `rxGain`: 30 dB
   
   - `chirpCfg`: Configures individual chirps (format: `chirpCfg <chirpStartIdx> <chirpEndIdx> <profileId> <startFreqVar> <freqSlopeVar> <idleTimeVar> <adcStartTimeVar> <txMask>`)
     - Example: `chirpCfg 0 0 0 0 0 0 0 1` configures chirp 0 with profile 0 and TX antenna 0
   
   - `frameCfg`: Configures the frame (format: `frameCfg <chirpStartIdx> <chirpEndIdx> <numLoops> <numFrames> <framePeriodicity> <triggerSelect> <frameTriggerDelay>`)
     - Example: `frameCfg 0 2 16 0 100 1 0`
       - Uses chirps 0-2
       - 16 loops per frame
       - Continuous frame mode (numFrames = 0)
       - 100 ms frame periodicity
   
   - `cfarCfg`: Configures CFAR detection (format: `cfarCfg <detectionDomain> <mode> <noiseWin> <guardWin> <divShift> <cyclicMode> <thresholdScale> <peakGrouping>`)
     - Example: `cfarCfg -1 0 2 8 4 3 0 15 1`
       - Detection threshold: 15 dB
       - Guard cells: 8
       - Training cells: 2

### 8.3 Radar Parameter Impacts

1. **Range Resolution**: Determined by bandwidth (controlled by `freqSlopeConst` and `rampEndTime`)
   - Higher bandwidth = better range resolution
   - Formula: Range Resolution = c / (2 × Bandwidth)
   - Example: With 4 GHz bandwidth, resolution is approximately 0.0375 m

2. **Maximum Range**: Determined by sampling frequency and number of samples
   - Formula: Max Range = (c × Sampling Frequency × Number of ADC Samples) / (2 × Bandwidth)
   - Increasing `numAdcSamples` increases maximum range

3. **Velocity Resolution**: Determined by carrier frequency and chirp duration
   - Formula: Velocity Resolution = λ / (2 × Number of Chirps × Frame Time)
   - Increasing `numChirpsPerFrame` improves velocity resolution

4. **Maximum Velocity**: Determined by chirp repetition time
   - Formula: Max Velocity = λ / (4 × Chirp Repetition Time)
   - Decreasing chirp time increases maximum detectable velocity

5. **Angular Resolution**: Determined by number of RX antennas and array configuration
   - More RX antennas = better angular resolution
   - Controlled by `channelCfg` parameter

## 9. Running the Software

### 9.1 Using the Launcher

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

### 9.2 Running Individual Applications

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

## 10. Quick Reference

### 10.1 Essential Commands

#### Starting the Applications

```bash
# Launch the main launcher application
python launcher.py

# Launch Range Profile application directly
python "Range Profile/rp_main.py"

# Launch Range Doppler application directly
python "Range Doppler/rd_main.py"

# Launch Range Angle application directly
python "Range Angle/ra_main.py"
```

#### Python Environment

```bash
# Create virtual environment
python -m venv radar_env

# Activate virtual environment (Windows)
radar_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# List installed packages
pip list
```

#### Network Testing

```bash
# Test connection to DCA1000 EVM
ping 192.168.33.180

# Check UDP ports (Windows)
netstat -a -p UDP | findstr "4096 4098"
```

### 10.2 Key Configuration Parameters

#### Radar Configuration Quick Reference

| Parameter | Description | Example Value | Impact |
|-----------|-------------|---------------|--------|
| startFreq | Starting frequency (GHz) | 77 | Center frequency of radar operation |
| freqSlopeConst | Frequency slope (MHz/μs) | 70 | Affects bandwidth and range resolution |
| numAdcSamples | ADC samples per chirp | 256 | Affects maximum range |
| numChirpsPerFrame | Chirps per frame | 16 | Affects velocity resolution |
| framePeriodicity | Frame period (ms) | 100 | Controls update rate |
| txMask | TX antenna mask | 15 (all 4 TX) | Controls which TX antennas are used |
| rxMask | RX antenna mask | 7 (first 3 RX) | Controls which RX antennas are used |

### 10.3 Common Configuration Scenarios

#### Long Range Configuration
```
profileCfg 0 77 267 7 57.14 0 0 40 1 512 5209 0 0 30
frameCfg 0 2 16 0 100 1 0
```
- Lower frequency slope (40 MHz/μs)
- More ADC samples (512)
- Impact: Longer maximum range, reduced range resolution

#### High Resolution Configuration
```
profileCfg 0 77 267 7 57.14 0 0 100 1 256 5209 0 0 30
frameCfg 0 2 16 0 100 1 0
```
- Higher frequency slope (100 MHz/μs)
- Impact: Better range resolution, reduced maximum range

#### Fast Update Rate Configuration
```
profileCfg 0 77 267 7 57.14 0 0 70 1 256 5209 0 0 30
frameCfg 0 2 16 0 50 1 0
```
- Reduced frame periodicity (50 ms)
- Impact: Faster update rate, potentially increased CPU load

### 10.4 Processing Parameters

#### Window Functions

| Window Type | Characteristics | Best For |
|-------------|-----------------|----------|
| Blackman-Harris | Excellent sidelobe suppression, wider mainlobe | Scenarios with large dynamic range between targets |
| Hamming | Good balance between mainlobe width and sidelobe level | General purpose |
| Hanning | Similar to Hamming but with different coefficients | General purpose |
| Rectangular | Narrowest mainlobe, highest sidelobes | High resolution between targets of similar RCS |

#### Range Padding

| Padding Factor | Effect |
|----------------|--------|
| 1x | No padding, fastest processing |
| 2x | Doubled range bins, smoother display |
| 4x | 4x range bins, much smoother display, slower processing |
| 8x | 8x range bins, very smooth display, slowest processing |

#### CFAR Detection

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| Guard Cells | Cells around target to exclude from background | 4-8 |
| Training Cells | Cells used to estimate background | 8-16 |
| False Alarm Rate | Probability of false detection | 0.001-0.01 |

## 11. Troubleshooting

### 11.1 COM Port Issues

1. **Problem**: Cannot find or connect to COM port
   - **Solution**:
     - Check Device Manager to verify the COM port number
     - Ensure the USB cable is properly connected
     - Try a different USB port
     - Reinstall FTDI drivers from the [FTDI website](https://ftdichip.com/drivers/)

2. **Problem**: COM port found but connection fails
   - **Solution**:
     - Ensure no other application is using the COM port
     - Try closing and reopening the application
     - Restart the computer and the XWR1843 EVM

### 11.2 Network Connection Issues

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

### 11.3 Data Capture Issues

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

### 11.4 Application Crashes

1. **Problem**: Application crashes during startup
   - **Solution**:
     - Check console output for error messages
     - Verify all dependencies are installed correctly
     - Try reinstalling the required packages
     - Check for conflicts with other Python installations

2. **Problem**: Application crashes during operation
   - **Solution**:
     - Reduce range padding to decrease memory usage
     - Close other memory-intensive applications
     - Check for memory leaks by monitoring memory usage
     - Try running with a smaller configuration (fewer samples or chirps)

## 12. Performance Optimization

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

## 13. Updating the Software

1. **Checking for updates**:
   - Visit the project repository regularly for updates
   - Download the latest version when available

2. **Updating the software**:
   - Back up your custom configuration files
   - Download and extract the new version
   - Install any new dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   - Copy your custom configuration files back if needed

3. **Updating firmware** (if required):
   - Check the release notes for firmware requirements
   - Use TI UniFlash to update the XWR1843 EVM firmware if needed
   - Follow the flashing procedure in section 4.2

## 14. Support and Contact

For support or questions, please contact:
- Jih-Tsun Yu: t108368020@ntut.org.tw
- Jyun-Jhih Lin: t109368038@ntut.org.tw

If you encounter issues not covered in the troubleshooting section, please provide the following information when seeking support:
- Hardware configuration details
- Software version
- Error messages or logs
- Steps to reproduce the issue
- Screenshots of the issue if applicable

## 15. Acknowledgements and Citation

### Acknowledgements

Thanks to TI, TI's e2e forum, and other people working on mmWave Radar for making this project possible. Special thanks to Mr. Chieh-Hsun Hsieh for his help.

### Citation

If you use this tool in your research, please cite:

J. Yu, L. Yen and P. Tseng, "mmWave Radar-based Hand Gesture Recognition using Range-Angle Image," 2020 IEEE 91st Vehicular Technology Conference (VTC2020-Spring), Antwerp, Belgium, 2020, pp. 1-5, doi: 10.1109/VTC2020-Spring48590.2020.9128573.

**BibTex Form**
```
@INPROCEEDINGS{9128573,
  author={J. {Yu} and L. {Yen} and P. {Tseng}},
  booktitle={2020 IEEE 91st Vehicular Technology Conference (VTC2020-Spring)}, 
  title={mmWave Radar-based Hand Gesture Recognition using Range-Angle Image}, 
  year={2020},
  pages={1-5},
  doi={10.1109/VTC2020-Spring48590.2020.9128573}
}
```

### Demo Video

A demonstration video of the system in action is available at: [Watch the demo video on YouTube](https://youtu.be/Z6rTQDMe6a4)
