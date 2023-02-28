# -*- coding: UTF-8 -*-
__author__ = "yezhongyi"
__version__ = "2021.08.27"

import math
import time
# from communication import *
import numpy as np
from matplotlib.pyplot import plot, show, grid, legend
import multiprocessing as mp
import threading as td
import guiutils as gu
from Communication import rsi_com_cartesian as rc

# x, y, z, a, b, c
kuka_pose_limits = (-0.18, 0.18, -0.18, 0.18, -0.18, 0.18, -18.0, 18.0, -18.0, 18.0, -18.0, 18.0)
acceleration_max = 0.5
velocity_max = 0.025
omega_max = 14.0
alpha_max = 14.0
velocity_factor = 0.25
omega_factor = 144.0


def saturate(original, low_limit, up_limit):
    assert low_limit < up_limit, "Limits order wrong"
    original = original if original < up_limit else up_limit
    original = original if original > low_limit else low_limit
    return original


def load_control_args(self):
    gu.load_config_file(self, "control", show_info_callback=self.ui.te_control_info.appendPlainText)
    self.pose_limits = [self.min_x, self.max_x, self.min_y, self.max_y, self.min_z, self.max_z,
                        self.min_a, self.max_a, self.min_b, self.max_b, self.min_c, self.max_c]


def set_control_args(self):
    # x y z a b c
    self.pose_limits = [ds.value() for ds in self.pose_limits_ds[0:12]]  # \
    self.max_acc = self.ui.ds_max_acc.value()  # m/s^2   / 1000  # change into m # not used yet
    self.max_v = self.ui.ds_max_v.value()  # m/s     / 1000  # change into m
    self.max_alpha = self.ui.ds_max_alpha.value()
    self.max_omega = self.ui.ds_max_omega.value()
    self.velocity_factor = self.ui.ds_velocity_factor.value()
    self.omega_factor = self.ui.ds_omega_factor.value()
    self.ui.te_control_info.appendPlainText(self.time_stamp + "\tThe control parameters are set")


def export_control_args(self):
    parameter_dict = {"min_x": self.min_x,
                      "max_x": self.max_x,
                      "min_y": self.min_y,
                      "max_y": self.max_y,
                      "min_z": self.min_z,
                      "max_z": self.max_z,
                      "min_a": self.min_a,
                      "max_a": self.max_a,
                      "min_b": self.min_b,
                      "max_b": self.max_b,
                      "min_c": self.min_c,
                      "max_c": self.max_c,
                      "max_acc": self.max_acc,
                      "max_v": self.max_v,
                      "max_omega": self.max_omega,
                      "max_alpha": self.max_alpha,
                      "velocity_factor": self.velocity_factor,
                      "omega_factor": self.omega_factor}
    gu.export_config_file(self, "control", parameter_dict, show_info_callback=self.ui.te_control_info.appendPlainText)


def set_control_signal(self):
    if self.ui.box_signal_source.currentText() == "Hand":  # activate sliders and  deactivate join control
        # self.ui.pb_start_joint_control.setDisabled(True)
        [ds.setEnabled(True) for ds in self.hand_dses]
        [slider.setEnabled(True) for slider in self.hand_sliders]
    if self.ui.box_signal_source.currentText() == "KinectV2":  # deactivate sliders and  activate join control
        [ds.setDisabled(True) for ds in self.hand_dses]
        [slider.setDisabled(True) for slider in self.hand_sliders]


def set_initial_pose(self):   # kuka initial pose
    try:
        lock = mp.Lock()
        lock.acquire()
        self.ini_pose[:] = rc.get_pose(self.kuka_msg)[:]
        lock.release()
        gu.update_table(self.ini_pose, self.ui.table_ini_pose)
        self.ui.pb_start_control.setEnabled(True)
        self.ui.te_control_info.appendPlainText(self.time_stamp + "\tInitial Pose is set")
    except TypeError:
        self.ui.te_control_info.appendPlainText(self.time_stamp + "\tError: Initialising Error")


