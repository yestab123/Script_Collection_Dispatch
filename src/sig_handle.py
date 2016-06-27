#!/usr/bin/python
import os, signal, sys, logging

Restart_Flag = 0
Stop_Flag = 0
User_signal = []
User_signal_flag = 0

# User signal num from 34 to 45
def signal_regist():
    # Set Signal Handle
    signal.signal(signal.SIGUSR1, SIGUSR1_handle)
    signal.signal(signal.SIGTERM, SIGTERM_handle)
    for i in range(34, 46):
        signal.signal(i, user_signal_handle)

# Signal to Output Module info to module.info file.
def SIGUSR1_handle(signum, frame):
    # global Restart_Flag
    # Restart_Flag = 1
    # logging.info("recv RESTART signal SIGUSR1")
    pass

# Set SIGTERM flag, give master process time to clean environment
def SIGTERM_handle(signum, frame):
    global Stop_Flag
    Stop_Flag = 1
    logging.info("Recv SIGTERM signal, Set Flag to clean environment")
    
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def user_signal_handle(signum, frame):
    global User_signal_flag
    User_signal_flag = 1
    User_signal.append(signum)

