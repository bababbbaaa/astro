import functions
from asyncio import *
from controller import *
from utils import *
import config
from aiogram.dispatcher.filters.state import State, StatesGroup

import functions

# ----------------------------------------start

class UserReg(StatesGroup):
    name = State()
    birth_day = State()
    gender = State()
    birth_time=State()
    destime_id=State()
    birth_place=State()



@dp.message_handler(text="full_delete_user", state="*")
async def full_delete_user(message: Message):
    author = message.from_user.id
    if author in config.managers:
        functions.full_delete_user(author)

        await bot.send_message(author, "Аккаунт был успешно удален")

async def delete_messages_from_cache(id):
    try:
        for i in range(len(delete_cache[id])):

            message_id=delete_cache[id][i]
            try:
                await bot.delete_message(id,message_id)
            except:
                continue
        del(delete_cache[id])
    except:
        pass


#----------------------------------------начало регистарции

@dp.message_handler(commands=["start"])
async def gen_user_mess(message):
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
        await UserReg.name.set()
    elif functions.ListUserName(inpTelegramID=id)[0] == "":
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

    # else:
    #     await UserReg.name.set()


#---------------------------------ввод имени--------------



@dp.message_handler(state=UserReg.name)
async def enter_name(message: CallbackQuery, state: FSMContext):
    id=message.chat.id

    add_message_to_cache(id,message_id=message.message_id)
    async with state.proxy() as state_data:
        

        state_data['name'] = message.text
        if len(message.text)>254:
            await delete_messages_from_cache(id)
            mes=await wait_until_send_photo(id, config.inter_name, photo=photos["inter_name"])
            add_message_to_cache(id,mes.message_id)
            return 0 
        await UserReg.gender.set()

        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(
            text="Мужской", callback_data="ge1nder;1")

        but2 = types.InlineKeyboardButton(
            text="Женский", callback_data="ge1nder;2")

        keyboard.row(but1, but2)
        await delete_messages_from_cache(id)
        await wait_until_send_photo(id, config.inter_gender, photo=photos["inter_gender"], reply_markup=keyboard)




#-------------------------------------пол

@dp.callback_query_handler(state=UserReg.gender)
@dp.callback_query_handler(lambda call: call.data.find("ge1nder") != -1)
async def enter_gender(call: CallbackQuery, state: FSMContext):
    try:
        id = call.from_user.id
        data = call.data.split(";")
        text = int(data[1])
        async with state.proxy() as state_data:
            state_data['gender'] = text
            await UserReg.birth_day.set()
        message = await wait_until_send_photo(id, config.inter_date, photo=photos["inter_date"])
        add_message_to_cache(id,message_id=message.message_id)
    except:
        pass
    finally:
        try:
            await bot.delete_message(id, call.message.message_id)
        except:
            pass

#-------------------------------------день рождения

@dp.message_handler(state=UserReg.birth_day)
async def enter_birth_day(message: CallbackQuery, state: FSMContext):
    id=message.chat.id
    add_message_to_cache(id,message_id=message.message_id)
    text=message.text
    async with state.proxy() as state_data:
        if functions.validation_everything(type="Birthday", text=text)[0] == True:

            state_data['birth_day'] = text
            await UserReg.birth_place.set()
            await delete_messages_from_cache(id)
            mes=await wait_until_send_photo(id, config.inter_city, photo=photos["inter_city"],)
            add_message_to_cache(id,message_id=mes.message_id)
        else:
            await delete_messages_from_cache(id)
            mes = await wait_until_send_photo(id, config.inter_date, photo=photos["inter_date"])
            add_message_to_cache(id,message_id=mes.message_id)
#-------------------------------------место рождения

@dp.message_handler(state=UserReg.birth_place)
async def enter_birth_place(message: CallbackQuery, state: FSMContext):
    id=message.chat.id
    text=message.text
    add_message_to_cache(id,message_id=message.message_id)
    #----------------------------валидация-------------{

    if len(message.text)>254:
            await delete_messages_from_cache(id)
            mes=await wait_until_send_photo(id, config.inter_date, photo=photos["inter_date"])
            add_message_to_cache(id,mes.message_id)
            return 0 

    #----------------------------валидация-------------}

    async with state.proxy() as state_data:
        state_data["birth_place"]=text
        await UserReg.birth_time.set()
        await delete_messages_from_cache(id)
        mes=await wait_until_send_photo(id, config.inter_time, photo=photos["inter_time"],)
        add_message_to_cache(id,message_id=mes.message_id)


