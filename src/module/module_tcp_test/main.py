#!/usr/bin/python
import sys, logging
sys.path.append("../..")
from tcp_base import *

class echo_server(tcp_base):
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 8123
        self.name = "Tcp_Echo_Server"
        self.desc = "Tcp Module Testing(Echo Server)"
        self.event = select.EPOLLIN
        self.client = []
        self.flag = 1

    def load_init(self):
        self.socket = self.creat_listen(self.ip, self.port)
        if self.socket == None:
            return -1
        else:
            self.fd = self.socket.fileno()
            return 0

    def epollin_handle(self):
        global tcp_global
        client, addr = self.accept_connection()
        logging.info("%s:accept new client %d %s" % (self.name, client.fileno(), str(addr)))
        node = echo_node()
        node.load_init(client, addr)
        return node, select.EPOLLIN|select.EPOLLOUT|select.EPOLLHUP|select.EPOLLERR

class echo_node(tcp_client_char_base):
    def epollin_handle(self):
        i = self.tcp_read()
        if i == -1:
            self.close()
            logging.debug("%d %s close" % (self.fd, str(self.addr)))
            return -1
        elif i == 1:
            self.push_to_write(self.read_buff["buff"], self.read_buff["idx"])
            self.read_buff_init()
        return 0

    def epollout_handle(self):
        i = self.tcp_write()
        if i == -1:
            self.close()
            logging.debug("%d %s close" % (self.fd, str(self.addr)))
            return -1
        return 0

