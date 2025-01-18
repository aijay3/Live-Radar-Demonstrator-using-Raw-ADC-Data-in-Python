"""
Main application module for real-time radar visualization.
"""

from real_time_process import UdpListener, DataProcessor
from radar_config import SerialConfig
from radar_parameters import RadarParameters
from dsp import calculate_range_profile
from queue import Queue
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import numpy as np  
import threading
import time
import sys
import socket
import logging
from typing import Optional, List, Tuple
from app_layout import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os
import serial.tools.list_ports

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_COM_PORT = "COM5"
SOCKET_TIMEOUT = 0.1  # seconds
BUFFER_SIZE = 2097152  # bytes
FRAME_QUEUE_TIMEOUT = 0.5  # seconds
PACKET_HEADER = (0xA55A).to_bytes(2, byteorder='little', signed=False)
PACKET_FOOTER = (0xEEAA).to_bytes(2, byteorder='little', signed=False)
PACKET_SIZE_ZERO = (0x00).to_bytes(2, byteorder='little', signed=False)
PACKET_SIZE_SIX = (0x06).to_bytes(2, byteorder='little', signed=False)

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

# FPGA Configuration Data
FPGA_CONFIG_DATA = (0x01020102031e).to_bytes(6, byteorder='big', signed=False)
PACKET_CONFIG_DATA = (0xc005350c0000).to_bytes(6, byteorder='big', signed=False)

# Network Configuration
RADAR_HOST = '192.168.33.30'
RADAR_DATA_PORT = 4098
RADAR_CONFIG_PORT = 4096
FPGA_CONFIG_HOST = '192.168.33.180'
FPGA_CONFIG_PORT = 4096

# Data Processing Queues
binary_data_queue = Queue()
range_doppler_queue = Queue()
range_angle_queue = Queue()
range_profile_queue = Queue()

# Default Radar Configuration (updated when config file is loaded)
num_adc_samples = 256  # Default values
num_chirps = 16
num_tx_channels = 3
num_rx_channels = 4  
radar_config = [num_adc_samples, num_chirps, num_tx_channels, num_rx_channels]
frame_length = num_adc_samples * num_chirps * num_tx_channels * num_rx_channels * 2

# Network addresses
data_address = (RADAR_HOST, RADAR_DATA_PORT)
config_address = (RADAR_HOST, RADAR_CONFIG_PORT)
fpga_address = (FPGA_CONFIG_HOST, FPGA_CONFIG_PORT)

# Global instances
config = None
radar_params = None
plot_widget = None
ui = None
collector = None
processor = None
radar_ctrl = None
fpga_socket = None

def get_available_com_ports() -> List[str]:
    """Get a list of available COM ports."""
    try:
        ports = [port.device for port in serial.tools.list_ports.comports()]
        logger.debug(f"Found COM ports: {ports}")
        return ports
    except Exception as e:
        logger.error(f"Error getting COM ports: {e}")
        return []

def browse_config():
    """Browse and load radar configuration file."""
    global ui, radar_params
    filename, _ = QFileDialog.getOpenFileName(
        None,
        "Select Configuration File",
        os.path.dirname(os.path.abspath(__file__)),
        "Config Files (*.cfg);;All Files (*.*)"
    )
    if filename:
        try:
            radar_params = RadarParameters(filename)
            ui.config_path.setText(os.path.basename(filename))
            ui.config_path.setProperty("fullPath", filename)
        except Exception as e:
            logger.error(f"Failed to process config file: {e}")

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

def update_figure() -> None:
    """Update range profile visualization plot with new data."""
    global plot_rpl, update_time, plot_widget, ui, radar_params
    
    # Get latest data
    range_profile_data = range_profile_queue.get()
    
    # Calculate range axis using radar parameters
    range_resolution = radar_params.range_resolution if radar_params else 0.0488
    range_axis = np.arange(len(range_profile_data)) * range_resolution
    
    # Update selected channel range profile
    # Average across chirps for the selected channel
    profile_data_selected = range_profile_data[:, 0, :]  # Select first channel
    profile_power = np.mean(np.abs(profile_data_selected) ** 2, axis=1)  # Average across chirps
    profile_data_db = 10 * np.log10(profile_power / np.max(profile_power) + 1e-10)
    plot_rpl.setData(range_axis, profile_data_db)
    
    QtCore.QTimer.singleShot(1, update_figure)
    update_time = ptime.time()

def initialize_radar() -> None:
    """Initialize and start radar data collection."""
    global radar_ctrl, config, ui, radar_config, frame_length, radar_params
    
    # Get configuration
    com_port = ui.com_select.currentText()
    config_path = ui.config_path.property("fullPath")
    
    # Validate inputs
    if not com_port:
        logger.error("Please select a COM port")
        return
    if not config_path or not os.path.exists(config_path):
        logger.error("Please select a valid configuration file")
        return
    
    # Initialize radar parameters
    if not radar_params:
        radar_params = RadarParameters(config_path)
    
    # Display parameters
    params = radar_params.get_all_parameters()
    logger.info("\n=== Calculated Radar Parameters ===")
    for key, value in params.items():
        if isinstance(value, float):
            logger.info(f"{key}: {value:.2f}")
        else:
            logger.info(f"{key}: {value}")
    logger.info("================================")
    
    # Update configuration
    num_adc_samples = radar_params.config_params['adc_samples']
    num_chirps = radar_params.config_params['chirps_per_frame']
    num_tx_channels = radar_params.num_tx_channels
    num_rx_channels = radar_params.num_rx_channels
    
    radar_config = [num_adc_samples, num_chirps, num_tx_channels, num_rx_channels]
    frame_length = int(radar_params.radar_cube_size * 1024)
    
    # Initialize radar
    radar_ctrl = SerialConfig(name='ConnectRadar', CLIPort=com_port, BaudRate=115200)
    radar_ctrl.StopRadar()
    radar_ctrl.SendConfig(config_path)
    
    # Start radar
    time.sleep(1)
    radar_ctrl.StartRadar()
    logger.info("Radar started and streaming data...")
    
    
    update_figure()

