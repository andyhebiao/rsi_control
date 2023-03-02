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
from Communication.rsi_udp_server import RsiUdpServer


def set_static_ip(self):
    if platform.system() == "Windows":
        set_cmd = "netsh interface ip set address name=\"%s\" " \
                  "source=\"static\" addr=\"%s\" mask=\"%s\"" \
                  % (self.rsi_net_adapter, self.rsi_server_ip, self.rsi_server_mask)
        sub.call(set_cmd, shell=True)
    else:
        self.show_info("wrong system")


def set_dhcp(self):
    if platform.system() == "Windows":
        set_cmd = "netsh interface ip set address name=\"%s\" source=\"dhcp\"" % self.ui.le_rsi_net_adapter.text()
        sub.call(set_cmd, shell=True)
    else:
        self.show_info("wrong system")


def get_ipoc(data):
    r = re.compile(r'(?:<IPOC>)(?P<IPOC>[\S\s]*)(?:</IPOC>)')
    m = r.search(data)
    ipoc = int(m.group('IPOC'))
    return ipoc


def start_rsi_com(self):
    if self.rsi_com is None:
        try:
            self.rsi_com = RsiUdpServer(self.ui.combo_control_mode.currentText(),
                                        self.pre_pose, self.control_vector,  self.ui.sb_rsi_server_port.value())
            self.rsi_com.start()
            self.ui.pb_start_rsi_com.setDisabled(True)
            self.ui.pb_stop_rsi_com.setEnabled(True)
            self.ui.pb_terminate_rsi_com.setEnabled(True)
            self.show_info(time.asctime() + "\t" + "The Communication Server is started, start KUKA RSI now!")
        except Exception as error:
            self.show_info(time.asctime() + "\t" + str(error))
    else:
        self.show_info(time.asctime() + "\t" + "communication already starts, start KUKA RSI now!")


def stop_rsi_com(self):
    if self.rsi_com is not None:
        self.rsi_com.end()
        self.com_state.value = 0
        self.rsi_com = None
        # self.ini_pose = None
        self.ui.pb_start_rsi_com.setEnabled(True)
        self.ui.pb_stop_rsi_com.setDisabled(True)
        self.show_info(time.asctime() + "\t" + "communication stopped")
    else:
        self.show_info(time.asctime() + "\t" + "communication already closed")


def load_config(self, file_path="") -> bool:
    if not file_path:
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Config File", "./config_files", "Config Files(*.cfg)")
    if not file_path:
        self.show_info(time.asctime() + "\t" + "No config file is loaded.")
        return False
    else:
        cfg = configparser.ConfigParser()
        try:
            print(str(file_path))
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
        self.show_info(time.asctime() + "\t" + file_path + " is loaded.")
        return True


def export_config_file(self) -> bool:
    file_path, _ = QFileDialog.getSaveFileName(self, "Export Config File", "./config_files", "Config Files(*.cfg)")
    if not file_path:
        self.show_info(time.asctime() + "\t" + "No config file is exported.")
        return False
    else:
        cfg = configparser.ConfigParser()
        try:
            cfg.read(file_path, encoding='gbk')
        except UnicodeError:
            cfg.read(file_path, encoding='utf-8')
        for section, section_dict in self.parameter_sections_dict.items():
            # execute callbacks to get the actual values
            section_dict = {key: section_dict[key]() for key in section_dict}
            print("section:", section, "section_dict:", section_dict)
            cfg[section] = section_dict
        with open(file_path, 'w', encoding="utf-8") as configfile:
            cfg.write(configfile)

        self.show_info(time.asctime() + "\t" + file_path + " is exported.")
        return True


