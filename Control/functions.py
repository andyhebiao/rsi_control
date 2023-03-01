# -*- utf-8 -*-
# @Time:  2023/3/1 16:01
# @Autor: Andy Ye
# @File:  functions.py
# @IDE: PyCharm
import multiprocessing as mp
from Gui.functions import *

def sliders_to_spinboxes(sliders, spinboxes):
    [spinbox.setValue(slider.value()) for (slider, spinbox) in zip(sliders, spinboxes)]


def limits_to_sliders_and_spinboxes(limits, sliders, spinboxes):
    [[sliders[i].setMinimum(limits[i * 2].value()), sliders[i].setMaximum(limits[i * 2 + 1].value()),
      spinboxes[i].setMinimum(limits[i * 2].value()), spinboxes[i].setMaximum(limits[i * 2 + 1].value())]
     for i in range(len(sliders))]


def start_control(self):
    print("start control")
    pass


def stop_control(self):
    print("stop control")
    pass


def terminate_control(self):
    print("terminate control")
    pass


def set_initial_pose(self, prompt_obj_callback=None):   # kuka initial pose
    lock = mp.Lock()
    with lock:
        self.ini_pose[:] = self.pre_pose[:]
    update_table(self.ini_pose, self.ui.table_ini_pose)
    self.ui.pb_start_cartesian_control.setEnabled(True)
    prompt_obj_callback(self.time_stamp + "\tThe initial pose is set")




# def start_axis_control(self):
#     pass
#
#
# def stop_axis_control(self):
#     pass
#
#
# def terminate_axis_control(self):
#     pass
#
#
# def set_initial_pose_axis(self, prompt_obj_callback=None):   # kuka initial pose
#     lock = mp.Lock()
#     with lock:
#         self.ini_pose[:] = self.pre_pose[:]
#     update_table(self.ini_pose, self.ui.table_ini_pose)
#     self.ui.pb_start_cartesian_control.setEnabled(True)
#     prompt_obj_callback(self.time_stamp + "\tThe initial pose is set")