def start_control(self):
    if any(self.ini_pose) and (self.rsi_position_control is None):
        print(self.pose_limits, self.max_acc, self.max_v, self.max_omega, self.max_alpha, self.velocity_factor,
              self.omega_factor)
        if (self.ui.box_signal_source.currentText() == "KinectV2") and \
                (self.ui.box_control_object.currentText() == "HEAD_POSE"):
            control_mode = "xyzabc"
        elif self.ui.box_signal_source.currentText() == "Hand":
            control_mode = "xyzabc"
        elif self.ui.box_signal_source.currentText() == "RealsenseD435":
            control_mode = "xyz"
        else:
            control_mode = "xyz"
        print("control_mode", control_mode)
        self.rsi_position_control = RsiPositionControl(self.enable_ctl, control_mode,
                                                   self.ini_pose, self.ref_displacement, self.pre_pose,
                                                   self.motion_vec,
                                                   pose_limits=self.pose_limits,
                                                   acc_max=self.max_acc, v_max=self.max_v, ome_max=self.max_omega,
                                                   alp_max=self.max_alpha, v_factor=self.velocity_factor,
                                                   ome_factor=self.omega_factor)
        self.rsi_position_control.start()
        self.ui.pb_end_control.setEnabled(True)
        self.ui.pb_move_ini_pose.setEnabled(True)
        self.ui.pb_set_home.setEnabled(True)
        self.ui.pb_start_control.setDisabled(True)
        # self.ui.pb_start_printing.setDisabeld(True)
        self.ui.te_control_info.appendPlainText(self.time_stamp + "   The control process is started")
    else:

        self.ui.te_control_info.appendPlainText(self.time_stamp + "  Error: No initial pose is set")


def end_control(self):
    lock = mp.Lock()
    lock.acquire()
    present_pose = rc.get_pose(self.kuka_msg)
    # if present_pose is not None:
    self.ui.pb_move_ini_pose.setDisabled(True)
    if self.rsi_position_control is not None:
        self.ref_displacement[:] = [pre_coord - ini_coord
                                    for (pre_coord, ini_coord) in zip(present_pose, self.ini_pose)]
        self.rsi_position_control.end()
        self.rsi_position_control = None
        self.ui.pb_start_control.setEnabled(True)
        self.ui.pb_end_control.setDisabled(True)
        # self.ui.pb_start_printing.setEnabled(True)
        self.ui.te_control_info.appendPlainText(self.time_stamp + "\tThe Control process is ended")
    else:
        self.ui.te_control_info.appendPlainText(self.time_stamp + "\tError: control is not started yet")
    lock.release()


def terminate_control(self):
    lock = mp.Lock()
    self.ui.pb_move_ini_pose.setDisabled(True)
    if self.rsi_position_control is not None:
        self.rsi_position_control.kill()
        lock.acquire()
        self.motion_vec[:] = [0, 0, 0, 0, 0, 0]
        self.ui.te_control_info.appendPlainText(self.time_stamp + "\tControl Terminated")
        self.ui.pb_start_printing.setEnabled(True)
    else:
        self.ui.te_control_info.appendPlainText(self.time_stamp + "\tNo control process is active")


def move_initial_pose(self):
    if (self.ui.box_signal_source.currentText() == "Hand") and (self.rsi_position_control is not None):
        lock = mp.Lock()
        lock.acquire()
        self.ref_displacement[:] = [0] * 6
        lock.release()
        self.ui.te_control_info.appendPlainText(self.time_stamp + "\tmove initial pose")
    else:
        self.ui.te_control_info.appendPlainText(self.time_stamp +
                                                "\tError: signal source is not hand or control process is not started")


def set_home_pose(self):
    if self.ui.box_signal_source.currentText() == "Hand":
        try:
            lock = mp.Lock()
            lock.acquire()
            self.home_pose[:] = self.pre_pose[:]
            gu.update_table(self.home_pose, self.ui.table_home_pose)
            lock.release()
            self.ui.pb_homing.setEnabled(True)
            self.ui.te_control_info.appendPlainText(self.time_stamp + "   Home pose is set")
        except TypeError:
            self.ui.te_control_info.appendPlainText(self.time_stamp + "  Error: Setting home pose error")

    else:
        self.ui.te_control_info.appendPlainText(self.time_stamp + "  Error: Signal source is not hand")


def homing(self):
    if (self.ui.box_signal_source.currentText() == "Hand") and (self.rsi_position_control is not None):
        lock = mp.Lock()
        lock.acquire()
        self.ref_displacement[:] = [home_coord - pre_coord
                                    for (home_coord, pre_coord) in zip(self.home_pose, self.pre_pose)]
        lock.release()
        self.ui.te_control_info.appendPlainText(self.time_stamp + "  Move home pose")
    else:
        self.ui.te_control_info.appendPlainText(self.time_stamp +
                                             "  Error: signal source is not hand or control process is not started")


