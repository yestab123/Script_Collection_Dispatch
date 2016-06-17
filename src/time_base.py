#!/usr/bin/python

class time_base(object):
    def __init__(self):
        self.time_between = 0   # Waiting How many time to execute 
        self.desc = ""
        self.name = ""

    # Don't Re-Define In your class.
    def frame_master_init(self):
        self.lasttime = 0       # The time that time event execute last time in second.
        self.process = None     # Event Running Process Save
        self.signo = []         # Signal Number Saving List

    # Loading Init Function.
    # Must return int value for master to judge status
    def load_init(self):
        return 0

    # Must Rewrite
    # If can run this time return True, else return False
    def time_judge(self, now_time):
        if now_time - self.lasttime > self.time_between:
            return True
        return False

    # Must Rewrite
    # Time Event Handle Function.(Main Action Run in here)
    def time_handle(self, now_time):
        if self.time_judge(now_time):
            self.lasttime = now_time
            # Running Event
            return 0
        else:
            return -1

    # # No use now
    # def time_judge(self, now_time):
    #     pass

    # Signal num from 34 to 45(include 45)
    def time_signal_handle(self, signo):
        pass
