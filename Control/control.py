# -*- utf-8 -*-
# @Time:  2023/3/1 22:35
# @Autor: Andy Ye
# @File:  control.py
# @IDE: PyCharm
import time
from matplotlib.pyplot import plot, show, grid, legend



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





if __name__ == '__main__':
    t1 = SimpleTransferFunction([0, 1], [1, 1])
    t1.step()