# Detailed Setup and Installation Guide for Real Time Radar

This guide provides comprehensive instructions for setting up and installing the Real Time Radar processing tool for TI mmWave radar XWR1843 EVM with DCA1000 EVM.

## Table of Contents
1. [Hardware Requirements](#1-hardware-requirements)
2. [Software Requirements](#2-software-requirements)
3. [Hardware Setup](#3-hardware-setup)
   - [Physical Connections](#31-physical-connections)
   - [Flashing the Radar](#32-flashing-the-radar)
4. [Network Configuration](#4-network-configuration)
   - [Ethernet Setup](#41-ethernet-setup)
   - [Firewall Configuration](#42-firewall-configuration)
5. [Software Installation](#5-software-installation)
   - [Python Environment Setup](#51-python-environment-setup)
   - [Installing Dependencies](#52-installing-dependencies)
   - [Verifying Installation](#53-verifying-installation)
6. [Configuration Files](#6-configuration-files)
   - [Default Configuration](#61-default-configuration)
   - [Custom Configuration](#62-custom-configuration)
7. [Running the Software](#7-running-the-software)
   - [Using the Launcher](#71-using-the-launcher)
   - [Running Individual Applications](#72-running-individual-applications)
8. [Troubleshooting](#8-troubleshooting)
   - [COM Port Issues](#81-com-port-issues)
   - [Network Connection Issues](#82-network-connection-issues)
   - [Data Capture Issues](#83-data-capture-issues)
   - [Application Crashes](#84-application-crashes)
9. [Updating the Software](#9-updating-the-software)

## 1. Hardware Requirements

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

## 2. Software Requirements

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

## 3. Hardware Setup

### 3.1 Physical Connections

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

### 3.2 Flashing the Radar

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

## 4. Network Configuration

### 4.1 Ethernet Setup

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

### 4.2 Firewall Configuration

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

## 5. Software Installation

### 5.1 Python Environment Setup

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

### 5.2 Installing Dependencies

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

### 5.3 Verifying Installation

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

## 6. Configuration Files

### 6.1 Default Configuration

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

### 6.2 Custom Configuration

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

3. **Understanding radar parameter impacts**:
   - **Range Resolution**: Determined by bandwidth (controlled by `freqSlopeConst` and `rampEndTime`)
     - Higher bandwidth = better range resolution
     - Formula: Range Resolution = c / (2 × Bandwidth)
     - Example: With 4 GHz bandwidth, resolution is approximately 0.0375 m
   
   - **Maximum Range**: Determined by sampling frequency and number of samples
     - Formula: Max Range = (c × Sampling Frequency × Number of ADC Samples) / (2 × Bandwidth)
     - Increasing `numAdcSamples` increases maximum range
   
   - **Velocity Resolution**: Determined by carrier frequency and chirp duration
     - Formula: Velocity Resolution = λ / (2 × Number of Chirps × Frame Time)
     - Increasing `numChirpsPerFrame` improves velocity resolution
   
   - **Maximum Velocity**: Determined by chirp repetition time
     - Formula: Max Velocity = λ / (4 × Chirp Repetition Time)
     - Decreasing chirp time increases maximum detectable velocity
   
   - **Angular Resolution**: Determined by number of RX antennas and array configuration
     - More RX antennas = better angular resolution
     - Controlled by `channelCfg` parameter

4. **Loading custom configurations**:
   - In the application, use the "Browse" button to select your custom configuration file
   - Click "Send Radar Config" to apply the configuration

## 7. Running the Software

### 7.1 Using the Launcher

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

### 7.2 Running Individual Applications

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

## 8. Troubleshooting

### 8.1 COM Port Issues

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

### 8.2 Network Connection Issues

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

### 8.3 Data Capture Issues

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

### 8.4 Application Crashes

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

## 9. Updating the Software

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
   - Follow the flashing procedure in section 3.2
