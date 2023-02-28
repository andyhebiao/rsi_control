# -*- utf-8 -*-
# @Time:  2023/2/27 17:45
# @Autor: Andy Ye
# @File:  functions.py
# @IDE: PyCharm

import socket
import re
import multiprocessing as mp
import time
import threading as td
import subprocess as sub
import platform
import configparser
from PyQt5.QtWidgets import QFileDialog
from Communication.cartesian import *
from Communication.axis import *


def set_static_ip(self):
    if platform.system() == "Windows":
        set_cmd = "netsh interface ip set address name=\"%s\" " \
                  "source=\"static\" addr=\"%s\" mask=\"%s\"" \
                  % (self.rsi_net_adapter, self.rsi_server_ip, self.rsi_server_mask)
        sub.call(set_cmd, shell=True)
    else:
        print("wrong system")


def set_dhcp(net_adapter):
    if platform.system() == "Windows":
        set_cmd = "netsh interface ip set address name=\"%s\" source=\"dhcp\"" % net_adapter
        sub.call(set_cmd, shell=True)
    else:
        print("wrong system")


def get_ipoc(data):
    r = re.compile(r'(?:<IPOC>)(?P<IPOC>[\S\s]*)(?:</IPOC>)')
    m = r.search(data)
    ipoc = int(m.group('IPOC'))
    return ipoc


def start_rsi_com(self):
    if self.rsi_com is None:
        self.com_state.value = 1
        try:
            self.rsi_com = RsiUdpServer(self.com_state, self.kuka_msg, self.pre_pose, self.motion_vec,
                                        rsi_server_port=self.rsi_server_port)
            self.rsi_com.start()
            self.ui.pb_start_rsi_com.setDisabled(True)
            self.ui.pb_stop_rsi_com.setEnabled(True)
        except Exception as error:
            print(error)
    else:
        print("communication already starts")


def stop_rsi_com(self):
    if self.rsi_com is not None:
        self.rsi_com.end()
        self.com_state.value = 0
        self.rsi_com = None
        # self.ini_pose = None
        self.ui.pb_start_rsi_com.setEnabled(True)
        self.ui.pb_stop_rsi_com.setDisabled(True)
    else:
        print("communication already closed")


def load_config(self, file_path="", prompt_obj_callback=None) -> bool:
    if not file_path:
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Config File", "./config_files", "Config Files(*.cfg)")
    if not file_path:
        return False
    else:
        cfg = configparser.ConfigParser()
        try:
            cfg.read(file_path, encoding='gbk')
        except UnicodeError:
            cfg.read(file_path, encoding='utf-8')
        for section in cfg.sections():
            for (key, value) in cfg.items(section):
                if "sb_" + key in dir(self.ui):
                    exec("self.ui.sb_" + key + ".setValue(" + value + ")")
                    # exec("self." + key + "=" + value)
                    # print("self." + key + "=" + value)
                elif "ds_" + key in dir(self.ui):
                    exec("self.ui.ds_" + key + ".setValue(" + value + ")")
                    # exec("self." + key + "=" + value)
                    # print("self." + key + "=" + value)
                elif "le_" + key in dir(self.ui):
                    # print("le_" + key)
                    exec("self.ui.le_" + key + ".setText(\"" + value + "\")")
                    # exec("self." + key + "=\"" + value + "\"")
                    # print("self." + key + "=" + value)
                elif "combo_" + key in dir(self.ui):
                    # print("self.ui.combo_" + key + ".setCurrentText(\"" + value + "\")")
                    exec("self.ui.combo_" + key + ".setCurrentText(\"" + value + "\")")
                    # self.ui.combo_rsi_mode.setCurrentText("")
                elif key in dir(self):
                    exec("self." + key + "=" + value)
                    # print("self." + key + "=" + value)
                else:
                    print("redundant parameters:", key, "=", value)
        if prompt_obj_callback:
            prompt_obj_callback(time.asctime() + "\t" + file_path + " is loaded.")
        return True


def export_config_file(self, sections_dict, prompt_obj_callback=None) -> bool:
    file_path, _ = QFileDialog.getSaveFileName(self, "Export Config File", "./config_files", "Config Files(*.cfg)")
    if not file_path:
        return False
    else:
        cfg = configparser.ConfigParser()
        try:
            cfg.read(file_path, encoding='gbk')
        except UnicodeError:
            cfg.read(file_path, encoding='utf-8')
        for section, section_dict in sections_dict.items():
            # execute callbacks to get the actual values
            section_dict = {key: section_dict[key]() for key in section_dict}
            print("section:", section, "section_dict:", section_dict)
            cfg[section] = section_dict
        with open(file_path, 'w', encoding="utf-8") as configfile:
            cfg.write(configfile)

        if prompt_obj_callback:
            prompt_obj_callback(time.asctime() + "\t" + file_path + " is exported.")
        return True


class RsiUdpServer(mp.Process):
    def __init__(self, rsi_modem, communication_state,  present_pose, control_vector,
                 rsi_server_port=59152, buffer_size=1024, daemon=True):
        super().__init__(daemon=daemon)
        # self.rsi_modem = rsi_modem
        self.comm_state = communication_state
        self.control_vec = control_vector
        self.buffer_size = buffer_size
        self.pre_pose = present_pose
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(("host", rsi_server_port))
        self.get_pose_callback = extract_pose_axis if rsi_modem == "axis" else extract_pose_cartesian
        self.create_cmd_callback = control_cmd_axis if rsi_modem == "axis" else control_cmd_cartesian

    def run(self):
        print('start Rsi Udp Server')
        lock = mp.Lock()
        with lock:
            self.comm_state.value = 2  # starting communication
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
                self.comm_state.value = 3  # communicating

            motion_ipoc.append(ipoc)
            motion_cmd = "<Sen Type=\"ImFree\">\r\n" \
                         "<RKorr X=\"%0.3f\" Y=\"%0.3f\"Z=\"%0.3f\" A=\"%0.3f\" B=\"%0.3f\" C=\"%0.3f\" />\r\n" \
                         "<IPOC>%d</IPOC>\r\n" \
                         "</Sen>" \
                         % tuple(motion_ipoc)
            self.server.sendto(motion_cmd.encode("utf-8"), address_kuka)

    def terminate(self):
        print("communication stopped")
        super().terminate()
        time.sleep(0.11)
        super().close()

