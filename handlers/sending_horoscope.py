import functions
from asyncio import *
from controller import *
from utils import *

import config
import sys
sys.path.append("../")


@dp.message_handler(commands=["send"])
async def send(message):
    id=message.chat.id
    try:
        
        js = horoscopeproc.GenHourMessAll(11, inpTelegramID=str(id))
        txt = js[0]
        today_send = txt[6]

    except:
        horoscopeusr.GenNewUserMess(id)
        js = horoscopeproc.GenHourMessAll(11, inpTelegramID=str(id))
        txt = js[0]
        today_send = txt[6]
    
    today_send = txt[6]
    is_active_bot=functions.GetUsers(id)[0]["IsActiveBot"]

    if is_active_bot==0:
        try:
            horoscopeusr.ChUserInfo(inpTelegramID=id,inpFieldName="isActiveBot",inpValue=1)   
        except:
            pass     
    if functions.select_all_active_until_table(id)["days_till_end"]+1<=0:
        horoscopeusr.ChUserInfo(inpTelegramID=id,inpFieldName="SubscrType_ID",inpValue=5)
        horoscopeusr.ChUserInfo(inpFieldName="IsActiveSub",inpTelegramID=id,inpValue=0)
        await subscribe1(message)
        return 0 
                                                                                                                                                                                       
    elif today_send:
        
        text = ""
        text += (js[0][2]+"\n\n"+js[0][3])
        mes = await wait_until_send(id, config.if_horo_sended)

        await send_mes(js[0],)
        return 0
    else:
        text = ""
        text += (js[0][2]+"\n\n"+js[0][3])
        mes = await wait_until_send(
            id, config.if_not_horo_sended)
    # mes=await wait_until_send(id,config.if_horo_sended)

        await send_mes(js[0],)
        return 0





async def subscribe1(message):
    
    id=message.chat.id
    sub_type=functions.GetUsers(id)[0]
    sub_type=int(sub_type["SubscrType_ID"])
    try:
        if id in delete_cache:
            for i in delete_cache[id]:
                bot.delete_message(id, i)
    except:
        pass
    if sub_type==1 or sub_type==2:
        print("here")
        keyboard=types.InlineKeyboardMarkup()
        but1=types.InlineKeyboardButton(text="Активировать подписку", callback_data="2opt;"+str(sub_type))
        keyboard.row(but1)
        print(config.sub_type1_text(id))
        await wait_until_send(id, str(config.sub_type1_text(id)), reply_markup=keyboard)

    if sub_type == 100:
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(
            text="Активировать подписку", callback_data="2opt;"+str(sub_type))
        keyboard.row(but1)
        await wait_until_send(id, config.sub_type3_text(id), reply_markup=keyboard)

    if sub_type == 3:
        keyboard = types.InlineKeyboardMarkup()
        # end_date = str(horoscopeproc.GetSubscrState(id)[0][2])
        but1 = types.InlineKeyboardButton(
            text="Продлить подписку", callback_data="2opt;"+str(sub_type))
        but2 = types.InlineKeyboardButton(
            text="Отказаться от подписки", callback_data="end")
        keyboard.row(but1, but2)
        await wait_until_send(id, config.sub_type3_text(id), reply_markup=keyboard)

    if sub_type == 4 or sub_type == 5:
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(
            text="Активировать подписку", callback_data="2opt;"+str(sub_type))
        keyboard.row(but1)
        await wait_until_send(id, config.sub_type4_text(id), reply_markup=keyboard)


