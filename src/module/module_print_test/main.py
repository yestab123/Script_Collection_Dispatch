#!/usr/bin/python
import sys, logging
sys.path.append("../..")
from time_base import *

class module_print_test(time_base):
    def __init__(self):
        self.time_between = 20
        self.desc = "A test module to print text every 20 sec"
        self.name = "Module_Print_Test"

    def load_init(self):
        logging.debug("%s init success and ready to run" % self.name)
        return 0

    def time_handle(self, now_time):
        if self.time_judge(now_time):
            self.lasttime = now_time
            logging.info("module:%s running" % self.name)
            return 0
        else:
            return -1

    def time_signal_handle(self, signo):
        logging.info("module:%s recv signal:%d and processing" % (self.name, signo))
        return 0



if __name__ == '__main__':
    c = module_print_test()
    c.frame_master_init()
    c.load_init()
    c.time_handle(10000)
    c.time_signal_handle(35)
