# -*- utf-8 -*-
# @Time:  2023/3/1 0:31
# @Autor: Andy Ye
# @File:  ini.py
# @IDE: PyCharm
import multiprocessing as mp
from Control.functions import *


def init(self):
    # parameters
    # self.ini_pose = [None] * 6
    self.ref_pose = mp.Array('f', [0, 0, 0, 0, 0, 0])  # reference pose
    # self.poses = [self.ini_pose, self.ref_pose, self.pre_pose, self.control_vec]
    self.control_process = None
    # signals
    self.ui.pb_start_control.clicked.connect(lambda: start_control(self))
    self.ui.pb_end_control.clicked.connect(lambda: stop_control(self))
    self.ui.pb_terminate_control.clicked.connect(lambda: terminate_control(self))
    self.ui_timer.timeout.connect(lambda: update_control_states(self))
    # ui
    # self.ui.pb_start_control.setDisabled(True)
    self.ui.pb_end_control.setDisabled(True)
    self.ui.pb_terminate_control.setDisabled(True)


# cartesian control

    self.ds_limits_cartesian = [[self.ui.ds_min_x, self.ui.ds_max_x], [self.ui.ds_min_y, self.ui.ds_max_y],
                                [self.ui.ds_min_z, self.ui.ds_max_z], [self.ui.ds_min_a, self.ui.ds_max_a],
                                [self.ui.ds_min_b, self.ui.ds_max_b], [self.ui.ds_min_c, self.ui.ds_max_c]]
    self.tw_pose_tables_cartesian = [self.ui.tw_pre_pose_cartesian,
                                     self.ui.tw_ref_pose_cartesian, self.ui.tw_control_vector_cartesian]
    self.hs_hand_cartesian = [self.ui.hs_hand_x, self.ui.hs_hand_y, self.ui.hs_hand_z,
                              self.ui.hs_hand_a, self.ui.hs_hand_b, self.ui.hs_hand_c]
    self.ds_hand_cartesian = [self.ui.ds_hand_x, self.ui.ds_hand_y, self.ui.ds_hand_z, self.ui.ds_hand_a,
                              self.ui.ds_hand_b, self.ui.ds_hand_c]

    self.parameter_sections_dict["cartesian_control"] = \
        {"min_x": self.ui.ds_min_x.value,
         "max_x": self.ui.ds_max_x.value,
         "min_y": self.ui.ds_min_y.value,
         "max_y": self.ui.ds_max_y.value,
         "min_z": self.ui.ds_min_z.value,
         "max_z": self.ui.ds_max_z.value,
         "min_a": self.ui.ds_min_a.value,
         "max_a": self.ui.ds_max_a.value,
         "min_b": self.ui.ds_min_b.value,
         "max_b": self.ui.ds_max_b.value,
         "min_c": self.ui.ds_min_c.value,
         "max_c": self.ui.ds_max_c.value,
         "max_acc_cartesian": self.ui.ds_max_acc_cartesian.value,
         "max_v_cartesian": self.ui.ds_max_v_cartesian.value,
         "max_omega_cartesian": self.ui.ds_max_omega_cartesian.value,
         "max_alpha_cartesian": self.ui.ds_max_alpha_cartesian.value,
         "velocity_factor_cartesian": self.ui.ds_velocity_factor_cartesian.value,
         "omega_factor_cartesian": self.ui.ds_omega_factor_cartesian.value,
         }
    # signal:
    [[limit.valueChanged.connect(
        lambda: limits_to_sliders_and_spinboxes(self.ini_pose, self.ds_limits_cartesian, self.hs_hand_cartesian,
                                                self.ds_hand_cartesian)) for limit in limit_group]
     for limit_group in self.ds_limits_cartesian]
    [slider.valueChanged.connect(lambda: sliders_to_spinboxes(self.hs_hand_cartesian, self.ds_hand_cartesian))
     for slider in self.hs_hand_cartesian]

    # ui
    # limits_to_sliders_and_spinboxes(self.ds_limits_cartesian, self.hs_hand_cartesian, self.ds_hand_cartesian)


# axis control
    # parameters:
    self.tw_pose_tables_axis = [self.ui.tw_pre_pose_axis,
                                self.ui.tw_ref_pose_axis, self.ui.tw_control_vector_axis]
    self.ds_limits_axis = [[self.ui.ds_min_a1, self.ui.ds_max_a1], [self.ui.ds_min_a2, self.ui.ds_max_a2],
                           [self.ui.ds_min_a3, self.ui.ds_max_a3], [self.ui.ds_min_a4, self.ui.ds_max_a4],
                           [self.ui.ds_min_a5, self.ui.ds_max_a5], [self.ui.ds_min_a6, self.ui.ds_max_a6]]
    self.hs_hand_axis = [self.ui.hs_hand_a1, self.ui.hs_hand_a2, self.ui.hs_hand_a3,
                         self.ui.hs_hand_a4, self.ui.hs_hand_a5, self.ui.hs_hand_a6]
    self.ds_hand_axis = [self.ui.ds_hand_a1, self.ui.ds_hand_a2, self.ui.ds_hand_a3,
                         self.ui.ds_hand_a4, self.ui.ds_hand_a5, self.ui.ds_hand_a6]
    self.parameter_sections_dict["axis_control"] = \
        {"min_a1": self.ui.ds_min_a1.value,
         "max_a1": self.ui.ds_max_a1.value,
         "min_a2": self.ui.ds_min_a2.value,
         "max_a2": self.ui.ds_max_a2.value,
         "min_a3": self.ui.ds_min_a3.value,
         "max_a3": self.ui.ds_max_a3.value,
         "min_a4": self.ui.ds_min_a4.value,
         "max_a4": self.ui.ds_max_a4.value,
         "min_a5": self.ui.ds_min_a5.value,
         "max_a5": self.ui.ds_max_a5.value,
         "min_a6": self.ui.ds_min_a6.value,
         "max_a6": self.ui.ds_max_a6.value,
         "max_omega_axis": self.ui.ds_max_omega_axis.value,
         "max_alpha__axis": self.ui.ds_max_alpha_axis.value,
         "omega_factor_axis": self.ui.ds_omega_factor_axis.value,
         }

    # signal:
    [[limit.valueChanged.connect(
        lambda: limits_to_sliders_and_spinboxes(self.ini_pose, self.ds_limits_axis, self.hs_hand_axis,
                                                self.ds_hand_axis)) for limit in limit_group]
     for limit_group in self.ds_limits_axis]
    [slider.valueChanged.connect(lambda: sliders_to_spinboxes(self.hs_hand_axis, self.ds_hand_axis))
     for slider in self.hs_hand_axis]

    # ui:
    # limits_to_sliders_and_spinboxes(self.limits_axis, self.hs_hand_axis, self.ds_hand_axis)