def set_hand_zero(self):
    lock = mp.Lock()
    [slider.setValue(0) for slider in self.hand_sliders]
    lock.acquire()
    #  m  and degree
    self.ref_displacement[:] = [0, 0, 0, 0, 0, 0]
    lock.release()


def hand_move(self):
    if self.ui.box_signal_source.currentText() == "Hand":
        lock = mp.Lock()
        hand_disp = [self.hand_dses[i].value() if i > 2 else self.hand_dses[i].value() / 1000 for i in range(6)]
        hand_disp = [saturate(hand_disp[i], self.pose_limits_ds[i * 2].value(),
                     self.pose_limits_ds[i * 2 + 1].value()) for i in range(6)]
        print(hand_disp)
        lock.acquire()
        #  m  and degree
        self.ref_displacement[:] = hand_disp[:]
        lock.release()
        # self.ui.te_control_info.appendPlainText(self.time_stamp + "   Hand move")
    else:
        self.ui.te_control_info.appendPlainText(self.time_stamp + "  Error: signal source is not hand")


class SimpleTransferFunction(object):
    """
        simple transfer function in form of a1 * ẏ + a0 * y = b1 * ẋ+ b0 * x
    """

    def __init__(self, numerator, denominator, output_min=-float("inf"), output_max=float("inf")):
        """
        param delta_t = sample delay time  in second
        """
        self.a1 = denominator[0]
        self.a0 = denominator[1]
        self.b1 = numerator[0]
        self.b0 = numerator[1]
        self.input_old = 0  # t = 0 or i -1
        self.output_old = 0  # t = 0 or i -1
        self.t_old = None
        self.output_max = output_max
        self.output_min = output_min

    def set_x0_y0(self, input_0=0, output_0=0):
        self.input_old = input_0
        self.output_old = output_0

    def tf(self, input_now):

        if self.t_old is None:
            # print('time.time():', time.time())
            # time.sleep(self.delta_t)
            output = 0 if self.b1 == 0 else self.b1/self.a1 * input_now
            self.t_old = time.time()
        else:
            # time.sleep(self.delta_t)
            t = time.time()
            dt = t - self.t_old
            # try:
            output = 1 / (self.a1 + self.a0 * dt) \
                * (self.a1 * self.output_old + self.b1 * input_now - self.b1 * self.input_old + self.b0 * dt * input_now)
            self.t_old = t
        output = saturate(output, self.output_min, self.output_max)
        self.input_old = input_now  # t now
        self.output_old = output  # t now
        return output

    def step(self, amplitude=1, time_interval=5):
        t = []
        output = []
        t_start = time.time()
        # i = 0
        while True:
            # print('i:', i)
            self.tf(amplitude)
            t.append(self.t_old - t_start)
            output.append(self.output_old)
            if self.t_old - t_start > time_interval: break
            # i += 1
        plot(t, output, label="stf")
        # plot(t_old_lst, pt1_old_lst, label="pt1")
        grid()
        legend()
        show()


class TransferFunction(object):
    """ still to consider the saturation """
    def __init__(self, numerator, denominator):
        """
        param denominator:  an  ... a0
        param numerator: bm ...  b0
        """
        numerator = [bi / denominator[0] for bi in numerator]    # normalize a vector
        denominator = [ai / denominator[0] for ai in denominator]  # normalize b vector
        len_num = len(numerator)
        len_den = len(denominator)
        print("normalized system:", numerator, "/", denominator)
        a = denominator[::-1]
        b = numerator[::-1]
        b = b + (len_den - len_num) * [0]
        self.x = np.array([[0] * (len_den - 1)], dtype="f")
        # self.num = np.array(numerator, dtype="f")
        # self.den = np.array(denominator, dtype="f")
        if len_den < 3:
            self.A = np.array([-a[-1]], "f")
            # self.B = np.array([b[0]], "f")
            # self.C = np.array([b[0] - a[0]], "f")
            # self.D = np.array([b[1]])
        else:
            I = np.identity(len_den - 2, dtype="f")
            zero_vector = np.array([[0]] * (len_den - 2))
            a_vector = np.array(denominator[-1:0:-1], dtype="f")
            upper_part_A = np.hstack((zero_vector, I))
            self.A = np.vstack((upper_part_A, a_vector))
            print("I:", I, "I.ndim:", I.ndim, I.size,
                  "zero_vector:", zero_vector, "zero_vector.ndim:", zero_vector.ndim, zero_vector.size)
        self.B = np.array([0] * (len_den - 2) + [1], dtype="f")
        self.C = np.array([[bi - b[-1] * ai] for (ai, bi) in zip(a[:-1], b[:-1])], dtype="f")
        self.D = np.array([b[-1]], dtype="f")

    def show_space_model(self):
        print("system matrix A:\n\r", self.A)
        print("input matrix B:\n\r", self.B)
        print("output matrix C:\n\r", self.C)
        print("feedthrough matrix:\n\r", self.D)

    def set_x_0(self, x0):
        self.x = x0

    def tf(self, input_vector, output):
        pass


