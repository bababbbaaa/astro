from controller import dp, bot
from aiogram.types import *
from aiogram.dispatcher.storage import FSMContext
from .registration import registartion
from utils import *


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


@dp.message_handler(content_types=[ContentType.TEXT])
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

    else:
        await registartion(id, text)

@dp.message_handler(state="*")
async def unknown_handler(message: Message):
    author = message.from_user.id

    await bot.send_message(author, "Выберите в меню то, что вам необходимо")
