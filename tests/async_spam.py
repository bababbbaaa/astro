"""

Асинхронная версия спам проверки

Клиенты практически одновременно отправляют различные сообщения

"""

from threading import Thread
from pyrogram import Client
from faker import Faker
import asyncio
import logger
from constants import *
from rich.console import Console

fake = Faker('ru_RU')

COMMANDS = ['/start', 'name', 'М', 'date', 'Место', '12:30', '/support', '/change']

DELAY = 2
THREAD_DELAY = len(COMMANDS) * DELAY
USERS = 3

RECEIVER = 'Tvoi_horoscopeBot'

console = Console()

logo = """

   _____                            ___________              __          
  /  _  \   _________.__. ____   ___\__    ___/___   _______/  |_  ______
 /  /_\  \ /  ___<   |  |/    \_/ ___\|    |_/ __ \ /  ___/\   __\/  ___/
/    |    \\___ \ \___  |   |  \  \___|    |\  ___/ \___ \  |  |  \___ \ 
\____|__  /____  >/ ____|___|  /\___  >____| \___  >____  > |__| /____  >
        \/     \/ \/         \/     \/           \/     \/            \/ 

"""

console.print(f'[bold cyan]{logo}')
logger.info(f'RECEIVER: {RECEIVER}')

async def test(app_name, app_id, app_hash):
    user = Client(app_name, app_id, app_hash, workdir='sessions')

    try:
        await user.start()
    except Exception as e:
        logger.error(e)
        logger.error(f'CANCEL: {app_name}')

        return

    logger.info(f'Bot connected: {app_name}')

    while True:
        for command in COMMANDS:
            try:
                message = command
                if command == 'date':
                    date = fake.date_object()
                    message = f'{date.day}.{date.month}.{date.year}'

                await user.send_message(RECEIVER, message)
                logger.info(f'Command sent: {message}')
                await asyncio.sleep(DELAY)
            except Exception as e:
                logger.error(e)
                logger.warning(f'Waiting : {DELAY}s')
                await asyncio.sleep(DELAY)

for i in range(USERS):
    spam = Thread(target=asyncio.run, args=(test(users[i], APP_IDS[i], APP_HASHS[i]), ))
    spam.start()
