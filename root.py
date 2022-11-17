from threading import Thread
from os import system, listdir, curdir, path, chdir
from utils import logger
from sys import platform, argv


logo = """

  ___      _             _                  ______       _   
 / _ \    | |           | |                 | ___ \     | |  
/ /_\ \___| |_ _ __ ___ | | ___   __ _ _   _| |_/ / ___ | |_ 
|  _  / __| __| '__/ _ \| |/ _ \ / _` | | | | ___ \/ _ \| __|
| | | \__ \ |_| | | (_) | | (_) | (_| | |_| | |_/ / (_) | |_ 
\_| |_/___/\__|_|  \___/|_|\___/ \__, |\__, \____/ \___/ \__|
                                  __/ | __/ |                
                                 |___/ |___/                 

"""

print(logo)

RUNNING = 'running.txt'

def _kill_script(pid):
    system(f'kill {pid}')

def _clear_file(file_name):
    with open(file_name, 'w') as write_stream : pass

def launch():
    logger.warning("Launching AstrologyBot...")

    database = 'databaseInteraction'

    scripts = [
         'bot_version_menu', 
        #'mailing', 
        f'./{database}/subscriptions',
        "check_payment",
        ]

    tables = [
        'posts',
        'buttons',
    ]

    current_dir = listdir(curdir)

    if 'env' not in current_dir:
        logger.warning("Generating virtual enviroment...")
        # if virtual enviroment doesn`t exist generate one
        system("python3 -m venv env")
        logger.info("Done!")

    # activate enviroment
    logger.warning("Activating virtual enviroment...")
    logger.info("Done!")

    # installing dependencies
    logger.warning("Installing dependencies...")

    python = 'python3'

    if platform != 'win32':
        system(f'{python} -m pip install -r requirements.txt ')
    else:
        logger.error("This script is available only for Linux OC")

    logger.info("Done!")

    def execute_script(script_name):
        system(f'{python} {script_name}.py')

    logger.warning("Killing previous session...")

    terminate()

    # clear file
    _clear_file(RUNNING)

    logger.info("Done!")

    logger.warning("Launching scripts...")

    for script in scripts:
        logger.warning(f"Executing {script} script...")
        
        executor = Thread(target=execute_script, args=(script, ), daemon=True, name=f'Astrology-Thread-[{script}]')
        executor.start()

        logger.info("Done!")

    logger.warning("Setupping database tables...")

    chdir(database)

    for table in tables:
        logger.warning(f"Executing {table} table...")
        system(f"python3 {table}.py")

        logger.info('Done!')


def terminate():

    with open(RUNNING, 'r') as rows:
        if not rows.readlines():
            logger.info("No sessions executed")
            return

        logger.warning("Killing current root session...")

        for row in rows:
            _kill_script(row)
    
    # clear file            
    _clear_file(RUNNING)

if len(argv) == 1:
    logger.error("use --launch | --terminate to interact with root.py")
    exit()

if not path.exists(RUNNING):
    logger.warning("Generating running.txt - PIDs...")
    _clear_file(RUNNING)

if argv[1] == '--launch':
    launch()
elif argv[1] == '--terminate':
    terminate()
