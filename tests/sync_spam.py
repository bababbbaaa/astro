"""
Синхронная версия спам проверки

Клиенты из списка users поочередно отправляют различные сообщения

"""

from pyrogram import Client
from faker import Faker
import asyncio
import logger
from constants import *

fake = Faker('ru_RU')



COMMANDS = ['/start', '/gen_user_mes', 'М', 'М', 'date']

DELAY = 2
USERS = 3

RECEIVER = 'Tvoi_horoscopeBot'

async def test(app_name, app_id, app_hash):
    user = Client(app_name, app_id, app_hash, workdir='sessions')

    await user.start()
    logger.info(f'Bot connected: {app_name}')

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

    await user.stop()

while True:
    for i in range(USERS):
        asyncio.run(test(users[i], APP_IDS[i], APP_HASHS[i]))