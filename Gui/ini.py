# -*- utf-8 -*-
# @Time:  2023/3/1 18:52
# @Autor: Andy Ye
# @File:  ini.py
# @IDE: PyCharm
from PyQt5 import QtCore


def init(self):
    self.show_info = self.ui.pte_info.appendPlainText
    self.ui_timer = QtCore.QTimer()
    self.ui_timer.start(30)

    # self.ui_timer.timeout.connect(self.update_ui_states)

