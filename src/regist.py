#!/usr/bin/python
import logging, master_conf
# User need to add import from their module below
from module.module_tcp_test.main import *
from module.module_print_test.main import *

tcp_module = None
time_module = None

# User need to add module info in below function
def tcp_module_conf_init():
    global tcp_module
    if master_conf.working_mode == 1:
        # Online Environment
        tcp_module = [
        ]
    else:
        # Test Environment Module Load
        tcp_module = [
            {
                "name":"tcp_echo",
                "module":echo_server
            }
        ]

# User need to add module info in below function
def time_module_conf_init():
    global time_module
    if master_conf.working_mode == 1:
        # Online Environment
        time_module = [
        ]
    else:
        # Test Environment Module Load
        time_module = [
            {
                "name":"print_test",
                "module":module_print_test
            }
        ]



def time_module_init():
    save_list = []
    for i in time_module:
        tl = i["module"]()
        tl.frame_master_init()
        res = tl.load_init()
        if res < 0:
            logging.error("load module error %s" % (str(i)))
            continue
        logging.info("success load time module %s" % (str(i)))

        new_module = {}
        new_module["class"] = tl
        new_module["name"] = i["name"]

        save_list.append(new_module)
    return save_list

def tcp_module_init():
    save_list = []
    for i in tcp_module:
        tl = i["module"]()
        res = tl.load_init()
        if res < 0:
            logging.error("load module error %s" % (str(i)))
            continue
        logging.info("success load tcp module %s" % (str(i)))
        new_module = {}
        new_module["class"] = tl
        new_module["name"] = i["name"]
        save_list.append(new_module)
    return save_list

def output_module_info():
    fd = open("module.info", "w")
    if fd:
        string = ""
        for i in time_module:
            pass
        fd.close()