def cleanup() -> None:
    """Cleanup all resources and stop data collection."""
    global collector, processor, fpga_socket, radar_ctrl
    logger.info("Starting cleanup...")
    
    # Stop radar
    if hasattr(radar_ctrl, 'StopRadar'):
        try:
            radar_ctrl.StopRadar()
            logger.info("Radar stopped")
        except Exception as e:
            logger.error(f"Error stopping radar: {e}")
    
    # Stop threads
    for thread, name in [(collector, "Collector"), (processor, "Processor")]:
        if thread and thread.is_alive():
            try:
                thread.stop()
                thread.join(timeout=2)
                if thread.is_alive():
                    logger.warning(f"{name} thread did not stop gracefully")
                else:
                    logger.info(f"{name} thread stopped successfully")
            except Exception as e:
                logger.error(f"Error stopping {name} thread: {e}")
    
    # Close socket
    if fpga_socket:
        try:
            fpga_socket.sendto(create_command_packet('6'), fpga_address)
            fpga_socket.close()
            logger.info("Config socket closed")
        except Exception as e:
            logger.error(f"Error closing config socket: {e}")
    
    # Clear queues
    for queue in [binary_data_queue, range_doppler_queue, range_angle_queue, range_profile_queue]:
        try:
            while not queue.empty():
                queue.get_nowait()
        except Exception as e:
            logger.debug(f"Error clearing queue: {e}")
            
    logger.info("Cleanup completed")

def initialize_gui() -> None:
    """Initialize and run the main application window."""
    global plot_rpl, update_time, collector, processor, fpga_socket
    global radar_ctrl, plot_widget, ui
    
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    
    # Configure close event
    def handle_close(event):
        cleanup()
        app.quit()
        event.accept()
        sys.exit()
    
    main_window.closeEvent = handle_close
    main_window.show()
    
    # Initialize buttons
    start_button = ui.start_button
    exit_button = ui.exit_button
    
    # Setup COM ports
    com_ports = get_available_com_ports()
    ui.com_select.addItems(com_ports)
    com5_index = ui.com_select.findText(DEFAULT_COM_PORT)
    if com5_index >= 0:
        ui.com_select.setCurrentIndex(com5_index)
    
    
    # Setup range profile plot
    view_rpl = ui.range_profile_view.addViewBox()
    view_rpl.setAspectLocked(False)
    plot_widget = pg.PlotItem(viewBox=view_rpl)
    
    # Configure range profile plot
    ui.range_profile_view.setCentralItem(plot_widget)
    plot_widget.setLabel('left', 'Magnitude', units='dB')
    plot_widget.setLabel('bottom', 'Range', units='m')
    plot_widget.showGrid(x=True, y=True)
    plot_rpl = plot_widget.plot(pen='y')
    
    update_time = ptime.time()

    # Load default config
    default_config = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 '..', 'config', 'IWR1843_cfg.cfg')
    if os.path.exists(default_config):
        ui.config_path.setText(os.path.basename(default_config))
        ui.config_path.setProperty("fullPath", default_config)
        radar_params = RadarParameters(default_config)
    
    # Connect buttons
    ui.browse_button.clicked.connect(browse_config)
    start_button.clicked.connect(initialize_radar)
    exit_button.clicked.connect(lambda: (cleanup(), app.quit(), sys.exit()))
    
    # Connect channel selection
    def on_channel_changed(button):
        if processor:
            channel_id = ui.channel_group.id(button)
            processor.set_channel(channel_id)
            logger.info(f"Selected channel changed to {channel_id}")
    
    ui.channel_group.buttonClicked.connect(on_channel_changed)
    
    app.instance().exec_()

def initialize_fpga() -> socket.socket:
    """Initialize FPGA with retry mechanism and proper error handling."""
    command_sequence = ['9', 'E', '3', 'B', '5', '6']
    
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            sock.bind(config_address)
        except OSError as e:
            logger.error(f"Failed to bind socket: {e}")
            # Cleanup existing sockets
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
        
        # Configure FPGA
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

# Initialize system
fpga_socket = initialize_fpga()

# Start data collection
collector = UdpListener('Listener', binary_data_queue, frame_length, data_address, BUFFER_SIZE)
processor = DataProcessor('Processor', radar_config, binary_data_queue,
                        range_doppler_queue, range_angle_queue, range_profile_queue,
                        selected_channel=0)  # Start with first channel
collector.start()
processor.start()

if __name__ == '__main__':
    try:
        initialize_gui()
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        cleanup()
        logger.info("Program closed")
        sys.exit()
