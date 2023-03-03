# -*- coding: UTF-8 -*-
__author__ = "yezhongyi"
__version__ = "2021.08.27"

import math
import time
# from communication import *
import numpy as np
from matplotlib.pyplot import plot, show, grid, legend
import multiprocessing as mp
from Control.constant import *
from Control.control import *


class RsiAxisControl(mp.Process):
    def __init__(self,  initial_pose, reference_pose, present_pose, control_vector, pose_bounds, ome_max=axis_omega_max,
                 alp_max=axis_alpha_max, ome_factor=axis_omega_factor, daemon=True):
                 # omega: angular velocity  degree/s,  alpha: angular acceleration degree/s^2

        super().__init__(daemon=daemon)
        # motion limits
        # self.lock = mp.Lock()
        self.pose_bounds = pose_bounds
        self.ome_max = ome_max
        self.alp_max = alp_max
        self.ome_factor = ome_factor
        self.pre_pose = present_pose
        self.ref_pose = reference_pose
        self.control_vector = control_vector
        self.ini_pose = initial_pose[:]

    def run(self):
        axes_tfs = [  # axis SimpleTransfer Function
            # control
                       {'p3': SimpleTransferFunction([1, 1], [1, 1]),  # prefilter 3
                        'p2': SimpleTransferFunction([1, 1], [1, 1]),  # prefilter 2
                        'p1': SimpleTransferFunction([1, 1], [3, 1]),  # prefilter 1
                        'c': SimpleTransferFunction([3, 1], [1, 3]),  # controller
                        'i': SimpleTransferFunction([0, 1], [1, 0],  # integrator
                                                    output_min=-self.ome_max, output_max=self.ome_max)}
                      for i in range(6)]
        lock = mp.Lock()  # resource lock for access the shared variables
        while True:
            with lock:
                pre_pose = self.pre_pose[:]
                ref_pose = self.ref_pose[:]  # robot present position, unit in m
            ref_pose = [saturate(ref_pose[i], self.pose_bounds[i][0], self.pose_bounds[i][1]) for i in range(6)]

            control_vector = [axes_tfs[i]['i'].tf(
                axes_tfs[i]['c'].tf(
                    axes_tfs[i]["p3"].tf(axes_tfs[i]['p2'].tf(axes_tfs[i]['p1'].tf(ref_pose[i]))) - pre_pose[i]))
                for i in range(6)]
            control_vector = [value / self.ome_factor for value in control_vector]
            with lock:
                self.control_vector[:] = control_vector[:]       # in percentage
            time.sleep(0.001)


if __name__ == "__main__":
    ini_pose = ref_pose = pre_pose = control_vec = [10] * 6
    axis_offset_limits = (-10, 20, -30, 40, -50, 60, -70, 80, -90, 100, -110, 120)
    # ctrl = RsiAxisControl(ini_pose, ref_pose, pre_pose, control_vec)