#-------------------------------------время рождения
@dp.message_handler(state=UserReg.birth_time)
async def enter_birth_time(message: CallbackQuery, state: FSMContext):
    id=message.chat.id
    text=message.text
    add_message_to_cache(id,message.message_id)

    #----------------------------валидация-------------{
    if len(message.text)>6:
            await delete_messages_from_cache(id)
            mes=await wait_until_send_photo(id, config.inter_time, photo=photos["inter_time"],)
            add_message_to_cache(id,mes.message_id)
            return 0 
        #----------------------------валидация-------------}


    async with state.proxy() as state_data:
        state_data["birth_time"]=text

        await UserReg.birth_time.set()

        keyboard1 = types.InlineKeyboardMarkup()
        keyboard1.row(types.InlineKeyboardButton(text="Утро", callback_data="tim;mor"),
                        types.InlineKeyboardButton(text="Вечер", callback_data="tim;evn"))
        await delete_messages_from_cache(id)
        mes = await wait_until_send_photo(id, config.inter_time_option, photo=photos["inter_time_option"], reply_markup=keyboard1)
        add_message_to_cache(id,mes.message_id)


@dp.callback_query_handler(state=UserReg.birth_time)
@dp.callback_query_handler(lambda call: call.data.split(";")[0] == "tim")
async def time_select(call: CallbackQuery, state: FSMContext):
    try:
        id = call.from_user.id
        data = call.data
        data = data.split(";")
        if data[1] == "mor":
            text=0

        else:
            text=1
        async with state.proxy() as state_data:
            state_data["destime_id"]=text
            mes = await wait_until_send(id, "Спасибо, все данные заполнены.\n\nПожалуйста, подождите. Формируем вашу натальную карту, на основе которой будет составляться ваш персональный ежедневный гороскоп.\n\nЕсли вы ошиблись при вводе, то отправьте корректные данные в поддержку @AstroBot_support. Мы исправим информацию, чтобы для вас формировался корректный гороскоп.")
            # Удаляем сообщение, чтобы юзер не игрался с выбором времени
            try:
                await bot.delete_message(chat_id=id, message_id=call.message.message_id)
            except:
                pass
            await wait_until_send(id, config.before_first_horo)
            await end_registartion(mes,state,text)

    except:
        try:
            await wait_until_send(id, "Что-то пошло не так")
        except:
            return 0
        


async def end_registartion(message: CallbackQuery, state: FSMContext,destime_id):
    '''{"ID","Name",        "is_main",  "BirthTime",
    "Birthday",         "Gender_ID",    'Birthplace',   "DesTime_ID",
    "TimeZone"  "TelegramID",    "RegDate",  "IsActiveBot",
    "Balance",  "IsActiveSub",  "SubscrType_ID",
    "ActiveUntil",  "DateSend", "Source_ID"'''


    id=message.chat.id

    async with state.proxy() as state_data:
         
        name=state_data["name"]
        gender=int(state_data["gender"])
        birth_day=state_data["birth_day"]
        birth_time=state_data["birth_time"]
        birth_place=state_data["birth_place"]
        kwarks={
            "Name":name,
            "Gender_ID":gender,
            "Birthday":birth_day,
            "DesTime_ID":destime_id,
            "BirthTime":birth_time,
            "Birthplace":birth_place
        }
        horoscopeusr.RegUserFull(inpTelegramID=id,inpValues=kwarks)

        horoscopeusr.GenNewUserMess(str(id))
    # Удаляем сообщение, чтобы юзер не игрался с выбором времени
        js = horoscopeproc.GenHourMessAll(
                        11, inpTelegramID=str(id))
        txt = js[0]
        await state.finish()
        await send_mes(txt)
