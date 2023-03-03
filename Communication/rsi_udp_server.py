# -*- utf-8 -*-
# @Time:  2023/3/2 10:25
# @Autor: Andy Ye
# @File:  rsi_udp_server.py
# @IDE: PyCharm


import socket
from Communication.functions import *


class RsiUdpServer(mp.Process):
    def __init__(self, control_mode, communication_state,  present_pose, control_vector,
                 rsi_server_port=59152, buffer_size=1024, daemon=True):
        super().__init__(daemon=daemon)
        # self.rsi_modem = rsi_modem
        self.comm_state = communication_state
        self.control_vec = control_vector
        self.buffer_size = buffer_size
        self.pre_pose = present_pose
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(("", rsi_server_port))
        self.get_pose_callback = extract_pose_axis if control_mode == "Axis" else extract_pose_cartesian
        self.create_cmd_callback = control_cmd_axis if control_mode == "Axis" else control_cmd_cartesian

    def run(self):
        print('start Rsi Udp Server')
        lock = mp.Lock()
        while True:
            # read and write istposition
            # print("self.comm_state.value", self.comm_state.value)
            bytes_data_kuka, address_kuka = self.server.recvfrom(self.buffer_size)  # kuka message
            self.kuka_msg = bytes_data_kuka.decode("utf-8")
            ipoc = get_ipoc(bytes_data_kuka)
            pre_pose = self.get_pose_callback(self.kuka_msg)
            with lock:
                self.pre_pose[:] = pre_pose[:]
                motion_ipoc = self.control_vec[:]
                # self.comm_state.value = 3  # communicating
            motion_cmd = self.create_cmd_callback(motion_ipoc, ipoc)
            self.server.sendto(motion_cmd.encode("utf-8"), address_kuka)


if __name__ == '__main__':
    mode = "axis"
