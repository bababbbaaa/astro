from datetime import datetime
import os
from telebot.types import *
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from posixpath import abspath
from os.path import join
from calendar import Calendar
from asyncio import *
import time 
import sys
from mics import *
import horoscopeproc as horoscopeproc
sys.path.append("../")
import horoscopeusr as horoscopeusr
import functions
import for_payments
import random
import horoscopeproc as horoscopeproc
import horoscoperr as horoscoperr
def check_format(data : str, time_format : str):
    try:
        datetime.strptime(data, time_format)
        return True
    except Exception as e:
        print(e)
        return False
from rich.console import Console

console = Console()

def create_session():
    LINK ='sqlite:///' + abspath(join('../horoscope.db'))

    engine = create_engine(LINK)
    return sessionmaker(engine)()

def days_in_month(month_index : int, year_index : int) -> int:
    c = Calendar()
    days = c.monthdays2calendar(year_index, month_index)[-1]


    for i in range(len(days) - 1, -1, -1):
        if days[i][0] != 0:
            return days[i][0]

def make_markup(buttons : list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    for button in buttons:
        _button = InlineKeyboardButton(text=button.Source, url=button.Url)
        markup.add(_button)

    return markup

def write_pid():
    RUNNING = 'running.txt'

    with open(RUNNING, 'a') as write_stream:
        write_stream.write(f'{os.getpid()}\n')
async def wait_until_send_photo(id,caption,photo,reply_markup=None,parse_mode=None):
        while True:
            try:
                mes=await bot.send_photo(id,caption=caption,photo=photo,reply_markup=reply_markup,parse_mode=parse_mode)
                return mes
            except Exception as err:
                
                if 'error_code' not in vars(err).keys():
                    return 0
                    
                if err.error_code==429:
                    return err

                elif err.error_code==400:
                    return err
                elif err.error_code==403:
                    horoscopeusr.ChUserInfo(inpValue=0,inpTelegramID=str(id),inpFieldName="IsActiveBot" )
                    return err
                else:
                    return err
async def wait_until_copy(id, forward_id, mes_id, reply_markup=None):
    while True:

        try:
            mes =await bot.copy_message(
                id, forward_id, mes_id, reply_markup=reply_markup)
            return mes
        except Exception as err:
            if 'error_code' not in vars(err):
                return err
            if err.error_code == 429:
                print (err)
                return err
            if err.error_code==400:
                return err
            else:
                return(err)

async def wait_until_send(id, text, reply_markup=None, parse_mode=None, url=None):
    while True:

        try:
            result =await bot.send_message(
                id, text, reply_markup=reply_markup, parse_mode=parse_mode)
            return result
        except Exception as err:
            console.log(err)
            if 'error_code' not in vars(err).keys():
                return err
            if err.error_code == 429:
                print(id)
                print(err)
                return err
            elif err.error_code == 400:
                if url != None:

                    new_user_horo = horoscopeproc.GenTmpUsrMess(id)[0]

                    gender = new_user_horo[4]

                    name = new_user_horo[1]
                    horoscopeusr.RegTmpUser(id)
                    horoscopeusr.ChTmpUserInfo(
                        inpTelegramID=id, inpValue=name, inpFieldName="Name")
                    horoscopeusr.ChTmpUserInfo(
                        inpTelegramID=id, inpValue=gender, inpFieldName="Gender_ID")
                    text = new_user_horo[2]+"\n\n"+new_user_horo[3]
                    # await wait_until_send(id,"Мы состоявляем гороскоп вашему другу, подождите некоторое время")
                    send_friend_horo(id, text)
                    return 0
                    # keyboard=types.InlineKeyboardMarkup()
                    # but1=types.InlineKeyboardButton(text="Отправить другу",url=url)
                    # keyboard.add(but1)

                    # await wait_until_send(id,text,reply_markup=None,parse_mode="html")
                    # time.sleep(0.1)
                    # return(0)
                else:
                    return err
            elif err.error_code == 403:
                print(id,"Это тот, который ломает бота")
                try:
                    mes=await bot.send_message(5127634821,str(id)+" ОН ЛОМАЕТ БОТА")
                    
                    id_of_hack=mes.id
                    mes=await bot.send_message(5127634821,str(id_of_hack)+"айди сообщения, по нему можно определить юзера")
                    await bot.forward_message(952863788,str(id),message_id=mes.id-1)
                    # bot.forward_message()
                except:
                    pass
                return err
            else:
                return err
                # return mes

async def send_natal_map(id):
    try:

        await sleep(10)
        try:
            keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True)
            but=types.KeyboardButton(text="Посмотреть гороскоп другу")
            keyboard.add(but)
            # bot.send_photo(id, photo=open(
            #     'data/'+str(id)+".png", 'rb'), caption="")
            mes = await wait_until_send(
                id, config.after_form_natal_map, parse_mode="html",reply_markup=keyboard)
        except:
            keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True)
            but=types.KeyboardButton(text="Посмотреть гороскоп другу")
            keyboard.add(but)
            mes = await wait_until_send(
                id, config.after_form_natal_map, parse_mode="html",reply_markup=keyboard)
        # name=functions.ListUserName(inpTelegramID=int(id))[0]
        js = horoscopeproc.GenHourMessAll(11, inpTelegramID=str(id))
        txt = js[0]
        today_send = txt[6]
        text = txt[2]+"\n\n"+txt[3]

        await sleep(5)
        await wait_until_send(id, text, parse_mode="html")
    except Exception as error:

        if 'error_code' not in vars(error).keys():
            return 0
        if error.error_code == 429:
            # continue
            pass

