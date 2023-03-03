# -*- utf-8 -*-
# @Time:  2023/3/1 16:01
# @Autor: Andy Ye
# @File:  functions.py
# @IDE: PyCharm
import multiprocessing as mp
from Gui.functions import *
import time
from Control.axis_control import *
from Control.cartesian_control import *


def update_control_states(self):
    control_mode = self.ui.combo_control_mode.currentText()
    update_table(self.pre_pose, self.ui.tw_pre_pose_cartesian if control_mode == "Cartesian" else self.ui.tw_pre_pose_axis)
    update_table(self.ref_pose, self.ui.tw_ref_pose_cartesian if control_mode == "Cartesian" else self.ui.tw_ref_pose_axis)
    update_table(self.control_vector, self.ui.tw_control_vector_cartesian if control_mode == "Cartesian" else self.ui.tw_control_vector_axis)


def sliders_to_spinboxes(sliders, spinboxes):
    [spinbox.setValue(slider.value()) for (slider, spinbox) in zip(sliders, spinboxes)]


def limits_to_sliders_and_spinboxes(initial_pose, limits, sliders, spinboxes):
    lock = mp.Lock()
    with lock:
        ini_pose = initial_pose[:]
    bounds = \
        [[sliders[i].setMinimum(limits[i][0].value() + ini_pose[i]),
          sliders[i].setMaximum(limits[i][1].value() + ini_pose[i]),
          spinboxes[i].setMinimum(limits[i][0].value() + ini_pose[i]),
          spinboxes[i].setMaximum(limits[i][1].value()) + ini_pose[i]]
         for i in range(6)]
    print("bounds", bounds)


# def set_initial_pose(self, prompt_obj_callback=None):   # kuka initial pose
#     lock = mp.Lock()
#     with lock:
#         self.ini_pose[:] = self.pre_pose[:]
#     update_table(self.ini_pose, self.ui.table_ini_pose)
#     self.ui.pb_start_cartesian_control.setEnabled(True)
#     prompt_obj_callback(self.time_stamp + "\tThe initial pose is set")


def velocity_ramp(control_vector, tangent=0.01):
    lock = mp.Lock()
    with lock:
        local_control_vector = control_vector[:]
    while True:
        local_control_vector = [value - tangent if abs(value) > 0.1 else value for value in local_control_vector]
        if all([abs(value) < 0.05 for value in control_vector]):
            break
        control_vector[:] = local_control_vector[:]
        time.sleep(0.1)


def start_control(self):
    if self.control_process is not None:
        self.show_info(time.asctime() + "\tThe control process is already started!")
    elif not self.if_got_ini_pose:
        self.show_info(time.asctime() + "\tThe initial pose is not set! Check the Communication")
    else:
        control_mode = self.ui.combo_control_mode.currentText()
        if control_mode == "Cartesian":
            pose_limits = [[ds.value() for ds in group] for group in self.ds_limits_cartesian]
            pose_bounds = [[pose_limits[i * 2] + self.ini_pose[i], pose_limits[i * 2 + 1] + self.ini_pose[i]]
                           for i in range(6)]
            self.rsi_position_control = RsiCartesianControl(self.ref_pose, self.pre_pose, self.control_vec,
                                                            pose_bounds=pose_bounds,
                                                            ome_max=self.ui.ds_max_omega_axis.value(),
                                                            alp_max=self.ui.ds_max_alpha_axis.value(),
                                                            ome_factor=self.ui.ds_omega_factor_axis.value())
        else:
            pose_limits = [[ds.value() for ds in group] for group in self.ds_limits_axis]
            pose_bounds = [[pose_limits[i * 2] + self.ini_pose[i], pose_limits[i * 2 + 1] + self.ini_pose[i]]
                           for i in range(6)]
            self.rsi_position_control = RsiAxisControl(self.ref_pose, self.pre_pose, self.control_vec,
                                                       pose_bounds=pose_bounds,
                                                       ome_max=self.ui.ds_max_omega_axis.value(),
                                                       alp_max=self.ui.ds_max_alpha_axis.value(),
                                                       ome_factor=self.ui.ds_omega_factor_axis.value())
        self.rsi_position_control.start()
        self.ui.pb_end_control.setEnabled(True)
        self.ui.pb_move_ini_pose.setEnabled(True)
        self.ui.pb_start_control.setDisabled(True)
        self.show_info(
            time.asctime() + "\tThe" + self.ui.combo_control_mode.currentText() + "control process is started!")


def stop_control(self):
    if self.control_process is not None:
        self.control_process.terminate()
        self.control_process.close()
        mp.Process(target=velocity_ramp, args=(self.control_vector,)).start()
        self.control_process = None
        self.ui.pb_end_control.setEnabled(False)
        self.ui.pb_move_ini_pose.setEnabled(False)
        self.ui.pb_start_control.setEnabled(True)
        self.show_info(time.asctime() + "\tThe" + self.ui.combo_control_mode.currentText() + "control process is ended!")
    else:
        self.show_info(time.asctime() + "\tThe control process is not started!")


def terminate_control(self):
    if self.control_process is not None:
        self.control_process.terminate()
        self.control_process.close()
        self.control_vector[:] = [0, 0, 0, 0, 0, 0]
        self.control_process = None
        self.ui.pb_end_control.setEnabled(False)
        self.ui.pb_move_ini_pose.setEnabled(False)
        self.ui.pb_start_control.setEnabled(True)
        self.show_info(time.asctime() + "\tThe" + self.ui.combo_control_mode.currentText() + "control process is terminated!")
    else:
        self.show_info(time.asctime() + "\tThe control process is not started!")


def move_ini_pose(self):
    if self.control_process is not None:
        lock = mp.Lock()
        with lock:
            self.ref_pose[:] = self.ini_pose[:]
        self.show_info(time.asctime() + "\tmoving to initial pose.")
    else:
        self.show_info(time.asctime() + "\tThe control process is not started!")
