# Real Time Data Capture and Processing Tool for mmWave Radar in Python

This is a real-time ADC sample capture and processing tool to obtain and analyze raw data from TI mmWave radar ***XWR1843 EVM*** cascading with ***DCA1000 EVM*** using Python. The tool enables real-time processing to generate Range Profile, Range-Doppler, and Range-Angle images under 1 Transmitter and 4 Receiver (in this version) setting without using mmWave studio.

![Demo](Demo.PNG)

## Table of Contents
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation Guide](#installation-guide)
- [Hardware Setup](#hardware-setup)
- [Network Configuration](#network-configuration)
- [Running the Software](#running-the-software)
- [Using the Applications](#using-the-applications)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Features and Capabilities](#features-and-capabilities)
- [Contact](#contact)
- [Acknowledgement](#acknowledgement)
- [Citation](#citation)

## Hardware Requirements

- **Radar Device**: 
  - Texas Instruments XWR1843 EVM (Evaluation Module)
  - DCA1000 EVM (Data Capture Card)
- **Computer**:
  - Windows 10 operating system
  - Ethernet port for connecting to DCA1000
  - USB port for connecting to XWR1843 (serial configuration)

## Software Requirements

The project requires several Python packages. The main dependencies include:

* Python 3.8 or higher
* colorama==0.4.6
* contourpy==1.3.1
* cycler==0.12.1
* fonttools==4.56.0
* kiwisolver==1.4.8
* matplotlib==3.10.0
* numpy==2.2.2
* opencv-python==4.11.0.86
* packaging==24.2
* pillow==11.1.0
* pyparsing==3.2.1
* python-dateutil==2.9.0.post0
* six==1.17.0
* tqdm==4.67.1
* PyQt5==5.15.11
* psutil==7.0.0
* pyqtgraph==0.13.7
* pyserial==3.5
* scipy==1.16.0
* numba==0.61.2
* pyfftw==0.15.0

A complete list of dependencies with exact versions is available in the `requirements.txt` file.

## Installation Guide

### Step 1: Clone or Download the Repository

Download the repository to your local machine:

```bash
git clone https://github.com/aijay3/Live-Radar-Demonstrator-using-Raw-ADC-Data-in-Python.git
cd Live-Radar-Demonstrator-using-Raw-ADC-Data-in-Python
```

### Step 2: Set Up Python Environment

It's recommended to use a virtual environment:

#### Option 1: Using Conda (Recommended)

```bash
# Create and activate the conda environment
conda env create -f environment.yml
conda activate real-time-radar
```

#### Option 2: Using pip and venv

```bash
# Create a virtual environment
python -m venv radar_env

# Activate the virtual environment
# On Windows:
radar_env\Scripts\activate
# On macOS/Linux:
source radar_env/bin/activate
```

### Step 3: Install Dependencies

If using pip (Option 2 above), install all required packages:

```bash
pip install -r requirements.txt
```

## Hardware Setup

### Connecting the Hardware

1. Connect the XWR1843 EVM to the DCA1000 EVM using the MMWAVEICBOOST adapter board.
2. Connect the DCA1000 EVM to your computer using an Ethernet cable.
3. Connect the XWR1843 EVM to your computer using a USB cable for serial configuration.

### Flashing the Radar

1. Download and install TI's "UniFlash" tool from the Texas Instruments website.
2. Use UniFlash to flash the XWR1843 EVM with the demo firmware.
3. Verify that the radar is properly flashed by checking the LED indicators on the board.

## Network Configuration

### Setting Up the Network Interface

1. Configure your computer's Ethernet adapter with the following settings:
   - IP Address: 192.168.33.30
   - Subnet Mask: 255.255.255.0
   - Default Gateway: (leave empty)

2. Verify the connection by pinging the DCA1000 EVM:
   ```bash
   ping 192.168.33.180
   ```

3. Ensure that the software is allowed through your firewall:
   - Open Windows Defender Firewall
   - Allow the Python application through the firewall
   - Ensure UDP ports 4096 and 4098 are open for communication

## Running the Software

### Using the Launcher

The easiest way to run the software is using the launcher application:

```bash
python launcher.py
```

This will open a GUI that allows you to select which application to run:
- Range Profile: Basic 1D radar processing to detect object distance
- Range Doppler: 2D radar processing to detect object distance and velocity
- Range Angle: 2D radar processing to detect object distance and angle

### Running Individual Applications

You can also run any of the three main applications directly:

#### Range Profile Application
```bash
python "Range Profile/rp_main.py"
```

#### Range Angle Application
```bash
python "Range Angle/ra_main.py"
```

#### Range Doppler Application
```bash
python "Range Doppler/rd_main.py"
```

## Using the Applications

### Common Interface Elements

All three applications share similar interface elements:

1. **Configuration Section**:
   - COM Port Selection: Choose the COM port connected to the XWR1843 EVM
   - Configuration File: Select the radar configuration file (default is in the config folder)

2. **Processing Controls**:
   - Window Type: Select the FFT window function (Blackman-Harris, Hamming, etc.)
   - Range Padding: Adjust the FFT padding for better resolution
   - Channel Selection: Choose which receiver channel to display
   - Static Clutter Removal: Toggle clutter removal processing

3. **CFAR Detection Settings**:
   - Guard Cells: Number of guard cells for CFAR detection
   - Training Cells: Number of training cells for CFAR detection
   - False Alarm Rate: Probability of false alarm for detection threshold
   - Group Peaks: Enable/disable peak grouping for object detection

### Starting Data Capture

1. Select the appropriate COM port from the dropdown menu.
2. Verify the configuration file path (default is config/AWR1843_cfg.cfg).
3. Click the "Send Radar Config" button to start the real-time data capture and processing.
4. The visualization will update in real-time as data is received from the radar.
5. Detected objects will be displayed in the data table with range and magnitude information.

### Adjusting Processing Parameters

You can adjust various processing parameters in real-time:

1. **Window Function**: Change the window type to adjust the trade-off between resolution and sidelobe suppression.
2. **Range Padding**: Increase padding for better range resolution at the cost of processing time.
3. **Channel Selection**: View individual receiver channels or the combined output.
4. **Clutter Removal**: Enable to remove static background reflections.
5. **CFAR Parameters**: Adjust detection sensitivity and object grouping.

## Troubleshooting

### COM Port Issues

- **Problem**: Cannot find or connect to COM port
- **Solution**: 
  - Verify the USB connection to the XWR1843 EVM
  - Check Device Manager to confirm the COM port number
  - Try disconnecting and reconnecting the USB cable
  - Install/update the FTDI drivers for the XWR1843 EVM

### Network Connection Issues

- **Problem**: Cannot communicate with the DCA1000 EVM
- **Solution**:
  - Verify the Ethernet connection and IP address configuration
  - Check Windows Firewall settings to ensure the application is allowed
  - Restart the DCA1000 EVM by power cycling
  - Verify the network adapter settings

### Data Capture Issues

- **Problem**: No data is being received or processed
- **Solution**:
  - Ensure the radar is properly configured and started
  - Check that the DCA1000 is properly connected and powered
  - Verify the configuration file parameters match your hardware setup
  - Try restarting the application and hardware

### Application Crashes

- **Problem**: Application crashes during operation
- **Solution**:
  - Check the console output for error messages
  - Ensure all dependencies are properly installed
  - Verify that no other applications are using the same COM port or network ports
  - Try running with a smaller range padding size to reduce memory usage

## Project Structure

The project is organized into three main components:

1. **Range Profile (RP)**: Basic 1D radar processing to detect object distance
   * `rp_main.py`: Main application for Range Profile visualization
   * `rp_dsp.py`: Digital signal processing for Range Profile
   * `rp_app_layout.py`: UI layout for Range Profile application
   * `rp_real_time_process.py`: Real-time processing for Range Profile

2. **Range Angle (RA)**: 2D radar processing to detect object distance and angle
   * `ra_main.py`: Main application for Range-Angle visualization
   * `ra_dsp.py`: Digital signal processing for Range-Angle
   * `ra_app_layout.py`: UI layout for Range-Angle application
   * `ra_real_time_process.py`: Real-time processing for Range-Angle
   * `coordinate_transforms.py`: Coordinate transformation utilities

3. **Range Doppler (RD)**: 2D radar processing to detect object distance and velocity
   * `rd_main.py`: Main application for Range-Doppler visualization
   * `rd_dsp.py`: Digital signal processing for Range-Doppler
   * `rd_app_layout.py`: UI layout for Range-Doppler application
   * `rd_real_time_process.py`: Real-time processing for Range-Doppler

### Common Components
* `radar_config.py`: Configuration interface for the radar
* `radar_config_params.py`: Configuration parameters for the radar
* `radar_parameters.py`: Radar operational parameters
* `launcher.py`: Main launcher application for easy access to all tools

### Configuration Files
* `config/AWR1843_cfg.cfg`: Default configuration file for the XWR1843 EVM

## Features and Capabilities

### Data Acquisition
* Real-time ADC sample capture from TI mmWave radar via UDP
* Support for XWR1843 EVM with DCA1000 EVM data capture card
* Configurable radar parameters through configuration files

### Signal Processing
* Range Profile processing (1D FFT) with configurable window functions and zero-padding
* Range-Angle processing (2D FFT) for spatial mapping
* Range-Doppler processing for velocity detection
* Static clutter removal
* CFAR (Constant False Alarm Rate) detection with adjustable parameters
* Multiple visualization channels (individual RX channels or combined)

### User Interface
* Real-time visualization of radar data
* Interactive parameter adjustment
* Detected object display with range and magnitude information
* Channel selection for detailed analysis
* Configuration file management
