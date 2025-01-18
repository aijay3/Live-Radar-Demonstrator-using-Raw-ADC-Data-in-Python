# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import GraphicsLayoutWidget

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1000)
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Configure fonts
        button_font = QtGui.QFont()
        button_font.setFamily("微軟正黑體 Light")
        button_font.setBold(True)
        button_font.setWeight(75)
        
        title_font = QtGui.QFont()
        title_font.setFamily("微軟正黑體 Light")
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_font.setWeight(75)
        
        # COM Port selection
        self.com_port_label = QtWidgets.QLabel(self.centralwidget)
        self.com_port_label.setGeometry(QtCore.QRect(30, 20, 100, 31))
        self.com_port_label.setFont(button_font)
        self.com_port_label.setObjectName("com_port_label")
        
        self.com_select = QtWidgets.QComboBox(self.centralwidget)
        self.com_select.setGeometry(QtCore.QRect(140, 20, 120, 31))
        self.com_select.setFont(button_font)
        self.com_select.setObjectName("com_select")
        
        # Config file selection
        self.config_label = QtWidgets.QLabel(self.centralwidget)
        self.config_label.setGeometry(QtCore.QRect(280, 20, 100, 31))
        self.config_label.setFont(button_font)
        self.config_label.setObjectName("config_label")
        
        self.config_path = QtWidgets.QLineEdit(self.centralwidget)
        self.config_path.setGeometry(QtCore.QRect(390, 20, 250, 31))
        self.config_path.setFont(button_font)
        self.config_path.setObjectName("config_path")
        self.config_path.setReadOnly(True)
        
        # Control buttons
        self.browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_button.setGeometry(QtCore.QRect(660, 20, 120, 31))
        self.browse_button.setFont(button_font)
        self.browse_button.setObjectName("browse_button")
        
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(800, 20, 180, 31))
        self.start_button.setFont(button_font)
        self.start_button.setObjectName("start_button")
        
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(1780, 20, 110, 31))
        self.exit_button.setFont(button_font)
        self.exit_button.setObjectName("exit_button")
        
        # Channel selection
        self.channel_group = QtWidgets.QButtonGroup(self.centralwidget)
        self.channel_group.setExclusive(True)
        
        # Create channel radio buttons
        self.channel_label = QtWidgets.QLabel(self.centralwidget)
        self.channel_label.setGeometry(QtCore.QRect(1000, 20, 100, 31))
        self.channel_label.setFont(button_font)
        self.channel_label.setObjectName("channel_label")
        
        for i in range(4):  # Assuming 4 RX channels
            channel_btn = QtWidgets.QRadioButton(self.centralwidget)
            channel_btn.setGeometry(QtCore.QRect(1100 + i*70, 20, 60, 31))
            channel_btn.setFont(button_font)
            channel_btn.setObjectName(f"channel_{i+1}")
            self.channel_group.addButton(channel_btn, i)
            setattr(self, f"channel_{i+1}", channel_btn)
        
        # Select first channel by default
        self.channel_1.setChecked(True)
        
        # Visualization views
        # Range Profile
        self.range_profile_view = GraphicsLayoutWidget(self.centralwidget)
        self.range_profile_view.setGeometry(QtCore.QRect(30, 100, 710, 350))
        self.range_profile_view.setObjectName("range_profile_view")
        
        # Range-Doppler Image
        self.range_doppler_view = GraphicsLayoutWidget(self.centralwidget)
        self.range_doppler_view.setGeometry(QtCore.QRect(30, 500, 710, 450))
        self.range_doppler_view.setObjectName("range_doppler_view")
        
        # Range-Angle Image
        self.range_angle_view = GraphicsLayoutWidget(self.centralwidget)
        self.range_angle_view.setGeometry(QtCore.QRect(770, 500, 710, 450))
        self.range_angle_view.setObjectName("range_angle_view")
        
        # Blank Space (Previously Multi-channel View)
        self.blank_space_view = GraphicsLayoutWidget(self.centralwidget)
        self.blank_space_view.setGeometry(QtCore.QRect(770, 100, 710, 350))
        self.blank_space_view.setObjectName("blank_space_view")
        
        # Target ranges display
        self.target_display = QtWidgets.QTextBrowser(self.centralwidget)
        self.target_display.setGeometry(QtCore.QRect(1510, 80, 380, 830))
        self.target_display.setFont(button_font)
        self.target_display.setObjectName("target_display")
        
        # Plot titles
        self.range_profile_label = QtWidgets.QLabel(self.centralwidget)
        self.range_profile_label.setGeometry(QtCore.QRect(280, 60, 211, 31))
        self.range_profile_label.setFont(title_font)
        self.range_profile_label.setAlignment(QtCore.Qt.AlignCenter)
        self.range_profile_label.setObjectName("range_profile_label")
        
        self.detected_points_label = QtWidgets.QLabel(self.centralwidget)
        self.detected_points_label.setGeometry(QtCore.QRect(1020, 60, 211, 31))
        self.detected_points_label.setFont(title_font)
        self.detected_points_label.setAlignment(QtCore.Qt.AlignCenter)
        self.detected_points_label.setObjectName("detected_points_label")
        
        self.range_doppler_label = QtWidgets.QLabel(self.centralwidget)
        self.range_doppler_label.setGeometry(QtCore.QRect(280, 460, 211, 31))
        self.range_doppler_label.setFont(title_font)
        self.range_doppler_label.setAlignment(QtCore.Qt.AlignCenter)
        self.range_doppler_label.setObjectName("range_doppler_label")
        
        self.range_angle_label = QtWidgets.QLabel(self.centralwidget)
        self.range_angle_label.setGeometry(QtCore.QRect(1020, 460, 211, 31))
        self.range_angle_label.setFont(title_font)
        self.range_angle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.range_angle_label.setObjectName("range_angle_label")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Real-Time Radar"))
        self.range_doppler_label.setText(_translate("MainWindow", "Range-Doppler Image"))
        self.range_angle_label.setText(_translate("MainWindow", "Range-Angle Image"))
        self.range_profile_label.setText(_translate("MainWindow", "Range Profile"))
        self.detected_points_label.setText(_translate("MainWindow", "Detected Points"))
        self.com_port_label.setText(_translate("MainWindow", "COM Port:"))
        self.config_label.setText(_translate("MainWindow", "Config File:"))
        self.browse_button.setText(_translate("MainWindow", "Browse"))
        self.start_button.setText(_translate("MainWindow", "Send Radar Config"))
        self.exit_button.setText(_translate("MainWindow", "Exit"))
        self.channel_label.setText(_translate("MainWindow", "Channel:"))
        self.channel_1.setText(_translate("MainWindow", "CH1"))
        self.channel_2.setText(_translate("MainWindow", "CH2"))
        self.channel_3.setText(_translate("MainWindow", "CH3"))
        self.channel_4.setText(_translate("MainWindow", "CH4"))
