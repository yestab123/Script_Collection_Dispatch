#!/usr/bin/python
import socket, select, time, logging
import threading

# Tcp Base Class.All tcp event will insert to this class.
# 1.Tcp Event include Listen event and Connection event.
# Listen Event mean the event which it is listen the tcp connection and wait for connect.
# This is mean it will listen a lot of port in one address depend on the number of tcp events.
# In fact, each tcp event need to listen different port or address.
#
# 2.Connection event will created by Listen event when client connected to the specify port and address.
class epoll_base(object):
    def __init__(self):
        self.listen_list = {}
        self.epoll_fd = select.epoll()

    def event_count(self):
        return len(self.listen_list)

    # conn is from class 'tcp_base'
    def epoll_add(self, conn):
        pass

    def epoll_regist_tcp_base(self, conn, event):
        self.epoll_fd.register(conn.fd, event)
        self.listen_list[conn.fd] = conn

    def epoll_unregist_tcp_base(self, conn):
        self.epoll_fd.unregister(conn.fd)
        if conn.fd in self.listen_list:
            del listen_list[conn.fd]

    def epoll_list(self):
        return self.epoll_fd.poll()

    def epoll_loop(self):
        elist = self.epoll_list()
        for fd, events in elist:
            conn = listen_list[fd]
            if select.EPOLLIN & events:
                conn.tcp_read()
            elif select.EPOLLHUP & events:
                conn.tcp_close()
            elif select.EPOLLOUT & events:
                conn.tcp_write()

# Time Base Class.All time event will insert to this class.
# Time Event mean the event which will run in some time.
class time_run_base(object):
    def __init__(self):
        self.time_list = []
        # time_list_part = {"name":MODULE_NAME, "class":MODULE_CLASS_CASE}

    def event_count(self):
        return len(self.time_list)

    def time_add(self, time_part):
        self.time_list.append(time_part)

    def time_loop(self):
        self.signal_event_loop()
        now_sec = int(time.time())
        for i in self.time_list:
            try:
                if i["class"].time_judge(now_sec):
                    if i["class"].process == None or i["class"].process.is_alive() == False:
                        i["class"].process = threading.Thread(target=i["class"].time_handle, args=(now_sec,))
                        i["class"].process.start()
            except Exception, e:
                logging.error("run time event:%s error %s" % (str(i), str(e)))
                continue

    def signal_event_loop(self):
        for i in self.time_list:
            try:
                if (i["class"].process == None or i["class"].process.is_alive() == False) and (len(i["class"].signo) > 0):
                    for sig in i["class"].signo:
                        logging.debug("%s running signal event %d" % (i["name"], sig))
                        i["class"].signo.remove(sig)
                        i["class"].process = threading.Thread(target=i["class"].time_signal_handle, args=(sig,))
                        i["class"].process.start()
                        break
            except Exception, e:
                logging.error("run thread signal handle (%s) error %s" % (str(i), str(e)))

    def signal_loop(self, signum):
        logging.debug("get user define signal %d" % signum)
        for i in self.time_list:
            try:
                i["class"].signo.append(signum)
                logging.debug("%s add signal %d waiting to run" % (i["name"], signum))
            except Exception, e:
                logging.error("add signum to event queue (sig:%d event:%s) error %s" % (signum, str(i), str(e)))
                continue

    def signal_specify_send(self, signum, module_name):
        logging.debug("get user specify signal(%d) to %s" % (signum, module_name))
        for i in self.time_list:
            if i["name"] == module_name:
                try:
                    i["class"].signo.append(signum)
                    logging.debug("module:%s had add specify signal(%d) in queue" % (module_name, signum))
                    return 0
                except Exception, e:
                    logging.error("add signum to event queue (sig:%d mod:%s) error %s" % (signum, module_name, str(e)))
                    return -1
        return -1
