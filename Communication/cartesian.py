# -*- utf-8 -*-
# @Time:  2023/2/27 19:49
# @Autor: Andy Ye
# @File:  cartesian.py
# @IDE: PyCharm
import re


def remap_kuka_pose(pose):
    """
    mapping for not continuous angle space, and reversed angular velocity
    """
    [a, b, c] = pose[3:6]
    a = a if a > 0 else a + 360   # A
    b = -b
    c = -c if c < 0 else 360 - c

    return [pose[0], pose[1], pose[2], a, b, c]


def extract_pose_cartesian(kuka_msg):  # kuka_message in multiprocessing
    r = re.compile(r'RIst (?:X=\")(?P<X>[-\d]+\.*\d*)(?:\") '
                   r'(?:Y=\")(?P<Y>[-\d]+\.*\d*)(?:\") '
                   r'(?:Z=\")(?P<Z>[-\d]+\.*\d*)(?:\") '
                   r'(?:A=\")(?P<A>[-\d]+\.*\d*)(?:\") '
                   r'(?:B=\")(?P<B>[-\d]+\.*\d*)(?:\") '
                   r'(?:C=\")(?P<C>[-\d]+\.*\d*)(?:\")')
    m = r.search(kuka_msg)
    return remap_kuka_pose([float(m.group(axis)) for axis in ['X', 'Y', 'Z', 'A', 'B', 'C']]) if m else None # in mm and degree


def control_cmd_cartesian(control_vector, ipoc):
    control_vector.append(ipoc)
    return "<Sen Type=\"ImFree\">\r\n" \
             "<RKorr X=\"%0.3f\" Y=\"%0.3f\"Z=\"%0.3f\" A=\"%0.3f\" B=\"%0.3f\" C=\"%0.3f\" />\r\n" \
             "<IPOC>%d</IPOC>\r\n" \
             "</Sen>" \
             % tuple(control_vector)


if __name__ == '__main__':
    print(control_cmd_cartesian([1, 2, 3, 4, 5, 6], 1234))
