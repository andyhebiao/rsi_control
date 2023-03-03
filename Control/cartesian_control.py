# -*- coding: UTF-8 -*-
__author__ = "yezhongyi"
__version__ = "2021.08.27"

import math
import time
# from communication import *
import numpy as np
from matplotlib.pyplot import plot, show, grid, legend
import multiprocessing as mp
from Control.control import *
from Control.constant import *
from Control.constant import *


class RsiCartesianControl(mp.Process):
    def __init__(self,  initial_pose, reference_pose, present_pose, control_vector,
                 pose_bounds,
                 acc_max=acceleration_max, v_max=velocity_max,  ome_max=cartesian_omega_max, alp_max=cartesian_alpha_max,
                 # omega: angular velocity  degree/s,  alpha: angular acceleration degree/s^2
                 v_factor=velocity_factor, ome_factor=cartesian_omega_factor):
        super().__init__(daemon=True)
        # motion limits
        self.pose_bounds = pose_bounds[:]  # in order of  x y z a b c
        self.acc_max = acc_max
        self.v_max = v_max
        self.ome_max = ome_max
        self.alp_max = alp_max
        lock = mp.Lock()
        self.v_factor = v_factor  # 1 entspricht  0.25 m/s
        self.ome_factor = ome_factor
        self.ini_pose = initial_pose[:]
        self.pre_pose = present_pose
        self.ref_pose = reference_pose
        self.control_vector = control_vector
        # self.pose_bounds = [[self.pose_limits[i * 2] + self.ini_pose[i], self.pose_limits[i * 2 + 1] + self.ini_pose[i]]
        #                     for i in range(6)]
        # print("cartesian bounds:", self.pose_bounds)
        # print([(self.pose_bounds[i][0], self.pose_bounds[i][1]) for i in range(6)])

    def run(self):
        axes_tfs = [  # translational mSimpleTransferFunctionotion control
                       {'p3': SimpleTransferFunction([1, 1], [1, 1]),  # prefilter 3
                        'p2': SimpleTransferFunction([1, 1], [1, 1]),  # prefilter 2
                        'p1': SimpleTransferFunction([1, 1], [3, 1]),  # prefilter 1
                        'c': SimpleTransferFunction([3, 1], [1, 3]),  # controller
                        'i': SimpleTransferFunction([0, 1], [1, 0],  # integrator
                                                    output_min=-self.v_max, output_max=self.v_max)}
                      for i in range(3)] + \
                   [  # rotational motion control
                       {'p3': SimpleTransferFunction([1, 1], [0.5, 1]),  # prefilter 3
                        'p2': SimpleTransferFunction([1, 1], [0.5, 1]),  # prefilter 2
                        'p1': SimpleTransferFunction([1, 1], [3, 1]),  # prefilter 1
                        'c': SimpleTransferFunction([3, 1], [1, 3]),  # controller
                        'i': SimpleTransferFunction([0, 1], [1, 0],  # integrator
                                                    output_min=-self.ome_max, output_max=self.ome_max)}
                    for i in range(3)]
        print('start control Unit')
        lock = mp.Lock()  # resource lock for access the shared variables
        while True:
            with lock:
                pre_pose = self.pre_pose[:]
                ref_pose = self.ref_pose[:]  # robot present position, unit in m
            ref_pose = [saturate(ref_pose[i], self.pose_bounds[i][0], self.pose_bounds[i][1]) for i in range(6)]
            control_vector = [axes_tfs[i]['i'].tf(
                axes_tfs[i]['c'].tf(
                    axes_tfs[i]["p3"].tf(axes_tfs[i]['p2'].tf(axes_tfs[i]['p1'].tf(ref_pose[i]))) - pre_pose[i]))
                for i in range(3)] + \
                [axes_tfs[i]['i'].tf(
                    axes_tfs[i]['c'].tf(axes_tfs[i]['p2'].tf(axes_tfs[i]['p1'].tf(ref_pose[i])) - pre_pose[i]))
                 for i in range(3, 6)]  # xyz in m/s  and  abc in deg/s
            control_vector[0:3] = [ele / self.v_factor for ele in control_vector[0:3]]
            control_vector[3:6] = [ele / self.ome_factor for ele in control_vector[3:6]]
            with lock:
                self.control_vector[:] = control_vector[:]       # in percentage
            time.sleep(0.001)


if __name__ == "__main__":
    # enable_ctl = mp.Value("i", 1)
    # control_mode = "xyz"
    # ini_pose = [0.54, 0.0, 0.895, 180.0, -0.0, 180.0]
    # # pre_pose = mp.Array('f', [0, 0, 0, 0, 0, 0])  # present position
    # pre_pose = mp.Array('f', [0, 0, 0, 0, 0, 0])  # present position
    # ref_disp = mp.Array('f', [0, 0, 0, 0, 0, 0])  # reference pose
    # motion_vec = mp.Array('f', [0, 0, 0, 0, 0, 0])  # motion vector
    # string = "<Rob Type=\"KUKA\"><RIst X=\"540.0\" Y=\"0.0\" Z=\"895.0\" A=\"-180.0\" B=\"0.0\" C=\"-180.0\"/>" \
    #          "<RSol X=\"540.0\" Y=\"0.0\" Z=\"895.0\" A=\"180.0\" B=\"0.0\" C=\"180.0\"/><Delay D=\"100\"/>" \
    #          "<Tech C11=\"0.0\" C12=\"0.0\" C13=\"0.0\" C14=\"0.0\" C15=\"0.0\" C16=\"0.0\"  " \
    #          "C17=\"0.0\" C18=\"0.0\" C19=\"0.0\" C110=\"0.0\"/><DiL>0</DiL><Digout o1=\"0\" o2=\"0\" o3=\"0\"/>" \
    #          "<Source1>3.5</Source1><IPOC>6580928</IPOC></Rob>"
    # kuka_msg = mp.Array("c", ("empty" + "\0" * 500).encode("utf-8"))  # for info share   # mp shared
    # kuka_msg[:len(string)] = string.encode("utf-8")
    #
    # rsi_control = RsiMotionControl(enable_ctl, control_mode, kuka_msg, ini_pose, ref_disp, motion_vec)
    # rsi_control.run()
    # rsi_control.join()
    kuka_pose_limits = (-0.18, 0.18, -0.18, 0.18, -0.18, 0.18, -18.0, 18.0, -18.0, 18.0, -18.0, 18.0)
    acceleration_max = 0.5
    velocity_max = 0.025
    omega_max = 14.0
    alpha_max = 14.0
    velocity_factor = 0.25
    omega_factor = 144.0



