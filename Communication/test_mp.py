# -*- utf-8 -*-
# @Time:  2023/2/28 17:05
# @Autor: Andy Ye
# @File:  test_mp.py
# @IDE: PyCharm

import multiprocessing as mp
import time


class MyProcess(mp.Process):
    def __init__(self, daemon=False):
        super().__init__(daemon=daemon)
        self.enable = True

    def run(self):
        while True:
            print(time.asctime())
            time.sleep(1)



if __name__ == '__main__':
    p = MyProcess()
    p.start()
    time.sleep(3)
    p.terminate()
    # p.kill()
    # p.close()
    time.sleep(2)
