#!/usr/bin/python
import sys, logging
sys.path.append("../..")
from time_base import *

class module_print_test(time_base):
    def __init__(self):
	self.time_between = 10

    def time_handle(self, now_time):
        if now_time - self.lasttime > 5:
            self.lasttime = now_time
            logging.debug("module_print_test print 1234")

