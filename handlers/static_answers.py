
import sys

sys.path.append("../")
import config
from utils import *
from controller import *



# class Token():
#     name
# @dp.message_handler(commands=["gen_token"])










@dp.message_handler(content_types=['text'])
async def main(message):
    id = message.chat.id
    is_user_already_in_handler[id] = True

    text = message.text
    text1 = text.split()

    if horoscopeusr.RegUser(inpTelegramID=str(id))[0]:
        if len(text1) == 2:
            try:
                horoscopeusr.ChUserInfo(inpValue=int(
                    text1[1]), inpTelegramID=str(id), inpFieldName="Source_ID")
            except:
                pass

        await wait_until_send_photo(id, config.inter_name, photo=photos["inter_name"])

    elif text == "/start":
        await wait_until_send(
            id, 'Здравствуйте.\n\nСпасибо,что вернулись в нашего бота. Вы получите гороскоп по расписанию.\n\nЕсли хотите получить его сейчас нажмите на соответствующую кнопку в меню')

    # else:
        # await registartion1(id, text)

























