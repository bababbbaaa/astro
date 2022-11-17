# from threading import Thread
# import subprocess
# import time
# import datetime
# timeout=6
# import os
# import signal
# start = datetime.datetime.now()
# # subprocess.run("python bot_version_menu.py", shell=True, check=True,timeout=10,output="^C")
# process = subprocess.Popen(["python", "bot_version_menu.py"],shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
# while process.poll() is None:
#         time.sleep(0.1)
#         now = datetime.datetime.now()
#         if (now - start).seconds > timeout:
#             os.kill(process.pid, signal.SIGKILL)
#             os.waitpid(-1, os.WNOHANG)
#             # print (now - start).seconds
#             break
#         print (now - start).seconds
import subprocess

import psutil


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


proc = subprocess.Popen(["python", "bot_version_menu.py"], shell=True)
while True:
    try:
        proc.wait(timeout=600)
        print("restart")
        proc = subprocess.Popen(["python", "bot_version_menu.py"], shell=True)
    except subprocess.TimeoutExpired:
        kill(proc.pid)
    except Exception as err:
        print (err)