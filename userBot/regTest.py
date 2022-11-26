import json
from os import path
import logger
from threading import Thread
from time import sleep, time
from pyrogram import Client, filters
import pyrogram
from sys import argv


def parse_json(file_name):
    data = open(path.join('static', f'{file_name}.json'),
                'r', encoding='utf-8').read()
    return json.loads(data)

answers = parse_json("answers")

WORKER = "SharapaGorg"
MANAGERS = [778327202]

IGNORE_WORDS = ['Дорог', 'Пока мы рассчитываем']

def update_states(status: str, last_message: str = None):
    """"

    Заполняет states.json, чтобы потом можно было смотреть в мониторе, 
    как аккаунты работают

    """

    states = parse_json("states")
    if last_message is None:
        states[WORKER] = (status, states[WORKER][1])
    else:
        states[WORKER] = (status, last_message)

    json.dump(
        states,
        open(path.join('static', 'states.json'), 'w', encoding='utf-8'),
        indent=4,
        sort_keys=True,
        ensure_ascii=False
    )


if len(argv) > 1:
    WORKER = argv[1]

update_states("[yellow]ACTIVATING", "NONE")

# APP_ID, APP_HASH = users[WORKER]
APP_ID, APP_HASH = (14478686, 'c0bafcc69071170e7a7772b506aee680')
WARNING_DELAY = 30  # максимально допустимая задержка ответа от бота
RECEIVER = 'TotalDBbot'
DELAY = 6

logger.info(f'LAUNCHED: {WORKER}')

app = Client(WORKER, APP_ID, APP_HASH, workdir='sessions')

def warn_managers(message, managers=MANAGERS):
    for manager in managers:
        try:
            app.send_message(manager, message)
        except:
            logger.warning(f"Bot must not send any message to this manager : {manager}")


def check_delay():
    # проверка задержки ответа от бота
    delay = .125
    while True:
        if update:
            return

        during = time() - last_sent

        if during > WARNING_DELAY:
            logger.warning(f"Bot is sleeping (DELAY)")
            update_states("[yellow]DELAY")
            # warn_managers(
            #     f"Бот не отвечает уже больше {WARNING_DELAY} секунд!")

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
        # logger.warning(f"Не найдено подходящего ответа: ({content})")
        warn_managers(f"Не найдено подходящего ответа: ({content})")

        return

    sleep(DELAY)

    if 'button' in suitable_answer:
        # значит, вместо текста, нужно нажать на кнопку
        try:
            button_index = int(suitable_answer.split(' : ')[1])

            message.click(button_index)
        except:
            pass

        return

    app.send_message(RECEIVER, suitable_answer)
    update_states("[green]ACTIVATED", suitable_answer[:30])

    checker = Thread(target=check_delay, args=[], daemon=True)
    update = False

    checker.start()


def trigger_receiver():
    # чтобы обрабатывать сообщения от бота сначала нужно ему что-то написать
    sleep(DELAY)
    message = "проснись и пой"

    app.send_message(RECEIVER, message)
    update_states("[green]LAUNCHED", message)


Thread(target=trigger_receiver, args=[], name="Trigger").start()

app.run()
