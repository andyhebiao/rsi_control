# -*- utf-8 -*-
# @Time:  2023/2/27 19:38
# @Autor: Andy Ye
# @File:  main.py
# @IDE: PyCharm

__author__ = "Andy Ye"
__version__ = "2023.02.27"

import sys
sys.path.append(r"D:\projects\cv")

# import numpy as np

# from cv2 import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow
#import control
import Communication.ini as com_ini
import Control.ini as ctrl_ini
from Gui.RsiGui import *
import Gui.ini as gui_ini
import sys

# import threading as td
# import guiutils as gu
# from ComupterVision.kinvectv2 import *
# from ComupterVision.kinect_const import *
# import vision_uitils as vu
# import touch_designer
# from td_utils import *
# import print.print_utils as pu
# import realsense as rs

# from PyQt5.QtGui import QPixmap


class RsiApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.parameter_sections_dict = {}
        gui_ini.init(self)
        com_ini.init(self)
        ctrl_ini.init(self)

        # self.ui.ds_min_x.setDisabled()
        # self.ui.tab_cartesian_control.setDisabled(True)
        # print(self.ui.hs_hand_a1)
        # self.ui.hs_hand_a1.valueChanged.connect(lambda: self.ui.ds_hand_a1.setValue(self.ui.hs_hand_a1.value()))
        # self.ui.ds_min_x.valueChanged.connect(lambda: self.ui.ds_max_x.setValue(self.))
        # self.ui.hs_hand_x.setMaximum()
        # self.ui.hs_hand_x.setMinimum()


        # self.ui.hs_front_limit.valueChanged.connect(self.cut_depth)
        # self.ui.hs_rear_limit.valueChanged.connect(self.cut_depth)



#     def set_static_ip(self):
#         com_func.set_static_ip(self)
#
#     def set_dhcp(self):
#         com_func.set_dhcp(self.rsi_net_adapter)
#
#     def load_rsi_com_config(self):
#         gu.load_config_file(self, "rsi_communication")
#
#     def export_rsi_com_config(self):
#         rc.export_rsi_com_config(self)
#
#     def start_rsi_com(self):
#         rc.start_rsi_com(self)
#
#     def stop_rsi_com(self):
#         rc.stop_rsi_com(self)
#
# # slots of control
#     def load_control_args(self):  # todo
#         control.load_control_args(self)
#
#     def set_control_args(self):
#         control.set_control_args(self)
#
#     def export_control_args(self):  # todo
#         control.export_control_args(self)
#
#     def set_control_signal(self):
#         control.set_control_signal(self)
#
#     def set_initial_pose(self):   # kuka initial pose
#         control.set_initial_pose(self)
#
#     def start_control(self):
#         control.start_control(self)
#
#     def end_control(self):
#         control.end_control(self)
#
#     def terminate_control(self):
#         control.terminate_control(self)
#
#     def move_initial_pose(self):
#         control.move_initial_pose(self)
#
#     def set_home_pose(self):
#         control.set_home_pose(self)
#
#     def homing(self):
#         control.homing(self)
#
#     def slider_to_spinbox(self):
#         [ds.setValue(slider.value()) for (ds, slider) in zip(self.hand_dses, self.hand_sliders)]
#
#     def hand_move(self):
#         control.hand_move(self)
#
#     def set_hand_zero(self):
#         control.set_hand_zero(self)
#
#     def start_kinectv2(self):
#         vu.start_kinectv2(self)
#
#     def stop_kinvectv2(self):
#         vu.stop_kinvectv2(self)
#
#     def initialise_joint_poses(self):
#         vu.initialise_joint_poses(self)
#
#     def start_joint_control(self):
#         vu.start_joint_control(self)
#
#     def stop_joint_control(self):
#         vu.stop_kinvectv2(self)
#
#     def cut_depth(self):
#         self.ui.ds_front_limit.setValue(self.ui.hs_front_limit.value())
#         self.front_limit = self.ui.ds_front_limit.value()
#         self.ui.ds_rear_limit.setValue(self.ui.hs_rear_limit.value())
#         self.rear_limit = self.ui.ds_rear_limit.value()
#
#     def start_td_com(self):
#         touch_designer.start_td_com(self)
#
#     def stop_td_com(self):
#         touch_designer.stop_td_com(self)
#
#     def start_td_control(self):
#         touch_designer.start_td_control(self)
#
#     def stop_td_control(self):
#         touch_designer.stop_td_control(self)
#
#     def load_print_parameters(self):
#         pu.load_print_parameters(self, self.ui.tw_sb_frame, self.ui.tw_tool_parameter,
#                                  self.ui.tw_start_end_position)
#
#     def set_print_parameters(self):
#         pu.set_print_parameters(self, self.ui.tw_sb_frame, self.ui.tw_tool_parameter,
#                                 self.ui.tw_start_end_position)
#
#     def export_print_parameters(self):
#         pu.export_print_parameters(self, self.ui.tw_tool_parameter, self.ui.tw_start_end_position)
#
#     def load_print_trajectory(self):
#         pu.load_print_trajectory(self)
#
#     def export_krl_scripts(self):
#         pu.export_krl_scripts(self, self.krl_mode)
#
#     def set_print_speed(self):
#         pu.set_print_speed(self)
#
#     def start_realsense(self):
#         rs.start_realsense(self)
#
#     def stop_realsense(self):
#         rs.stop_realsense(self)
#
#     def start_hand_wave(self):
#         rs.start_hand_wave(self)
#
#     def stop_hand_wave(self):
#         rs.stop_hand_wave(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RsiApp()
    window.show()
    sys.exit(app.exec_())
