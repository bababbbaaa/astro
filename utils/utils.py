import asyncio
from datetime import datetime
import os
from re import X
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from posixpath import abspath
from os.path import join
from calendar import Calendar
from asyncio import *
import time
import sys
from controller import *
import horoscopeusr
import random
from aiogram.types import *
import horoscopeproc
from rich.console import Console
import string
from databaseInteraction import *
from aiogram.types import InlineKeyboardButton
import requests
from datetime import datetime as date_time
from aiogram.dispatcher.storage import FSMContext
from datetime import timedelta
sys.path.append("../")
console = Console()


class InlineButton(InlineKeyboardButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.callback_data = generate_token(32)

    def onClick(self, coro, *args, **kwargs):
        try:
            @dp.callback_query_handler(lambda call: call.data == self.callback_data)
            async def some_coro(call):
                return await coro(call, *args, **kwargs)

        except Exception as e:
            pass
            # logger.error(f'{coro} - handler exception --> {e}')


async def startup(message):
    suggesting_commands = [
    BotCommand(command="send",description="Получить гороскоп сейчас"),
    BotCommand(command="gen_user_mes",description="Гороскоп другу"),
    BotCommand(command="subscribe",description="Подписка"),
    BotCommand(command="support",description="Поддержка"),
    BotCommand(command="change",description="Изменить данные"),
    ]

    await bot.set_my_commands(suggesting_commands)


async def general_info(message: Message):
    author = message.from_user.id
    chat = message.chat
    me = await bot.get_me()

    return author, chat, me


def parse_source_from_excel() -> list:
    """

    ВАЖНО !!!

    Чтобы нормально конвертировать xlsx в xls, зайдите в эксель/либре и пересохраните
    файл в другом формате, в ином случае ничего просто не будет работать, потому что
    структура файла не поменяется, и он будет распознаваться, как xlsx

    """

    import xlrd
    import datetime

    book = xlrd.open_workbook('sources.xls')
    page = book.sheet_by_index(1)
    result = list()

    for rx in range(1, page.nrows - 1):
        error, date, title, code, type_, price = page.row(rx)

        date = datetime.datetime(*xlrd.xldate_as_tuple(date.value,
                                                       book.datemode))

        result.append((date, title.value, code.value,
                      type_.value, int(price.value)))

    return result


def generate_token(length):
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(length))


def alchemy_to_dict(alchemy_object):
    ignore_keys = ['_sa_instance_state']
    result = dict()

    for key in vars(alchemy_object):
        if key in ignore_keys:
            continue

        result[key] = getattr(alchemy_object, key)

    return result

payment_keys=[
    "ID","telegram_id",	"payment_id","user_name",
    "days",	"amount","birth_day","is_reccurent_success","active_until",
    "payed"	,"type_of_payment",	"source_id"	,"payment_date"
            ]
source_keys=[
    "ID","title","code","price","date",
    "type","price_for_person","price_for_customer","profit","amount_of_persons",
    "amount_of_customers","amount_of_persons_who_ended_registr","amount_of_payments","price_for_ended_reg",
]
def _make_tuple(object,keys):
    result=list()
    for key in keys:
        result.append(getattr(object,key))
    return tuple(result)


def alchemy_tuple(objects:list,type:str="payment")->tuple:
    result=list()

    if type=="payment":
        keys=payment_keys
    else:
        keys=source_keys

    result.append(tuple(keys))

    if objects==[]:
        return []
    for object in objects:
        result.append(_make_tuple(object,keys))
    return result
    



def alchemy_list_convert(objects: list) -> list:
    result = list()

    for object in objects:
        result.append(alchemy_to_dict(object))

    return result


def create_session():
    user = 'admin2'
    password = "Sergey123"
    host = '185.209.29.236'
    port = 3306
    database = 'horoscope'
    connection_string = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
        user, password, host, port, database)
    # connection_string = 'sqlite:///' + abspath(join('../horoscope.db'))

    engine = create_engine(
        url=connection_string
    )
    return sessionmaker(engine)()


def markup_row(_markup: types.InlineKeyboardMarkup, array: list):
    _markup.row(*array)


def make_markup_by_list(buttons: list, post_id: str) -> "None | aiogram.types.InlineKeyboardMarkup":
    """

    Cоздает markup из кнопок с ссылками

    buttons : [(title, link)]
    :return: aiogram.types.InlineKeyboardMarkup

    """

    markup = InlineKeyboardMarkup(row_width=2)
    _session = create_session()

    if buttons is None:
        return markup

    for elem in buttons:
        text, link = elem

        if not check_url(link):
            continue

        add_button(_session, post_id, text, link)

        button = InlineButton(text=text, url=link)
        markup.add(button)

    return markup


