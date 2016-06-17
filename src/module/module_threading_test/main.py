#!/usr/bin/python
import sys, logging
sys.path.append("../..")
from time_base import *

class module_threading_test(time_base):
    def __init__(self):
        self.time_between = 10
        self.desc = "A test module"
        self.name = "Module_Threading_Test"
        self.var = 0

    def load_init(self):
        logging.debug("%s init success and ready to run" % self.name)
        return 0

    def time_handle(self, now_time):
        if self.time_judge(now_time):
            self.lasttime = now_time
            self.var += 1
            logging.info("module:%s value:%d" % (self.name, self.var))
            return 0
        else:
            return -1

