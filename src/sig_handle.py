#!/usr/bin/python
import os, signal, sys, logging

Restart_Flag = 0
User_signal = []
User_signal_flag = 0

# User signal num from 34 to 45
def signal_regist():
    # Set Signal Handle
    signal.signal(signal.SIGUSR1, SIGUSR1_handle)
    for i in range(34, 46):
        signal.signal(i, user_signal_handle)

# Signal to Output Module info to module.info file.
def SIGUSR1_handle(signum, frame):
    # global Restart_Flag
    # Restart_Flag = 1
    # logging.info("recv RESTART signal SIGUSR1")
    pass

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def user_signal_handle(signum, frame):
    global User_signal_flag
    User_signal_flag = 1
    User_signal.append(signum)