def parse_buttons(scheme: str) -> "None | list[tuple['title', 'link']]":
    """
    Переводит текст пользователя с описанием кнопок в 
    list[tuple(title, link)], где title - надпись на кнопке, а link - ссылка, заключенная в ней

    """

    if scheme.lower() == 'нет':
        return

    result = list()

    rows = scheme.split('\n')
    for row in rows:
        try:
            title, link = row.split(' - ')

            link = link.lstrip(' ').rstrip(' ')
        except Exception as e:
            print(e)
            continue

        result.append((title, link))

    return result

def get_today():
    today_string = date_time.strftime(date_time.today(), DATE_FORMAT)
    return today_string


def days_in_month(month_index: int, year_index: int) -> int:
    c = Calendar()
    days = c.monthdays2calendar(year_index, month_index)[-1]

    for i in range(len(days) - 1, -1, -1):
        if days[i][0] != 0:
            return days[i][0]


def make_markup(buttons: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    for button in buttons:
        _button = InlineKeyboardButton(text=button.Source, url=button.Url)
        markup.add(_button)

    return markup


def write_pid():
    RUNNING = 'running.txt'

    with open(RUNNING, 'a') as write_stream:
        write_stream.write(f'{os.getpid()}\n')


async def wait_until_send_photo(id, caption, photo, reply_markup=None, parse_mode=None):
    while True:
        try:
            mes = await bot.send_photo(id, caption=caption, photo=photo, reply_markup=reply_markup, parse_mode=parse_mode)
            return mes
        except Exception as err:

            if 'error_code' not in vars(err).keys():
                return 0

            if err.error_code == 429:
                return err

            elif err.error_code == 400:
                return err
            elif err.error_code == 403:
                horoscopeusr.ChUserInfo(inpValue=0, inpTelegramID=str(
                    id), inpFieldName="IsActiveBot")
                return err
            else:
                return err


async def wait_until_copy(id, forward_id, mes_id, reply_markup=None):
    while True:

        try:
            mes = await bot.copy_message(
                id, forward_id, mes_id, reply_markup=reply_markup)
            return mes
        except Exception as err:
            if 'error_code' not in vars(err):
                return err
            if err.error_code == 429:
                print(err)
                return err
            if err.error_code == 400:
                return err
            else:
                return(err)


async def wait_until_send(id, text, reply_markup=None, parse_mode=None, url=None):
    while True:

        try:
            result = await bot.send_message(
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
                print(id, "Это тот, который ломает бота")
                try:
                    mes = await bot.send_message(5127634821, str(id)+" ОН ЛОМАЕТ БОТА")

                    id_of_hack = mes.id
                    mes = await bot.send_message(5127634821, str(id_of_hack)+"айди сообщения, по нему можно определить юзера")
                    await bot.forward_message(952863788, str(id), message_id=mes.id-1)
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
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            but = types.KeyboardButton(text="Посмотреть гороскоп другу")
            keyboard.add(but)
            # bot.send_photo(id, photo=open(
            #     'data/'+str(id)+".png", 'rb'), caption="")
            mes = await wait_until_send(
                id, config.after_form_natal_map, parse_mode="html", reply_markup=keyboard)
        except:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            but = types.KeyboardButton(text="Посмотреть гороскоп другу")
            keyboard.add(but)
            mes = await wait_until_send(
                id, config.after_form_natal_map, parse_mode="html", reply_markup=keyboard)
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


def count_payments():
    session = sessionmaker(engine)()
    rows = session.query(Payment).count()
    session.commit()

    return int(rows)+10000


async def send_friend_horo(id, text):

    await sleep(2)
    keyboard = types.InlineKeyboardMarkup()
    text1 = text
    text1 = text1.replace("<b>", "")
    text1 = text1.replace("</b>", "")
    friend_name = horoscopeproc.GenTmpUsrMess(id)[0][1]
    url = "\n\nПривет, "+friend_name+config.friend_horo_text+text1 + \
        "\n\nБолее точный гороскоп для тебя по ссылке:https://t.me/EveryDayAstrologyBot?start=1"
    # url="ttps://t.me/share/url?url="+config.bot_name+"&text="+url
    but = types.InlineKeyboardButton(
        text="Отправить другу", switch_inline_query=url)
    keyboard.add(but)
    await wait_until_send(id, text, reply_markup=keyboard,
                          parse_mode="html", url=url)


async def send_mes(posts):
    # print(posts)

    first_part = posts[2]
    
    second_part = posts[3]
    id = posts[0]
    id = int(id)
    delta=1
    if "сегодня" in first_part :
        delta=0
    date=datetime.strftime(datetime.now()+timedelta(days=delta), DATE_FORMAT)
    path = "date_pict/"+date+".png"
    pict = open(path, "rb").read()

    await asyncio.sleep(5)
    await wait_until_send_photo(id, photo=pict, caption=first_part, parse_mode="html")
    await wait_until_send(id, second_part, parse_mode="html")
    try:
        block_dict.remove(id)
    except:
        pass


def add_message_to_cache(id, message_id):
    if id not in delete_cache:
        delete_cache[id] = list()
    delete_cache[id].append(message_id)


async def show_log_(coro):
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


