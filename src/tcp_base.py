#!/usr/bin/python
import socket, struct, logging

# Tcp Event Listener Base Class
class tcp_base(object):
    def __init__(self):
        self.fd = 0
        self.conn = None
        self.socket = None
        self.addr = None
        self.port = 0

        # Handle Signal Action
    def tcp_signal_handle(self, signo):
        pass

    # Usually this function should be call by load_init(), when it return None, load_init() need to return
    # -1 to tcp_module_init part, and this module will stop to use.
    def creat_listen(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((ip, port))
            sock.listen(5)
            return sock
        except Exception, e:
            logging.error("listen %s:%d error %s" % (ip, port, str(e)))
            return None

    # Accpet Client Connect and return client socket and addr
    def accept_connection(self):
        client, addr = sock.accept()
        client.setblocking(False)
        return client, addr

    # Module Init function.
    # Need to return value to caller,  0 means init success.
    # If return value < 0 , means this module init fail.
    def load_init(self):
        return 0

    # EPOLLIN handle function
    # Need to achieve by module
    def epollin_handle(self):
        pass

    # EPOLLOUT handle function
    # Need to achieve by module
    def epollout_handle(self):
        pass

    # EPOLL ERROR handle function (include hup, close or other error situation)
    # Need to achieve by module
    def epollerr_handle(self):
        pass


# Tcp Event Client which will creat by Tcp Event Listener Base Class
class tcp_client_base(object):
    def __init__(self):
        self.read_buff = {}
        self.write_queue = []
        self.socket = None
        self.addr = None
        self.fd = 0

    def load_init(self, sock, addr):
        self.socket = sock
        self.addr = addr
        self.fd = sock.fileno()
        self.read_buff_init()

    # Handle Signal Action
    def tcp_signal_handle(self, signo):
        pass

    # EPOLLIN handle function
    # Need to achieve by module
    def epollin_handle(self):
        pass

    # EPOLLOUT handle function
    # Need to achieve by module
    def epollout_handle(self):
        pass

    # EPOLL ERROR handle function (include hup, close or other error situation)
    # Need to achieve by module
    def epollerr_handle(self):
        pass

    # Init Recv Tcp Buff
    def read_buff_init(self):
        self.read_buff["buff"] = ""
        self.read_buff["len"] = 4
        self.read_buff["idx"] = 0

    # Send Buff Queue To Client
    def tcp_write(self):
        if len(self.write_queue) > 0:
            for i in self.write_queue:
                buff = i["buff"]
                idx = i["idx"]
                blen = i["len"]
                send_len = self.socket.send(buff[idx:])
                if send_len > 0:
                    i["idx"] += send_len
                    if i["idx"] >= i["len"]:
                        self.write_queue.remove(i)
                    else:
                        break
                elif slen == 0:
                    pass
                elif slen < 0:
                    pass

    # Add Buff that need to send to client in Write_Queue
    def push_to_write(self, buff, buff_len):
        if len(buff) <= 0 or buff_len <= 0:
            return -1
        part = {}
        part["buff"] = buff
        part["idx"] = 0
        part["len"] = buff_len
        self.write_queue.append(part)

    # Add TCP Protocol 4 Bytes Head in the buff that need to send to client
    def send_buff_head_pack(self, buff):
        buff_len = len(buff)
        buff_len += 4
        new_buff = struct.pack(">i", buff_len)
        new_buff += buff

        return new_buff

    # Recv Client Message
    # return 0 means still need to recv more
    # return -1 means this socket was broken, need to close
    # return 1 means finish one package recv, need to parse this buff.
    def tcp_read(self):
        try:
            data = self.socket.recv(self.read_buff["len"] - self.read_buff["idx"])
        except Exception, e:
            # Error and Close
            return -1

        if not data:
            # Close
            return -1

        self.read_buff["idx"] += len(data)
        self.read_buff["buff"] += data
        if self.read_buff["len"] > 4 and self.read_buff["len"] == self.read_buff["idx"]:
            # Finish Recv
            return 1
        elif self.read_buff["idx"] < 4:
            # Still need to recv
            return 0
        elif self.read_buff["idx"] == 4:
            new_len = struct.unpack(">i", self.read_buff["buff"])
            if new_len[0] > 5242880: # 5MB
                # Protocol Too Large Close
                return -1
            self.read_buff["len"] = new_len
            return 0




