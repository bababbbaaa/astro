"""

Один клиент бесперерывно проверяет, корректно ли работает регистрация
После каждый регистрации блокирует бота и начинает заново

"""

import time
from pyrogram import Client, filters
from threading import Thread
from constants import *
import logger
import json
import os, functools

COMMANDS = [
    'asgard_uga_buga123', 
    'М', 
    '30.10.2000', 
    '12:00', 
    'Махачкала',
    'empty message',
    'full_delete_user_uga_buga',
    'start'
    ]

answers_file = os.path.join('..', 'config.json')
answers_data = open(answers_file, 'r', encoding='utf-8').read()
config_data = json.loads(answers_data)
answers = config_data.get("Auth")

MANAGERS = config_data.get("MANAGERS")

ANSWERS = {
    'asgard_uga_buga123' : answers["name"],
    'М' : answers["gender"], 
    '30.10.2000' : answers["date"], 
    '12:00' : answers["time"], 
    'Махачкала' : answers["place"],
    'empty message' : answers["default"],
    'full_delete_user_uga_buga' : answers["finish"],
    'start' : answers["start"]
}

INCORRECT_FORMAT = answers["incorrect"]
USER, APP_ID, APP_HASH = users[2], APP_IDS[2], APP_HASHS[2]

CHAT = 'EveryDayAstrologyBot'
WARNING_DELAY = 30
DELAY = 3

logger.warning("Activating app...")

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
            logger.error(f'Exception during the test: {e}')

    return wrapper

update_checker = True
retries = 0

@app.on_message(filters.bot)
@authtest
def get_message(client, message):
    global last_command, last_answer, last_reply, last_sent, update_checker

    last_reply = time.time()
    update_checker = True

    if message.text is None or 'Дорог' in message.text:
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
        warning = f"Unexpected answer: [{last_command}] : " + last_answer.replace('\n', ' ')
        logger.error(warning)
        
        error_ = f"```Message : {last_command}\nWarning : Unexpected answer\nAnswer  : {last_answer[:30]}\nExpected: {expected_answer[:30]}```"

        warn_managers(error_, [952863788])
        

    if last_command == COMMANDS[-1]:
        current_command = COMMANDS[0]
    else:
        current_command = COMMANDS[COMMANDS.index(last_command) + 1]

    time.sleep(DELAY)
    
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


