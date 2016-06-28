# Script_Collection_Dispatch
Running scripts as module for master program. Developers can ignore some common operating logic, focusing on the development of the monitoring or statistics script process logic, by registering on the master program, the master program is responsible for time and TCP monitoring. As the mean time, it just need to manage one program instead of lot of programs.

Language:Python

Copyright 2016 Ziv Chow.

Version:0.1.0

Usage:
------
1. goto dir 'src'
2. run 'python ScriptHubMain.py start' to start process
3. run 'python ScriptHubMain.py stop' to stop process
4. run 'python ScriptHubMain.py status' to check the process status
5. run 'python ScriptHubMain.py signal [signo]' to send signal_number to all event.
6. run 'python ScriptHubMain.py signal [signo] [module_name]' to send signal_number to event which name is [module_name]

Develop:
------
1.Use time_base.py or tcp_base.py as module to develop new script.
2.Edit regist.py to regist your monitor script into master program.

@1:
-----
1.TimeEventModule Use multi-thread to process timeout event(For var syn with master process).Actually, python threading is only process in 1 cpu, so, if the event need to process a long time, use multi-process in event logic is recommended.
