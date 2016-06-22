# Script_Collection_Dispatch
Running all statistics and monitor script in one program with python. 通过模块化的方式统一调度统计和监控脚本。

Language:Python

Copyright 2016 Ziv Chow.

Usage:
------
1. goto dir 'src'
2. run 'python ScriptHubMain.py start' to start process
3. run 'python ScriptHubMain.py stop' to stop process
4. run 'python ScriptHubMain.py status' to check the process status
5. run 'python ScriptHubMain.py signal [signo]' to send signal_number to all event.
6. run 'python ScriptHubMain.py signal [module_name] [signo]' to send signal_number to event which name is [module_name]

@1:
-----
1.TimeEventModule Use multi-thread to process timeout event(For var syn with master process).Actually, python threading is only process in 1 cpu, so, if the event need to process a long time, use multi-process in event logic is recommended.
