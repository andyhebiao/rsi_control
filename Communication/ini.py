# -*- coding: UTF-8 -*-
# @Time: 2022/7/5 22:17
# @Author: Andy Ye
# @File: .py
from Communication.functions import *
import os


def init(self):
    # communication arguments
    self.com_state = mp.Value("i", 0)  # mp shared
    self.kuka_msg = mp.Array("c", ("empty" + "\0" * 500).encode("utf-8"))  # for info share   # mp shared
    self.pre_pose = mp.Array('f', [0, 0, 0, 0, 0] * 6)  # present position
    self.ini_pose = [None] * 6
    self.if_got_ini_pose = False
    #  in cartesian mode its 1 = 100%  = 250 mm/s or   144 degree/s
    #  in axis mode ?
    self.control_vector = mp.Array('f', [0, 0, 0, 0, 0, 0])
    self.rsi_com = None
    self.com_process = None
    self.all_tabs = [self.ui.tab_control, self.ui.tab_cartesian_control, self.ui.tab_axis_control, self.ui.tab_kinectv2,
                     self.ui.tab_realsense, self.ui.tab_webcam, self.ui.tab_touchdesigner, self.ui.tab_grasshopper,
                     self.ui.tab_unity]
    self.cartesian_control_tabs = [self.ui.tab_control, self.ui.tab_cartesian_control, self.ui.tab_kinectv2,
                                   self.ui.tab_realsense, self.ui.tab_webcam, self.ui.tab_touchdesigner]
    self.axis_control_tabs = [self.ui.tab_control, self.ui.tab_axis_control, self.ui.tab_grasshopper, self.ui.tab_unity]
    self.parameter_sections_dict["rsi_communication"] \
        = {"rsi_server_ip": self.ui.le_rsi_server_ip.text,
           "rsi_server_port": self.ui.sb_rsi_server_port.value,
           "rsi_server_mask": self.ui.le_rsi_server_mask.text,
           "rsi_net_adapter": self.ui.le_rsi_net_adapter.text,
           "rsi_mode": self.ui.combo_control_mode.currentText}

    # communication signals
    self.ui.pb_start_rsi_com.clicked.connect(lambda: start_rsi_com(self))
    self.ui.pb_stop_rsi_com.clicked.connect(lambda: stop_rsi_com(self))
    self.ui.pb_set_static_ip.clicked.connect(lambda: set_static_ip(self))
    self.ui.pb_set_dhcp.clicked.connect(lambda: set_dhcp(self))
    self.ui.pb_load_rsi_com_config.clicked.connect(lambda: load_config(self))
    self.ui.pb_export_rsi_com_config.clicked.connect(lambda: export_config_file(self))

    # ui
    load_config(self, os.path.abspath("./config_files/kuka__kr10.cfg"))
    self.ui.pb_stop_rsi_com.setDisabled(True)
    [tab.setDisabled(True) for tab in self.all_tabs]
