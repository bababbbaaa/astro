from controller import dp, bot
from aiogram.types import *
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils import *


class UserReg(StatesGroup):
    name = State()
    birth_day = State()
    gender = State()
    birth_time=State()
    destime_id=State()
    birth_place=State()

import functions

@dp.message_handler(state='*', text='cancel')
async def cancel_handler(message: Message, state: FSMContext):
    """
    Allow user to cancel any action
    """

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Действие было прервано', reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(content_types=[ContentType.TEXT])
# async def main(message):
#     id = message.chat.id
#     is_user_already_in_handler[id] = True

#     text = message.text
#     text1 = text.split()4qbgggggg h................................................\\[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[\\\\\\\\\\\\\\\\\\\\2222222222222222444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444#     if horoscopeusr.RegUser(inpTelegramID=str(id))[0]:
#         if len(text1) == 2:
#             try:
#                 horoscopeusr.ChUserInfo(inpValue=int(
#                     text1[1]), inpTelegramID=str(id), inpFieldName="Source_ID")
#             except:
#                 pass

#         await wait_until_send_photo(id, config.inter_name, photo=photos["inter_name"])

#     elif text == "/start":
#         await wait_until_send(
#             id, 'Здравствуйте.\n\nСпасибо,что вернулись в нашего бота. Вы получите гороскоп по расписанию.\n\nЕсли хотите получить его сейчас нажмите на соответствующую кнопку в меню')

#     else:
#         await registartion(id, text)



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


@dp.message_handler(state="*")
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
        await UserReg.name.set()
    if functions.ListUserName(inpTelegramID=id)[0] == "":
        if len(text1) == 2:
            try:
                horoscopeusr.ChUserInfo(inpValue=int(
                    text1[1]), inpTelegramID=str(id), inpFieldName="Source_ID")
            except:
                pass
        mes=await wait_until_send_photo(id, config.inter_name, photo=photos["inter_name"])

        add_message_to_cache(id,mes.message_id)
        await UserReg.name.set()
    elif text == "/start":
        await wait_until_send(
            id, 'Здравствуйте.\n\nСпасибо,что вернулись в нашего бота. Вы получите гороскоп по расписанию.\n\nЕсли хотите получить его сейчас нажмите на соответствующую кнопку в меню')
    else:
        mes=await wait_until_send(id,"Выберите в меню то, что вам необходимо")