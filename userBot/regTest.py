import json
from os import path
from data import users
import logger
from threading import Thread
from time import sleep, time
from pyrogram import Client, filters
import pyrogram

answers = open(path.join('static', 'new_answers.json'),
               'r', encoding='utf-8').read()
answers = json.loads(answers)

WORKER = "SharapaGorg"
MANAGERS = [ 778327202 ]

IGNORE_WORDS = ['Дорог', 'Пока мы рассчитываем']

APP_ID, APP_HASH = users[WORKER]
WARNING_DELAY = 30 # максимально допустимая задержка ответа от бота
RECEIVER = 'TotalDBbot'
DELAY = 6

logger.info(f'LAUNCHED: {WORKER}')

app = Client(WORKER, APP_ID, APP_HASH, workdir='sessions')


def warn_managers(message, managers=MANAGERS):
    for manager in managers:
        app.send_message(manager, message)

def check_delay():
    # проверка задержки ответа от бота
    delay = .125
    while True:
        if update:
            return 

        during = time() - last_sent

        if during > WARNING_DELAY:
            logger.warning(f"Bot is sleeping (DELAY)")
            warn_managers(f"Бот не отвечает уже больше {WARNING_DELAY} секунд!")

            return

        sleep(delay)

last_sent = time()
update = True

@app.on_message(filters.bot)
def get_messages(
        client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):

    global last_sent, update

    last_sent = time()
    update = True

    content = message.text
    if not content:
        content = message.caption

    if not content:
        # если в сообщении нет текста, значит, там только картинка и кнопки
        content = 'picture'

    content = content.split('\n')[0]

    for word in IGNORE_WORDS:
        if word in content:
            return

    suitable_answer = answers.get(content)

    if suitable_answer is None:
        logger.warning(f"Не найдено подходящего ответа: ({content})")
        warn_managers(f"Не найдено подходящего ответа: ({content})")

        return

    sleep(DELAY)

    if 'button' in suitable_answer:
        # значит, вместо текста, нужно нажать на кнопку
        button_index = int(suitable_answer.split(' : ')[1])

        message.click(button_index)
        return

    app.send_message(RECEIVER, suitable_answer)

    checker = Thread(target=check_delay, args=[], daemon=True)
    update = False

    checker.start()

def trigger_receiver():
    # чтобы обрабатывать сообщения от бота сначала нужно ему что-то написать
    sleep(DELAY)

    app.send_message(RECEIVER, "проснись и пой")


Thread(target=trigger_receiver, args=[], name="Trigger").start()

app.run()
