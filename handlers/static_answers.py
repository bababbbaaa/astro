
import sys
sys.path.append("../")
import config
from utils import *
from controller import *

@dp.message_handler(commands=['gen_token'])
@show_log_
async def generate_token(message):
    id = message.chat.id

    if id not in config.managers:
        await wait_until_send(id, "Вы не менджер, в доступе отказано")
        return
    else:
        await wait_until_send(
            id, "Введите название паблика,чтобы сгенирировать токен")
        