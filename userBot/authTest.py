"""
Один клиент бесперерывно проверяет, корректно ли работает регистрация
После каждoй регистрации удаляет себя из базы бота и начинает заново
"""

import time
from pyrogram import Client, filters
from pyrogram.types import Message
from threading import Thread
from data import users
import logger
import json
import os, functools
from traceback import format_exc

COMMANDS = [
    'asgard_uga_buga123', 
    'button : 1', 
    '30.10.2000', 
    '12:00', 
    'Махачкала',
    'empty message',
    'full_delete_user_uga_buga',
    'start'
    ]

answers_file = os.path.join('static', 'answers.json')
answers_data = open(answers_file, 'r', encoding='utf-8').read()
config_data = json.loads(answers_data)
answers = config_data.get("Auth")

MANAGERS = config_data.get("MANAGERS")

ANSWERS = {
    'asgard_uga_buga123' : answers["name"],
    'button : 1' : answers["gender"], 
    '30.10.2000' : answers["date"], 
    '12:00' : answers["time"], 
    'Махачкала' : answers["place"],
    'empty message' : answers["default"],
    'full_delete_user_uga_buga' : answers["finish"],
    'start' : answers["start"]
}

INCORRECT_FORMAT = answers["incorrect"]
user = users['SharapaGorg']


USER, APP_ID, APP_HASH = 'SharapaGorg', user[0], user[1]

# CHAT = 'EveryDayAstrologyBot'
CHAT = 'TotalDBbot'
WARNING_DELAY = 30
DELAY = 3

logger.warning("Activating app...")
logger.info(f'Current app: {USER} : [{APP_ID}, {APP_HASH}]')

app = Client(USER, APP_ID, APP_HASH, workdir='sessions')

last_command = 'start'
last_answer = str()

last_reply = time.time()
last_sent = time.time()

def check_interval() -> None:
    delay = .125
    while True:
        if update_checker:
            return

        during = time.time() - last_sent

        if during > WARNING_DELAY:
            logger.warning(f"Delay: {last_command}")
            warning_ = f"```Message : {last_command}\n Бот не отвечает больше 30 секунд!!!\nСЛОМАЛОСЬ!!!```"
            warn_managers(warning_)

            return

        time.sleep(delay)

def warn_managers(message, managers = MANAGERS):
    for manager in managers:
        app.send_message(manager, message)

def key_by_value(value : str) -> "str | None":
    for key in ANSWERS:
        if ANSWERS[key] == value:
            return key

    return None

def authtest(coro):
    @functools.wraps(coro)
    def wrapper(ctx, *args, **kwargs):
        try:
            return coro(ctx, *args, **kwargs)    
        except Exception as e:
            logger.error(f'Exception during the test: {format_exc(e)}')

    return wrapper

update_checker = True
retries = 0

@app.on_message(filters.bot)
@authtest
def get_message(client : Client, message : Message):
    global last_command, last_answer, last_reply, last_sent, update_checker

    last_reply = time.time()
    update_checker = True

    if message.text is not None and 'Дорог' in message.text:
        return

    if message.text != INCORRECT_FORMAT:
        last_answer = message.text
    else:
        warning = f"Something wrong: Message : {last_command} | Answer : " + message.text.replace('\n', ' ')
        logger.warning(warning)
        message = key_by_value(last_answer)

        if message is not None:
            pass

    expected_answer = ANSWERS.get(last_command)
    if last_answer != expected_answer:
        expected_answer_ = expected_answer[30:] if expected_answer is not None else "BUTTONS"
        last_command_ = last_command[30:] if last_command is not None else "BUTTONS"

        
        warn_ = f"```Message : {last_command}\nWarning : Unexpected answer\nAnswer  : {last_command_}\nExpected: {expected_answer_}```"

        logger.warning(warn_.replace('```', ''))

        # warn_managers(error_, [952863788])


    if last_command == COMMANDS[-1]:
        current_command = COMMANDS[0]
    else:
        current_command = COMMANDS[COMMANDS.index(last_command) + 1]

    time.sleep(DELAY)
    
    if 'button' in current_command:
        button_index = int(current_command.split(' : ')[1])

        try:
            message.click(button_index)
        except:
            pass
    else:
        app.send_message(CHAT, current_command)

    last_sent = time.time()

    # check delay
    checker = Thread(target=check_interval, args=[], daemon=True)
    update_checker = False
    checker.start()

    last_command = current_command

def start():
    time.sleep(3)
    app.send_message(CHAT, "full_delete_user_uga_buga")
    app.send_message(CHAT, "something")

logger.info(f"Sender: {USER} | Receiver : {CHAT} ")

Thread(target=start, args=[], name="Auth-Starter").start()

app.run()