# -*- utf-8 -*-
# @Time:  2023/2/27 19:42
# @Autor: Andy Ye
# @File:  axis.py
# @IDE: PyCharm
import re
import multiprocessing as mp


def extract_pose_axis(kuka_message):  # kuka_message in multiprocessing.array type
    lock = mp.Lock()
    with lock:
        kuka_msg = kuka_message[:].decode("utf-8").strip("\0")
    r = re.compile(r'AIPos (?:A1=\")(?P<A1>[-\d]+\.*\d*)(?:\") '
                   r'(?:A2=\")(?P<A2>[-\d]+\.*\d*)(?:\") '
                   r'(?:A3=\")(?P<A3>[-\d]+\.*\d*)(?:\") '
                   r'(?:A4=\")(?P<A4>[-\d]+\.*\d*)(?:\") '
                   r'(?:A5=\")(?P<A5>[-\d]+\.*\d*)(?:\") '
                   r'(?:A6=\")(?P<A6>[-\d]+\.*\d*)(?:\")')
    m = r.search(kuka_msg)
    return [float(m.group(axis)) for axis in ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']]  if m else None # in degree


def control_cmd_axis(control_vector, ipoc):
    control_vector.append(ipoc)
    return "<Sen Type=\"ImFree\">\r\n" \
           "<RKorr A1=\"%0.3f\" A2=\"%0.3f\" A3=\"%0.3f\" A4=\"%0.3f\" A5=\"%0.3f\" A6=\"%0.3f\" />\r\n" \
           "<IPOC>%d</IPOC>\r\n" \
           "</Sen>" \
        % tuple(control_vector)


if __name__ == '__main__':
    print(control_cmd_axis([1, 2, 3, 4, 5, 6], 1234))
