# -*- utf-8 -*-
# @Time:  2023/3/1 18:52
# @Autor: Andy Ye
# @File:  functions.py
# @IDE: PyCharm
from PyQt5.QtWidgets import QTableWidgetItem
import multiprocessing as mp


def update_table(data_list, ui_table):
    lock = mp.Lock()
    with lock:
        local_data_list = data_list[:]
    [ui_table.setItem(
        i, 0, QTableWidgetItem("%0.1f" % element if element else "None"))
        for (i, element) in enumerate(local_data_list)]
    ui_table.viewport().update()