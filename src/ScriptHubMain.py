#!/usr/bin/python
import regist, framerun_base, time, sig_handle, traceback, log, logging
from signal import SIGTERM
import sys, os, atexit

class Daemon:
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork error: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork error: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running...\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        sys.stderr.write("Starting ScriptHubMaster Now...\n")
        self.daemonize()
        self.run()

    def status(self):
        # Show status
        try:
            pf = file(self.pidfile, "r")
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "ScriptHubMaster is running(pid:%d).\n"
            sys.stderr.write(message % pid)
            sys.exit(0)
        else:
            sys.stderr.write("ScriptHubMaster not running\n")
            sys.exit(0)

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running...\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
                sys.stderr.write("ScriptHubMaster(%d) killing success\n" % pid)
                os.remove(self.pidfile)
                sys.exit(0)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                    sys.stderr.write("ScriptHubMaster not running and delete daemon pid file:%s\n" % err)
                    sys.exit(0)
            else:
                print str(err)
                sys.exit(1)
        sys.stderr.write("ScriptHubMaster(%d) killing success" % pid)
        sys.exit(0)


    def signal(self, signal_num):
        """
        Send signal to daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running...\n"
            sys.stderr.write(message % self.pidfile)
            return 

        # Try send signal to the daemon process
        try:
            while 1:
                os.kill(pid, signal_num)
                time.sleep(0.1)
                print "Send signal(%d) to ScripHubMaster(pid:%d) success" % (signal_num, pid)
                return 
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def signal_specify(self, signal_num, module_string):
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running...\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        # Try send signal with specify string to the daemon process
        try:
            while 1:
                if os.path.exists("signal.string"):
                    print "Signal.string still here, wait master to handle last specify signal."
                    time.sleep(1)
                    continue
                else:
                    fd = open("signal.string", "w")
                    fd.write(module_string)
                    fd.close()

                # Wait for system flush the buff
                time.sleep(0.1)
                os.kill(pid, signal_num)
                time.sleep(0.1)
                print "Send signal(%d) to ScripHubMaster(pid:%d) with string(%s) success" % (signal_num, pid,
                                                                                             module_string)
                return
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """


class ScriptHubDaemon(Daemon):
    def run(self):
        print "Daemon Running"
        try:
            # Init Log
            log.log_init("running.log")

            # Set Signal Handle
            sig_handle.signal_regist()

            # Init Time & Tcp module
            time_list = regist.time_module_init()
            tcp_list = regist.tcp_module_init()

            # Init & Insert Time module To Running List
            time_global = framerun_base.time_run_base()
            for i in time_list:
                time_global.time_add(i)

            # Init & Insert Tcp module To Running List
            tcp_global = framerun_base.epoll_base()
            for i in tcp_list:
                tcp_global.epoll_add(i)

            while True:
                if tcp_global.event_count() > 0:
                    tcp_global.epoll_loop()
                if time_global.event_count() > 0:
                    time_global.time_loop()
                if sig_handle.Restart_Flag == 1:
                    # Restart Python Program
                    logging.info("Start to Restart Program")
                    sig_handle.restart_program()
                if len(sig_handle.User_signal) > 0:
                    # Check Specify File
                    if os.path.exists("signal.string"):
                        fd = file("signal.string", 'r')
                        signal_string = fd.read().strip()
                        fd.close()
                        # Send Signal to Specify Process
                        for i in sig_handle.User_signal:
                            time_global.signal_specify_send(i, signal_string)
                            sig_handle.User_signal.remove(i)
                        os.unlink("signal.string")

                    else:
                        for i in sig_handle.User_signal:
                            time_global.signal_loop(i)
                            sig_handle.User_signal.remove(i)

                time.sleep(1)

        except Exception, e:
            error_buff = str(e) + ":" + traceback.format_exc()
            logging.error(error_buff)

if __name__ == '__main__':
    daemon = ScriptHubDaemon("daemon.pid")
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        # elif 'restart' == sys.argv[1]:
        #     daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        elif 'signal' == sys.argv[1]:
            if len(sys.argv) < 3:
                print "usage: %s signal [signal_num]" % sys.argv[0]
                sys.exit(2)
            if len(sys.argv) >= 4:
                signal_num = int(sys.argv[2])
                print "Get specify signal with string (%s)" % sys.argv[3]
                daemon.signal_specify(signal_num, sys.argv[3])
            else:
                signal_num = int(sys.argv[2])
                daemon.signal(signal_num)
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|status|signal [signal_num]|signal [signal_num] [module_name]" % sys.argv[0]
        sys.exit(2)