class StateSpace(object):
    def __init__(self, numerator, denominator):
        pass

    def set_x_0(self, x_0):
        pass

    def tf(self, input, output):
        pass


class RsiPositionControl(mp.Process):

    def __init__(self, enable_control, control_mode,
                 initial_pose, reference_displacement, present_pose, motion_vector,
                 pose_limits=kuka_pose_limits,
                 acc_max=acceleration_max, v_max=velocity_max,  ome_max=omega_max, alp_max=alpha_max,
                 # omega: angular velocity  degree/s,  alpha: angular acceleration degree/s^2
                 v_factor=velocity_factor, ome_factor=omega_factor):
        super().__init__(daemon=True)

        # control parameters
        self.enable_control = enable_control
        self.control_mode = control_mode
        # motion limits
        self.pose_limits = pose_limits[:]  # in order of  x y z a b c
        self.acc_max = acc_max
        self.v_max = v_max
        self.ome_max = ome_max
        self.alp_max = alp_max

        # kuka constants
        lock = mp.Lock()
        self.v_factor = v_factor  # 1 entspricht  0.25 m/s
        self.ome_factor = ome_factor
        # self.active_axis = active_axis.lower()
        lock.acquire()
        self.ini_pose = initial_pose[:]
        lock.release()


        # shared memory
        # self.kuka_msg = kuka_message
        self.pre_pose = present_pose
        self.ref_disp = reference_displacement
        self.motion_vec = motion_vector

    def run(self):
        self.enable_control.value = 1
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
        # axis_number = 6 if self.control_mode == "xyzabc" else 3
        while self.enable_control.value or any([abs(axis_velocity) > 0.005 for axis_velocity in self.motion_vec]):
            lock.acquire()
            pre_pose = self.pre_pose[:]
            ref_pose = self.ref_disp[:]  # robot present position, unit in m
            lock.release()
            ref_pose = [saturate(ref_pose[i], self.pose_limits[i * 2], self.pose_limits[i * 2 + 1])
                        for i in range(len(ref_pose))]

            motion_vec = [axes_tfs[i]['i'].tf(
                axes_tfs[i]['c'].tf(
                    axes_tfs[i]["p3"].tf(axes_tfs[i]['p2'].tf(axes_tfs[i]['p1'].tf(ref_pose[i])))
                    - (pre_pose[i] - self.ini_pose[i])))
                for i in range(3)] + \
                [axes_tfs[i]['i'].tf(
                    axes_tfs[i]['c'].tf(
                        axes_tfs[i]['p2'].tf(axes_tfs[i]['p1'].tf(ref_pose[i])) - (pre_pose[i] - self.ini_pose[i])))
                 for i in range(3, 6)]  # xyz in m/s  and  abc in deg/s
            # print('motion_vec', motion_vec)
            if self.control_mode == "xyzabc":
                motion_vec[0:3] = [ele / self.v_factor for ele in motion_vec[0:3]]
                motion_vec[3:6] = [ele / self.ome_factor for ele in motion_vec[3:6]]
            else:
                motion_vec[0:3] = [ele / self.v_factor for ele in motion_vec[0:3]]
                motion_vec[3:6] = [0, 0, 0]
            # print('motion_vec', motion_vec)
            lock.acquire()
            self.motion_vec[:] = motion_vec[:]       # in percentage
            lock.release()
            time.sleep(0.001)
        print("control ended")

    def end(self):
        self.enable_control.value = 0


