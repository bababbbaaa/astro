import functions
from asyncio import *
from controller import *
from utils import *
import config
import functions

# ----------------------------------------start


@dp.message_handler(commands=['start'])
async def start(message):

    text = message.text
    text1 = text.split()
    id = message.chat.id
    try:
        block_dict.remove(id)
    except:
        pass

    is_user_already_in_handler[id] = True
    text = message.text
    if horoscopeusr.RegUser(inpTelegramID=str(id))[0]:
        if len(text1) == 2:
            try:
                horoscopeusr.ChUserInfo(inpValue=int(
                    text1[1]), inpTelegramID=str(id), inpFieldName="Source_ID")
            except:
                pass

        await wait_until_send_photo(id, config.inter_name, photo=photos["inter_name"])

    elif functions.ListUserName(inpTelegramID=id)[0] == "":
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
        await registartion1(int(id), text)


@dp.message_handler(text="full_delete_user", state="*")
async def full_delete_user(message: Message):
    author = message.from_user.id

    functions.full_delete_user(author)

    await bot.send_message(author, "Аккаунт был успешно удален")



async def registartion1(id: int, text: str):
    # В этой фунции мы просматриваем , что у юзера не заполнено, и вписываем в поле, которое идет раньше при заполнении
    # введенные юзером данные
    '''{"ID","Name",        "is_main",  "BirthTime",
    "Birthday",         "Gender_ID",    'Birthplace',   "DesTime_ID",
    "TimeZone"  "TelegramID",    "RegDate",  "IsActiveBot",
    "Balance",  "IsActiveSub",  "SubscrType_ID",
    "ActiveUntil",  "DateSend", "Source_ID"'''
    # user_options
    user = functions.GetUsers(id)[0]
    if user["Name"] == "":
        if functions.validation_everything(type="Name", text=text)[0] == True:
            horoscopeusr.ChUserInfo(
                inpTelegramID=id, inpFieldName="Name", inpValue=text)

            keyboard = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton(
                text="Мужской", callback_data="ge1nder;1")

            but2 = types.InlineKeyboardButton(
                text="Женский", callback_data="ge1nder;2")

            keyboard.row(but1, but2)

            await wait_until_send_photo(id, config.inter_gender, photo=photos["inter_gender"], reply_markup=keyboard)
            return True
        else:  # Если имя введено некорректно
            await wait_until_send_photo(id, caption=config.inter_name, photo=photos["inter_name"])
    elif user["Gender_ID"] == None:
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(
            text="Мужской", callback_data="ge1nder;1")
        but2 = types.InlineKeyboardButton(
            text="Женский", callback_data="ge1nder;2")
        keyboard.row(but1, but2)
        await wait_until_send_photo(id, config.inter_gender, photo=photos["inter_gender"], reply_markup=keyboard)

    elif user["Birthday"] == None:
        if functions.validation_everything(type="Birthday", text=text)[0] == True:
            horoscopeusr.ChUserInfo(
                inpTelegramID=id, inpFieldName="Birthday", inpValue=text)
            await wait_until_send_photo(id, config.inter_city, photo=photos["inter_city"])
        else:
            await wait_until_send_photo(id, config.inter_date, photo=photos["inter_date"])
    elif user["Birthplace"] == None:

        if functions.validation_everything(type="birth_place", text=text)[0] == True:
            horoscopeusr.ChUserInfo(
                inpTelegramID=id, inpFieldName="Birthplace", inpValue=text)
            await wait_until_send_photo(id, config.inter_time, photo=photos["inter_time"])
        else:
            await wait_until_send_photo(id, config.inter_city, photo=photos["inter_city"])
    elif user["BirthTime"] == None:
        if functions.validation_everything(type="BirthTime", text=text)[0] == True:

            horoscopeusr.ChUserInfo(
                inpTelegramID=id, inpFieldName="BirthTime", inpValue=text)
            keyboard1 = types.InlineKeyboardMarkup()
            keyboard1.row(types.InlineKeyboardButton(text="Утро", callback_data="tim;mor"),
                          types.InlineKeyboardButton(text="Вечер", callback_data="tim;evn"))
            await wait_until_send_photo(id, config.inter_time_option, photo=photos["inter_time_option"], reply_markup=keyboard1)
        else:
            await wait_until_send_photo(id, config.inter_time, photo=photos["inter_time"])
    else:
        await bot.send_message(id, "Выберите в меню то, что вам необходимо")




#---------------------------------------------
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

    else:
        await registartion1(id, text)

# ---------------------------------------------Gender enter field------------------


@dp.callback_query_handler(lambda call: call.data.find("ge1nder") != -1)
async def gender(call):
    try:
        id = call.from_user.id
        data = call.data.split(";")
        text = int(data[1])
        horoscopeusr.ChUserInfo(
            inpValue=text, inpTelegramID=str(id), inpFieldName="Gender_ID")
        message = await wait_until_send_photo(id, config.inter_date, photo=photos["inter_date"])
    except:
        pass
    finally:
        try:
            await bot.delete_message(id, call.message.message_id)
        except:
            pass

# --------------------------------------------mailing time enter


@dp.callback_query_handler(lambda call: call.data.split(";")[0] == "tim")
async def time_select(call):
    try:
        id = call.from_user.id
        data = call.data
        data = data.split(";")
        if data[1] == "mor":
            functions.shedule_time_changer(
                inpTelegramID=id, shedule_time=int(0))

        else:
            functions.shedule_time_changer(
                inpTelegramID=id, shedule_time=int(1))
        horoscopeusr.GenNewUserMess(str(id))
        mes = await wait_until_send(id, "Спасибо, все данные заполнены.\n\nПожалуйста, подождите. Формируем вашу натальную карту, на основе которой будет составляться ваш персональный ежедневный гороскоп.\n\nЕсли вы ошиблись при вводе, то отправьте корректные данные в поддержку @AstroBot_support. Мы исправим информацию, чтобы для вас формировался корректный гороскоп.")
        # Удаляем сообщение, чтобы юзер не игрался с выбором времени
        await bot.delete_message(chat_id=id, message_id=call.message.message_id)
        await wait_until_send(id, config.before_first_horo)
        js = horoscopeproc.GenHourMessAll(
                        11, inpTelegramID=str(id))
        txt = js[0]

        await send_mes(txt)
    except:
        try:
            await wait_until_send(id, "Что-то пошло не так")
        except:
            return 0



