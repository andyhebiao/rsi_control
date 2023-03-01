# -*- utf-8 -*-
# @Time:  2023/3/1 22:35
# @Autor: Andy Ye
# @File:  control.py
# @IDE: PyCharm
import time
from matplotlib.pyplot import plot, show, grid, legend
import multiprocessing as mp
from constant import *


def saturate(original, low_limit, up_limit):
    assert low_limit < up_limit, "Limits order wrong"
    original = original if original < up_limit else up_limit
    original = original if original > low_limit else low_limit
    return original


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


class RsiPositionControl(mp.Process):
    def __init__(self,  initial_pose, reference_pose, present_pose, motion_vector,
                 pose_limits=kuka_pose_limits,
                 acc_max=acceleration_max, v_max=velocity_max,  ome_max=omega_max, alp_max=alpha_max,
                 # omega: angular velocity  degree/s,  alpha: angular acceleration degree/s^2
                 v_factor=velocity_factor, ome_factor=omega_factor):
        super().__init__(daemon=True)
        # motion limits
        self.pose_limits = pose_limits[:]  # in order of  x y z a b c
        self.acc_max = acc_max
        self.v_max = v_max
        self.ome_max = ome_max
        self.alp_max = alp_max
        lock = mp.Lock()
        self.v_factor = v_factor  # 1 entspricht  0.25 m/s
        self.ome_factor = ome_factor
        with lock:
           self.ini_pose = initial_pose[:]

        self.pre_pose = present_pose
        self.ref_pose = reference_pose
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
        while True:
            with lock:
                pre_pose = self.pre_pose[:]
                ref_pose = self.ref_disp[:]  # robot present position, unit in m
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
            motion_vec[0:3] = [ele / self.v_factor for ele in motion_vec[0:3]]
            motion_vec[3:6] = [ele / self.ome_factor for ele in motion_vec[3:6]]
            with lock:
                self.motion_vec[:] = motion_vec[:]       # in percentage
            time.sleep(0.001)


if __name__ == '__main__':
    t1 = SimpleTransferFunction([0, 1], [1, 1])
    t1.step()