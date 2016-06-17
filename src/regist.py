#!/usr/bin/python
import logging
from module.module_print_test.main import *
from module.module_threading_test.main import *
tcp_module = []
time_module = [module_print_test, module_threading_test]
time_module_t = [
    {
        "name":"Module_Print_Test",
        "module":module_print_test
    },

    {
        "name":"Module_Threading_Test",
        "module":module_threading_test
    }
]

def time_module_init():
    save_list = []
    for i in time_module_t:
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
        tl = i()
        res = tl.load_init()
        if res < 0:
            logging.error("load module error %s" % (str(i)))
            continue
        logging.info("success load tcp module %s" % (str(i)))
        save_list.append(tl)
    return save_list

def output_module_info():
    fd = open("module.info", "w")
    if fd:
        string = ""
        for i in time_module_t:
            pass
        fd.close()