class UpdateJointReferenceDisplacement(td.Thread):
    def __init__(self, joint_name, joint_present_pose, joint_displacement, reference_displacement, pose_limits,
                 minimal_distance=1.3, offset_kuka_to_kinect_x=0, offset_kuka_to_kinect_y=0.2):
        super().__init__(daemon=True)
        self.ref_disp = reference_displacement   # m deg
        self.pre_pose = joint_present_pose   # m deg
        self.enable_joint_control = 1
        self.joint_disp = joint_displacement  # m  deg
        self.joint_name = joint_name
        self.pose_limits = pose_limits

        #customer parameters
        # self.obj_dis = 0.5    # object from a man to the kuka flange
        self.min_dis = minimal_distance  # mininal distance between kinect and a man
        self.off_x = offset_kuka_to_kinect_x   # based on kuka coordinate system
        self.off_y = offset_kuka_to_kinect_y   # based on kuka coordinate system

        self.zone_min_x = self.min_dis
        self.zone_max_x = self.zone_min_x + (self.pose_limits[1] - self.pose_limits[0])
        # distance_kuka_man = self.pose_limits[1] - self.pose_limits[0]) / 2
        # kuka  x,y,z  valid zone
        self.k = self.pose_limits[1] / (self.min_dis + self.pose_limits[1] - self.pose_limits[0])
        self.zone_min_y = self.pose_limits[2] / self.k
        self.zone_max_y = self.pose_limits[3] / self.k
        print(self.zone_min_x, self.zone_max_x)
        print(self.zone_min_y, self.zone_max_y)

    def run(self):
        lock = mp.Lock()
        while self.enable_joint_control:  # todo  confirm the x y z  andy pitch yaw roll
            time.sleep(0.01)
            lock.acquire()
            disp = [dx, dy, dz, da, db, dc] = self.joint_disp[:]
            pre = [pre_x, pre_y, pre_z, pre_a, pre_b, pre_c] = self.pre_pose[:]
            lock.release()
            if self.joint_name == "HEAD_POSE":
                if all(disp):
                    ref_x = dy
                    ref_y = dx + math.tan(math.radians(da)) * pre_y
                    ref_z = dz
                    ref_a = - da
                    ref_x = saturate(ref_x, self.pose_limits[0], self.pose_limits[1])
                    ref_y = saturate(ref_y, self.pose_limits[2], self.pose_limits[3])
                    ref_z = saturate(ref_z, self.pose_limits[4], self.pose_limits[5])
                    ref_a = saturate(ref_a, self.pose_limits[6], self.pose_limits[7])
                    lock.acquire()
                    self.ref_disp[0:4] = [ref_x, ref_y, ref_z, ref_a]  # m
                    lock.release()

            elif self.joint_name == "Customer":
                if all(pre[0:3]):
                    if (self.zone_min_x < pre_y - self.off_x < self.zone_max_x) \
                            and (self.zone_min_y < pre_x - self.off_y < self.zone_max_y):
                        # print("pre_x, pre_y", pre_x, pre_y)
                        ref_x = pre_y - self.off_x - self.min_dis + self.pose_limits[0]
                        ref_y = (pre_x - self.off_y) * self.k
                        # print([ref_x, ref_y])
                        ref_x = saturate(ref_x, self.pose_limits[0], self.pose_limits[1])
                        ref_y = saturate(ref_y, self.pose_limits[2], self.pose_limits[3])
                    else:
                        ref_x = ref_y = 0
                    lock.acquire()
                    self.ref_disp[0:2] = [ref_x, ref_y]  # m
                    lock.release()

            else:
                if all(disp[0:3]):
                    ref_x = saturate(dy, self.pose_limits[0], self.pose_limits[1])
                    ref_y = saturate(dx, self.pose_limits[2], self.pose_limits[3])
                    ref_z = saturate(dz, self.pose_limits[4], self.pose_limits[5])
                    lock.acquire()
                    self.ref_disp[0:3] = [ref_x, ref_y, ref_z]   # m
                    lock.release()

    def end(self):
        self.enable_joint_control = 0



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
    tff = TransferFunction([1, 3, 3], [1, 2, 1])
    tff.show_space_model()


