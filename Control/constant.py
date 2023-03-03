# -*- utf-8 -*-
# @Time:  2023/3/1 0:43
# @Autor: Andy Ye
# @File:  constant.py
# @IDE: PyCharm



# cartesian
cartesian_limits = (-180, 180, -180, 180, -180, 180, -18.0, 18.0, -18.0, 18.0, -18.0, 18.0)  # mm  or  degree
acceleration_max = 500  # mm/s^2
velocity_max = 250  # mm/s
cartesian_omega_max = 14.0  # degree/s
cartesian_alpha_max = 14.0  # degree/s^2
velocity_factor = 250  # 100 %
cartesian_omega_factor = 144.0    # 100 %


# axis
axis_offset_limits = (-10, 10, -10, 10, -10, 10, -10, 10, -10, 10, -10, 10)  # degree
# axis_pose_bounds = [[axis_offset_limits[i * 2] + self.ini_pose[i], pose_limits[i * 2 + 1] + self.ini_pose[i]]
#                            for i in range(6)]
axis_omega_max = 14.0  # degree/s
axis_alpha_max = 14.0  # degree/s^2
axis_omega_factor = 144.0    # 100 %
