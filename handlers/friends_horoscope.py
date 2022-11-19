from controller import *
from aiogram.types import *
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import sys
from utils import *
sys.path.append("../")
import horoscopeproc
import horoscopeusr
import functions



class FriendHoroscope(StatesGroup):
    name = State()
    birth_day = State()
    gender = State()
    

#await NewPost.content.set()
#@dp.message_handler(state=NewPost.date)

@dp.message_handler(lambda message: message.text.find("Посмотреть гороскоп другу") != -1)
@dp.message_handler(commands=["gen_user_mes"])
async def gen_user_mess(message):
    id = message.chat.id
    horoscopeusr.RegTmpUser(id)
    is_user_already_in_handler[id] = True
    await FriendHoroscope.name.set()
    await wait_until_send(id,config.friend_block_start)



@dp.message_handler(state=FriendHoroscope.name)
async def enter_name(message: CallbackQuery, state: FSMContext):
    id=message.chat.id
    async with state.proxy() as state_data:
        

        state_data['name'] = message.text

        await FriendHoroscope.gender.set()

        await wait_until_send(id,config.friend_block_insert_gender)
        


@dp.message_handler(state=FriendHoroscope.gender)
async def enter_name(message: CallbackQuery, state: FSMContext):
    id=message.chat.id
    text=message.text.upper()

    if text=="Ж":
        gender=2
    elif text=="М":
        gender=1
    else:
        await wait_until_send(id,"Данные введены неверно, введите их в указанном формате")
        await wait_until_send(id,config.friend_block_insert_gender)
        return 0

    async with state.proxy() as state_data:
        
        
        state_data['gender'] = gender

        await FriendHoroscope.birth_day.set()

        await wait_until_send(id,config.friend_block_insert_Birthday)


@dp.message_handler(state=FriendHoroscope.birth_day)
async def enter_birth(message: CallbackQuery, state: FSMContext):
    id=message.chat.id
    text=message.text

    try:
        date=date_time.strptime(text,"%d.%m.%Y")
    except:
        await wait_until_send(id,"Данные введены неверно, введите их в указанном формате")
        await wait_until_send(id,config.friend_block_insert_Birthday)
        return 0
    async with state.proxy() as state_data:
        date=date_time.strftime(date,"%d.%m.%Y")
        state_data['birth_day'] = date
        
        await wait_until_send(id,config.friend_block_final_message)
        await final_user_registration(message, state,date)




async def final_user_registration(message: CallbackQuery, state: FSMContext,birth_day):
    id=int(message.chat.id)
    
    async with state.proxy() as state_data:
         
        name=state_data["name"]
        gender=int(state_data["gender"])

        horoscopeusr.ChTmpUserInfo(inpTelegramID=id, inpFieldName="Name", inpValue=name)
        horoscopeusr.ChTmpUserInfo(inpTelegramID=id, inpFieldName="Gender_ID", inpValue=gender)
        horoscopeusr.ChTmpUserInfo(inpTelegramID=id, inpFieldName="Birthday", inpValue=birth_day)

        new_user_horo = horoscopeproc.GenTmpUsrMess(id)[0]
    await state.finish()
    text=new_user_horo[2]+"\n\n"+new_user_horo[3]
    await send_friend_horo(id, text)

    
