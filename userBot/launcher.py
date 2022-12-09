import os
from threading import Thread

sessions = os.listdir('sessions')
threads = list()

def launch_bots():
    accounts = set()

    for session in sessions:
        nickname = session.split('.')[0]
        accounts.add(nickname)

    for account in accounts:
        launcher = Thread(
            target=os.system, 
            args=(f'python ./regTest.py {account}', )
            )
        threads.append(launcher)

        launcher.start()

launch_bots()