async def send_friend_horo(id, text):

    time.sleep(2)
    keyboard = types.InlineKeyboardMarkup()
    text1 = text
    text1 = text1.replace("<b>", "")
    text1 = text1.replace("</b>", "")
    friend_name = horoscopeproc.GenTmpUsrMess(id)[0][1]
    url = "\n\nПривет, "+friend_name+config.friend_horo_text+text1+"\n\nБолее точный гороскоп для тебя по ссылке:https://t.me/EveryDayAstrologyBot?start=1"
    # url="ttps://t.me/share/url?url="+config.bot_name+"&text="+url
    but = types.InlineKeyboardButton(
        text="Отправить другу", switch_inline_query=url)
    keyboard.add(but)
    await wait_until_send(id, text, reply_markup=keyboard,
                    parse_mode="html", url=url)

async def send_mes(posts):
    # print(posts)
    
    first_part=posts[2]
    second_part=posts[3]
    id=posts[0]
    id = int(id)
    date=datetime.strftime(datetime.now()+timedelta(days=1), DATE_FORMAT)
    path="date_pict/"+date+".png"
    pict=open(path,"rb").read()
    time.sleep(5)
    await wait_until_send_photo(id,photo=pict,caption=first_part,parse_mode="html")
    await wait_until_send(id,second_part,parse_mode="html")
    try:
        block_dict.remove(id)
    except:
        pass



async  def show_log_(coro):
    @functools.wraps(coro)
    async def wrapper(ctx, *args, **kwargs):

        if type(ctx) == 'Message':
            try:
                await logger.info(f'{ctx.chat.id} triggered --> {coro.__name__}')
            except:
                await logger.info(f'{ctx.chat.id} triggered --> {coro.__name__}')

        try:
            return coro(ctx, *args, **kwargs)
        except Exception as e:
            logger.error(f'{coro.__name__} catch exception --> {e}')

    return wrapper



async def generate_token_second_part(message):
    id = message.chat.id
    public_name = message.text
    # InsertIntoTable("AstroSchool",(("Category","334234423"),("MessageID",555)),)
    token = random.randint(100000000, 999999999)
    horoscopeproc.InsertIntoTable(inpTbName="Sources", inpValues={
                                    "Name": public_name, "Token": str(token)})
    await wait_until_send(id, "Паблик записан, вот ссылка для "+public_name +
                    " https://t.me/"+config.bot_name[1:]+"?start="+str(token))