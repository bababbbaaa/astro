import sys

sys.path.append("../")
import config
from utils import *
from controller import *



# class Token():
#     name
# @dp.message_handler(commands=["gen_token"])










@dp.message_handler(commands=["support"])

async def feedback(message):
    try:
        id = message.chat.id

        await wait_until_send(id, config.support)

    except:
        return 1

@dp.message_handler(commands=["change"])

async def change_tim(message):
    try:
        id = message.chat.id
        await wait_until_send(id, config.change_data)

    except:
        return 1























