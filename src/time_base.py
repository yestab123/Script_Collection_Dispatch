#!/usr/bin/python

class time_base(object):
    def __init__(self):
        self.hour = -1
        self.min = -1
        self.day = -1
        self.timeout = -1
        self.lasttime = 0       # The time that time event execute last time in second.

    # Must return int value for master to judge status
    def load_init(self):
        return 0

    def time_handle(self, now_time):
        pass

    # No use now
    def time_judge(self, now_time):
        pass

    # Signal num from 34 to 45(include 45)
    def time_signal_handle(self, signo):
        pass
