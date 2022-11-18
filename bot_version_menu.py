import time
import functions
from threading import Thread
import horoscopeusr as horoscopeusr
import config
import for_payments
from posixpath import abspath
import functools
import string
from sqlalchemy import *

from databaseInteraction import *
from datetime import date, timedelta
from datetime import datetime as date_time
from asyncio import *
from rich.console import Console

import horoscopeproc as horoscopeproc

from utils import *

import random
user = {}

from aiogram import *
user = dict()

SUPPORT = config.SUPPORT
TOKEN = config.TOKEN
RUNNING = 'running.text'

LINK = 'sqlite:///' + abspath(join('horoscope.db'))

write_pid()
# async def await wait_until_send_photo(id,caption,photo,reply_markup,parse_mode):
#     while True:
#         try:
#             mes=bot.send_photo(id,caption=caption,photo=photo,reply_markup=reply_markup,parse_mode=parse_mode)
#             return mes
#         except Exception as err:
            
#             if 'error_code' not in vars(err).keys():
#                 return 0
                
#             if err.error_code==429:
#                 return err

#             elif err.error_code==400:
#                 return err
#             elif err.error_code==403:
#                 horoscopeusr.ChUserInfo(inpValue=0,inpTelegramID=str(id),inpFieldName="IsActiveBot" )
#                 return err
#             else:
#                 return err
photos={}
for i in config.photos:
    photos[i]=open(config.photos[i],"rb").read()
async def create_session():
    engine = create_engine(LINK)
    return sessionmaker(engine)()


async  def show_log_(coro):
    @functools.wraps(coro)
    async def wrapper(ctx, *args, **kwargs):

        if type(ctx) == 'Message':
            try:
                logger.info(f'{ctx.chat.id} triggered --> {coro.__name__}')
            except:
                logger.info(f'{ctx.chat.id} triggered --> {coro.__name__}')

        try:
            return coro(ctx, *args, **kwargs)
        except Exception as e:
            logger.error(f'{coro.__name__} catch exception --> {e}')

    return wrapper


console = Console()


async def Get_Data():
    data1 = date.today()
    mon = str(data1.month)
    day = str(data1.day)
    year = str(data1.year)
    if len(mon) < 2:
        mon = "0"+mon
    if len(day) < 2:
        day = "0"+day
    data = day+"."+mon+"."+year
    return(data) 


block_dict=[]
try:
    
    is_user_already_in_handler = {}
    async def wait_until_send_photo(id,caption,photo,reply_markup=None,parse_mode=None):
        while True:
            try:
                mes=bot.send_photo(id,caption=caption,photo=photo,reply_markup=reply_markup,parse_mode=parse_mode)
                return mes
            except Exception as err:
                
                if 'error_code' not in vars(err).keys():
                    return 0
                    
                if err.error_code==429:
                    return err

                elif err.error_code==400:
                    return err
                elif err.error_code==403:
                    handlers.horoscopeusr.ChUserInfo(inpValue=0,inpTelegramID=str(id),inpFieldName="IsActiveBot" )
                    return err
                else:
                    return err
    async def wait_until_copy(id, forward_id, mes_id, reply_markup=None):
        while True:

            try:
                mes = bot.copy_message(
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
                result = bot.send_message(
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

                        new_user_horo = handlers.horoscopeproc.GenTmpUsrMess(id)[0]

                        gender = new_user_horo[4]

                        name = new_user_horo[1]
                        handlers.horoscopeusr.RegTmpUser(id)
                        handlers.horoscopeusr.ChTmpUserInfo(
                            inpTelegramID=id, inpValue=name, inpFieldName="Name")
                        handlers.horoscopeusr.ChTmpUserInfo(
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
                        mes=bot.send_message(5127634821,str(id)+" ОН ЛОМАЕТ БОТА")
                        
                        id_of_hack=mes.id
                        mes=bot.send_message(5127634821,str(id_of_hack)+"айди сообщения, по нему можно определить юзера")
                        bot.forward_message(952863788,str(id),message_id=mes.id-1)
                        # bot.forward_message()
                    except:
                        pass
                    return err
                else:
                    return err
                    # return mes

    async def send_natal_map(id):
        try:

            time.sleep(10)
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
            js = handlers.horoscopeproc.GenHourMessAll(11, inpTelegramID=str(id))
            txt = js[0]
            today_send = txt[6]
            text = txt[2]+"\n\n"+txt[3]

            time.sleep(5)
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
        friend_name = handlers.horoscopeproc.GenTmpUsrMess(id)[0][1]
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

        # except Exception as error:
        #     users = functions.GetUsers(inpTelegramID=str(id),)
        #     name = users[0]["Name"]
        #     horoscopeusr.ChUserInfo(inpValue=0, inpTelegramID=str(id), inpFieldName="IsActiveBot")
    

    TOKEN = config.TOKEN
    delete_cache = {}
    bot = Bot(TOKEN, parse_mode=None)
    async def started_bot():
        me = await bot.get_me()

        logger.info(f"Connection established: {me.first_name}")
    started_bot()
    dp=dispatcher
    class Button(types.InlineKeyboardButton):
        async def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.callback_data = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(32))

        async def onClick(self, coro, *args, **kwargs):
            try:
                @dp.callback_query_handler(lambda call: call.data == self.callback_data)
                async def some_coro(call):
                    return coro(call, *args, **kwargs)

            except Exception as e:
                logger.error(f'{coro} - handler exception --> {e}')


    @dp.message_handler(commands=['gen_token'])
    @show_log_
    async def generate_token(message):
        id = message.chat.id

        if id not in config.managers:
            await wait_until_send(id, "Вы не менджер, в доступе отказано")
            return
        else:
            await wait_until_send(
                id, "Введите название паблика,чтобы сгенирировать токен")
            bot.register_next_step_handler(
                message, generate_token_second_part)

    async def generate_token_second_part(message):
        id = message.chat.id
        public_name = message.text
        # InsertIntoTable("AstroSchool",(("Category","334234423"),("MessageID",555)),)
        token = random.randint(100000000, 999999999)
        horoscopeproc.InsertIntoTable(inpTbName="Sources", inpValues={
                                        "Name": public_name, "Token": str(token)})
        await wait_until_send(id, "Паблик записан, вот ссылка для "+public_name +
                        " https://t.me/"+config.bot_name[1:]+"?start="+str(token))

    @dp.message_handler(commands=['start'])
    @show_log_
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
        if handlers.horoscopeusr.RegUser(inpTelegramID=str(id))[0]:
            if len(text1) == 2:
                if int(text1[1]) == 20:
                    await wait_until_send(id, config.thanks_for_payment)
                try:
                    handlers.horoscopeusr.ChUserInfo(inpValue=int(
                        text1[1]), inpTelegramID=str(id), inpFieldName="Source_ID")
                except:
                    pass

            await wait_until_send_photo(id, config.inter_name,photo=photos["inter_name"])

        elif functions.ListUserName(inpTelegramID=id)[0] == "":
            if len(text1) == 2:
                try:
                    handlers.horoscopeusr.ChUserInfo(inpValue=int(
                        text1[1]), inpTelegramID=str(id), inpFieldName="Source_ID")
                except:
                    pass

            await wait_until_send_photo(id, config.inter_name,photo=photos["inter_name"])

        elif text == "/start":
            await wait_until_send(
                id, 'Здравствуйте.\n\nСпасибо,что вернулись в нашего бота. Вы получите гороскоп по расписанию.\n\nЕсли хотите получить его сейчас нажмите на соответствующую кнопку в меню')

        else:
            await registartion(id,text)

    
    #------------------------------------------Registration-------------------------------------------------

    async def registartion(id:int,text:str):

        '''{"ID","Name",        "is_main",  "BirthTime",
        "Birthday",         "Gender_ID",    'Birthplace',   "DesTime_ID",
        "TimeZone"  "TelegramID",    "RegDate",  "IsActiveBot",
        "Balance",  "IsActiveSub",  "SubscrType_ID",
        "ActiveUntil",  "DateSend", "Source_ID"'''
        #user_options
        user=functions.GetUsers(id)[0]
        if user["Name"] == None:
            if functions.validation_everything(type="Name",text=text)[0]==True:
                handlers.horoscopeusr.ChUserInfo(inpTelegramID=id,inpFieldName="Name",inpValue=text)

                keyboard=types.InlineKeyboardMarkup()
                but1=types.InlineKeyboardButton(text="Мужской",callback_data="ge1nder;1")
                but2=types.InlineKeyboardButton(text="Женский",callback_data="ge1nder;2")
                keyboard.row(but1,but2)
                await wait_until_send_photo(id, config.inter_gender,photo=photos["inter_gender"],reply_markup=keyboard)
                return True
            else:#Если имя введено некорректно
                await wait_until_send_photo(id,caption=config.inter_name,photo=photos["inter_name"])
        if user["Gender_ID"] == None:
            handlers.horoscopeusr.ChUserInfo(inpTelegramID=id,inpFieldName="Name",inpValue=text)

            keyboard=types.InlineKeyboardMarkup()
            but1=types.InlineKeyboardButton(text="Мужской",callback_data="ge1nder;1")
            but2=types.InlineKeyboardButton(text="Женский",callback_data="ge1nder;2")
            keyboard.row(but1,but2)
            await wait_until_send_photo(id, config.inter_gender,photo=photos["inter_gender"],reply_markup=keyboard)

        if user["Birthday"]==None:
            if await functions.validation_everything(type="Birthday",text=text)[0]==True:
                handlers.horoscopeusr.ChUserInfo(inpTelegramID=id,inpFieldName="Birthday",inpValue=text)
                await wait_until_send_photo(id, config.inter_city,photo=photos["inter_city"],reply_markup=keyboard)
        if user["Birthplace"]==None:
            if await functions.validation_everything(type="birth_place",text=text)[0]==True:
                handlers.horoscopeusr.ChUserInfo(inpTelegramID=id,inpFieldName="Birthplace",inpValue=text)
                await wait_until_send_photo(id, config.inter_time,photo=photos["inter_time"],reply_markup=keyboard)
        if user["BirthTime"]==None:
            if await functions.validation_everything(type="BirthTime")[0]==True:
                handlers.horoscopeusr.ChUserInfo(inpTelegramID=id,inpFieldName="BirthTime",inpValue=text)
            
            # await wait_until_send_photo(id, config.inter_city,photo=photos["inter_city"],reply_markup=keyboard)

    # ------------------------------- CHANGE USER INFO -------------------------------
    @dp.message(commands=["full_delete_user_uga_buga"])
    async def full_del(message):
        id = message.chat.id
        functions.full_delete_user(id)
        return None

    @dp.message(commands=["change_user"])
    @show_log_
    async def _change_user_info(message) -> None:
        author = message.chat.id

        if author not in config.managers:
            await wait_until_send(author, "Вы не менджер, в доступе отказано")
            return

        message = await wait_until_send(
            author, "Введите id пользователя: (проверьте тщательно, потому что сейчас проверки правильности введеннего id нет)")
        # bot.register_next_step_handler(message, choose_change_action)

    async def choose_change_action(message):
        author = message.chat.id
        user_id = message.text

        # тут будет проверка наличия пользователя в бд

        markup = types.InlineKeyboardMarkup()

        name = Button(text="Имя")
        gender = Button(text="Пол")
        time = Button(text="Время рассылки")
        cancel = Button(text="Отмена")

        name.onClick(change_user_name, user_id)
        gender.onClick(change_user_gender, user_id)
        time.onClick(change_user_time, user_id)
        cancel.onClick(change_user_cancel)

        markup.row(name, gender)
        markup.row(time, cancel)

        await wait_until_send(
            author, "Что именно хотите поменять у пользователя?", reply_markup=markup)

    async def change_user_name(message, id):
        message = await wait_until_send(
            message.from_user.id, "На какое имя хотите поменять?")
        bot.register_next_step_handler(message, _change_user_name, id)

    async def _change_user_name(message, id):
        handlers.horoscopeusr.ChUserInfo(
            inpValue=message.text, inpTelegramID=str(id), inpFieldName="Name")
        await wait_until_send(message.from_user.id, "Имя было успешно изменено")

    async def change_user_gender(message, id):
        author = message.from_user.id

        markup = types.InlineKeyboardMarkup()

        gender_m = Button(text='М')
        gender_f = Button(text='Ж')
        cancel = Button(text="Отмена")

        gender_m.onClick(_change_user_gender,
                            author=author, id=id, gender_id=1)
        gender_f.onClick(_change_user_gender,
                            author=author, id=id, gender_id=2)
        # cancel.onClick(lambda m: await wait_until_send(
        #     author, "Действие отменено."))

        markup.row(gender_m, gender_f)
        markup.add(cancel)

        await wait_until_send(author, "Выберите пол:", reply_markup=markup)

    @show_log_
    async def _change_user_gender(message, author, id, gender_id):
        handlers.horoscopeusr.ChUserInfo(
            inpValue=gender_id, inpTelegramID=str(id), inpFieldName="Gender_ID")
        await wait_until_send(author, "Пол был успешно изменен")

    @show_log_
    async def change_user_time(message, id):
        author = message.from_user.id

        markup = types.InlineKeyboardMarkup()

        morning = Button(text="Утро")
        evening = Button(text="Вечер")
        cancel = Button(text="Отмена")

        morning.onClick(_change_user_time, author, id, 1)
        evening.onClick(_change_user_time, author, id, 1)

        markup.row(morning, evening)
        markup.add(cancel)

        await wait_until_send(author, "Выберите время рассылки:",
                        reply_markup=markup)

    @show_log_
    async def _change_user_time(message, author, id, time_id):
        functions.shedule_time_changer(
            inpTelegramID=id, shedule_time=time_id)
        await wait_until_send(author, "Время рассылки было успешно изменено")

    async def change_user_cancel(message):
        await wait_until_send(message.from_user.id,
                        "Отмена была успешно инициирована")
        return

    # ---------------------------------------------------------------------------------------------

    async def markup_row(_markup: types.InlineKeyboardMarkup, array: list):
        _markup.row(*array)

    async def turn_calendar_page(message, current_date, months: int):
        step_month = current_date.month + months
        step_year = current_date.year

        if step_month == 13:
            step_month = 1
            step_year += 1

        if step_month == 0:
            step_month = 12
            step_year -= 1

        current_month = days_in_month(step_month, step_year)

        if months == -1:
            current_month = -current_month

        new_date = current_date + timedelta(days=current_month)

        show_calendar(message, new_date)
        bot.delete_message(chat_id=message.from_user.id,
                            message_id=message.message.id)

    @show_log_
    async def calendar_handler(message, date: str, post: bool):
        if date is None:
            return

        if post:
            render_posts(message, date, False)
            return

        create_post_(message, date)

    @dp.message(commands=["calendar"])
    @show_log_
    async def show_calendar(message, handled_date=None) -> None:
        try:
            author = message.chat.id
        except:
            author = message.from_user.id

        if author not in config.managers:
            await wait_until_send(author, "Вы не менджер, в доступе отказано")
            return

        today = date.today()

        dates = dict()
        posts = get_posts(create_session())

        for post in posts:
            post_date = post.Date

            if dates.get(post_date) is None:
                dates[post_date] = 0

            dates[post_date] += 1

        if handled_date is not None:
            today = handled_date

        calendar = Calendar()
        weeks = calendar.monthdays2calendar(today.year, today.month)

        markup = types.InlineKeyboardMarkup(row_width=8)

        previous = Button(text="<-----------")
        next = Button(text="----------->")

        previous.onClick(turn_calendar_page, today, -1)
        next.onClick(turn_calendar_page, today, 1)

        markup.row(previous, next)

        monday_ = Button(text="Пн")
        tuesday_ = Button(text="Вт")
        wednesday_ = Button(text="Ср")
        thursday_ = Button(text="Чт")
        friday_ = Button(text="Пт")
        saturday_ = Button(text="Сб")
        sunday_ = Button(text="Вс")

        markup.row(monday_, tuesday_, wednesday_,
                    thursday_, friday_, saturday_, sunday_)

        for week in weeks:
            markup_row_ = list()
            for day in week:
                number = day[0]
                formatted_date = None
                if number:
                    day_date = today.replace(day=number)
                    formatted_date = date_time.strftime(
                        day_date, DATE_FORMAT)

                    if formatted_date in dates:
                        number = f"{number} ({dates[formatted_date]})"

                number = str(number)
                button_width = 10

                button = Button(text = number)
                button.width = button_width
                button.onClick(calendar_handler,
                                formatted_date, '(' in number)

                markup_row_.append(button)

            markup_row(markup, markup_row_)

        await wait_until_send(
            author, f"Выбранная дата: *{months[today.month - 1]}* *{today.year}* Года", reply_markup=markup, parse_mode="Markdown")

    # ------------------------------- MANAGERS COMMANDS -------------------------------

    @dp.message(commands=["manager_access"])
    @show_log_
    async def _manager_access(message) -> None:
        try:
            author = message.chat.id
        except:
            author = message.from_user.id

        try:
            bot.delete_message(message.from_user.id, message.message.id)
        except:
            pass

        if author not in config.managers:
            await wait_until_send(author, "Вы не менджер, в доступе отказано")
            return

        handler = 'POST_MENU'
        markup = types.InlineKeyboardMarkup()

        create = types.InlineKeyboardButton(
            "Создать", callback_data=f"{handler};CREATE")
        choice = types.InlineKeyboardButton(
            "К постам", callback_data=f"{handler};POSTS")
        cancel = Button(text="Отмена")

        cancel.onClick(cancel_manager)

        markup.row(cancel, create)
        markup.add(choice)

        await wait_until_send(author, "*МЕНЮ*",
                        parse_mode="Markdown", reply_markup=markup)

    @show_log_
    async def cancel_manager(message):
        bot.delete_message(message.from_user.id, message.message.id)

        await wait_until_send(
            message.from_user.id, "*Вызвать* календарь: /calendar", parse_mode="Markdown")

    @dp.callback_query_handler(lambda call: call.data.split(';')[0] == 'POST_MENU' and call.data.split(';')[1] == 'POSTS')
    @show_log_
    async def choose_post(message):
        author = message.from_user.id
        bot.delete_message(author, message.message.id)

        markup = types.InlineKeyboardMarkup()
        dates = set()

        posts_in_date = dict()

        for post in get_posts(create_session()):
            date = post.Date

            if date not in posts_in_date:
                posts_in_date[date] = int()

            posts_in_date[date] += 1

            dates.add(date)

        for date in dates:
            button = Button(text=f"{date} ({posts_in_date[date]} поста)")
            button.onClick(render_posts, date=date)

            markup.add(button)

        await wait_until_send(
            author, "Выберите дату, на которую был запланирован пост", reply_markup=markup)

    @show_log_
    async def render_posts(call, date, delete_message: bool = True):
        author = call.from_user.id

        if delete_message:
            bot.delete_message(author, call.message.id)

        database = create_session()
        posts = get_posts(database, date=date)

        markup = types.InlineKeyboardMarkup()
        back_handler = 'POST_MENU'

        back = types.InlineKeyboardButton(
            text="<- Назад", callback_data=f'{back_handler};BACK')
        cancel = Button(text="Отмена")
        create = Button(text="Создать")

        cancel.onClick(cancel_manager)
        create.onClick(create_post_, date, True)

        markup.row(back, cancel)
        markup.add(create)

        for post in posts:
            category = post.Time if post.Category != 'person' else "Рубрика"
            category += f" ({post.FirstRow}...)"

            button = Button(text=category)
            button.onClick(_show_post_, post.PostID)

            markup.add(button)

        await wait_until_send(author, date, reply_markup=markup)

    @show_log_
    async def _show_post_(message, post_id):
        show_post(message, post_id)
        bot.delete_message(message.from_user.id, message.message.id)

        author = message.from_user.id
        markup = types.InlineKeyboardMarkup()

        edit = Button(text="Изменить")
        delete = Button(text="Удалить")
        cancel = Button(text="Отмена")
        back = Button(text="<-- Назад")

        edit.onClick(choose_post, post_id)
        delete.onClick(_delete_post, post_id)
        cancel.onClick(cancel_manager)

        markup.row(back, cancel)
        markup.row(edit, delete)

        await wait_until_send(author, "Выберите действиe:", reply_markup=markup)

    async def ask_time(author, is_heading: bool, date: str):

        message = await wait_until_send(
            author, "Напишите время отправки сообщения в формате: часы:минуты")

        bot.register_next_step_handler(
            message, check_time, is_heading, date)

    async def ask_date(author, time, is_heading: bool, date: str):
        if not date or date is None:
            message = await wait_until_send(
                author, "Напишите дату отправку сообщения в формате день.месяц.год")

            bot.register_next_step_handler(
                message, check_date, time, is_heading)
        else:
            date = date_time.strptime(date, DATE_FORMAT)
            ask_content(author, date, time, is_heading)

    async def ask_content(author, date, time, is_heading: bool):
        message = await wait_until_send(
            author, "Введите содержимое поста, которое нужно будет отправить")

        bot.register_next_step_handler(
            message, ask_buttons, author, date, time, is_heading)

    @show_log_
    async def ask_buttons(message, author, date, time, is_heading: bool):
        buttons = await wait_until_send(
            message.chat.id, "Хотите добавить кнопки в пост?\nЕсли *да*, то опишите кнопки в формате\n ``` Кнопка 1 - ссылка\n Кнопка 2 - ссылка```\n\nЕсли *нет*, напишите 'нет'", parse_mode="Markdown")

        bot.register_next_step_handler(
            buttons, add_buttons, author, date, time, is_heading, message,)
    @show_log_
    async def add_buttons(buttons, author, date, time, is_heading: bool,post):
        content = str()
        markup = types.InlineKeyboardMarkup()

        _session = create_session()
        if buttons.text==None:
            text=buttons.caption
        else:
            text=buttons.text
        if text != 'нет':
            for row in buttons.text.split('\n'):
                if len(row.split('-')) < 2:
                    continue

                source, link = row.split('-')

                source = source.lstrip(' ').rstrip(' ')
                link = link.replace(' ', '')

                add_button(_session, post.id, source, link)

                button = Button(text=source, url=link)
                markup.add(button)

        mes=await wait_until_send(id=post.from_user.id,text="Если необходимо отправить выбранной аудитории, то перенесите файл с телеграмм айди. Если такой необходимости нет, напишите 'нет'")
        bot.register_next_step_handler(mes,ask_file,buttons,author,date,time,is_heading,post)
    
    async def ask_file(message,buttons, author, date, time, is_heading: bool,post):
        print(message)
        if message.content_type=="text":
            if not message.text=="нет":
                mes=await wait_until_send(id=message.chat.id,text="Либо ответьте нет, либо отправьте файл в формате txt")
                bot.register_next_step_handler(mes,ask_file,buttons,author,date,time,is_heading,post)
            else:
                path=None
            
        else:
            # file=get_file
            file_info = bot.get_file(message.document.file_id)
        # file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            name=Get_Data()+"_"+str(random.randint(100000000, 999999999))
            # os.
            with open("post_files/"+name+".txt","wb") as file:
                file.write(downloaded_file)
            path="/post_files/"+name+".txt"

        send_post(buttons,author,date,time,is_heading,post,path)
        # bot.register_next_step_handler(
        #     buttons, send_post, author, date, time, is_heading,file_info, message)
    @show_log_
    async def send_post(buttons, author, date, time, is_heading: bool, post: str,path:str):
        try:
            content = str()
            markup = types.InlineKeyboardMarkup()

            _session = create_session()

            if buttons.text != 'нет':
                for row in buttons.text.split('\n'):
                    if len(row.split('-')) < 2:
                        continue

                    source, link = row.split('-')

                    source = source.lstrip(' ').rstrip(' ')
                    link = link.replace(' ', '')

                    # add_button(_session, post.id, source, link)

                    button = Button(text=source, url=link)
                    markup.add(button)

            content += '*Мета данные*:\n'
            content += f'*Рубрика* {is_heading}\n'
            content += f'*Дата*: {date.year} год, {months[date.month - 1]}, {date.day}-е число\n'
            content += f'*Время*: {time.hour} *часов* {time.minute} *минут*\n'
            content += '*Вызвать* календарь: /calendar'

            db_time = f'{time.hour}:{time.minute}'
            db_date = f'{date.day}.{date.month}.{date.year}'

            db_date = date_time.strptime(db_date, DATE_FORMAT)

            month = str(db_date.month)

            day = str(db_date.day)
            if len(month) == 1:
                month = "0"+str(month)
            if len(day) == 1:
                day = "0"+str(day)
            db_date = str(day)+"."+str(month)+"."+str(db_date.year)
            db_message = post.id
            db_author = post.chat.id
            db_category = "person" if is_heading else "none"

            db_first_row = "only picture"

            if post.text:
                db_first_row = post.text[:25]

            if post.caption:
                db_first_row = post.caption[:25]

            await wait_until_send(author, content, parse_mode='Markdown')
            await wait_until_copy(author, author, post.id, reply_markup=markup)

            database = create_session()
            add_post(
                database,
                category=db_category,
                managerId=db_author,
                postId=db_message,
                date=db_date,
                time=db_time,
                first_row=db_first_row,
                path=path)
        except:
            await wait_until_send(author,"Ошибка где-то")
            return(0)

    # ------------------------------- MANAGER HANDLERS -------------------------------

    months = ['Январь', "Февраль", "Март", "Апрель", "Май", "Июнь",
                "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    DATE_FORMAT = '%d.%m.%Y'
    TIME_FORMAT = '%H:%M'

    @show_log_
    async def _delete_post(call, post_id):
        author = call.from_user.id

        await wait_until_send(author, "Пост, который был удален:")
        await wait_until_copy(author, author, post_id)

        # адский костыль из-за убогости библиотеки
        # (хорошо, что хоть работает)
        _session = create_session()

        post = get_post(_session, post_id)
        delete_post(_session, post)

    async def show_post(call, post_id):
        author = call.from_user.id
        buttons = get_buttons(create_session(), post_id)
        markup = make_markup(buttons)                

        await wait_until_copy(author, author, post_id, reply_markup=markup)

    async def choose_post(call, post):
        author = call.from_user.id

        handler = 'POST_EDIT'
        markup = types.InlineKeyboardMarkup()

        time = types.InlineKeyboardButton(
            "Время", callback_data=f'{handler};TIME;{post}')
        date = types.InlineKeyboardButton(
            "Дату", callback_data=f'{handler};DATE;{post}')
        content = types.InlineKeyboardButton(
            "Содержимое", callback_data=f'{handler};CONTENT;{post}')
        type = types.InlineKeyboardButton(
            "Тип поста", callback_data=f'{handler};TYPE;{post}')

        buttons = types.InlineKeyboardButton(
            "Кнопки", callback_data=f'{handler};BUTTONS;{post}')
        
        markup.row(time, date)
        markup.row(content, type)
        markup.add(buttons)

        await wait_until_send(
            author, "Что именно вы хотите поменять?", reply_markup=markup)

    @dp.callback_query_handler(func=lambda call: call.data.split(";")[0] == "POST_EDIT")
    async def edit_post_data(call):
        author = call.from_user.id
        handler, field, postID = call.data.split(';')

        database = create_session()
        post = get_post(database, postID)
        database.close()

        time_ = post.Time
        date_ = post.Date
        type_ = post.Category

        if field == 'TIME':
            message = await wait_until_send(
                author, f"*Время*, установленное сейчас (часы, минуты): {time_}\n*Введите* новое:", parse_mode='Markdown')
            bot.register_next_step_handler(message, change_post_time, post)

        if field == 'DATE':
            message = await wait_until_send(
                author, f"*Дата*, установленная сейчас (день, месяц, год): {date_}\n*Введите* новую:", parse_mode='Markdown')
            bot.register_next_step_handler(message, change_post_date, post)

        if field == 'TYPE':
            change_post_field(call, post, "Category")

        if field == 'BUTTONS':
            current_buttons = get_buttons(create_session(), postID)
            markup = make_markup(current_buttons)

            await wait_until_send(author, "Текущее содержимое: ", reply_markup=markup)
            
            for button in current_buttons:
                await wait_until_send(author, '``` ' + button.Source + ' - ' + button.Url + '```', parse_mode='Markdown')

            answer = await wait_until_send(author, "Введите новое содержимое: ")

            bot.register_next_step_handler(answer, change_post_buttons, post)

        if field == 'CONTENT':
            await wait_until_send(
                author, f"*Содержимое*, установленное сейчас: \n", parse_mode='Markdown')
            await wait_until_copy(author, author, post.PostID)
            message = await wait_until_send(
                author, "*Введите* новое содержимое: ", parse_mode="Markdown")

            bot.register_next_step_handler(
                message, change_post_field, post, "PostID")

    @show_log_
    async def change_post_buttons(message, post):
        buttons = message.text.split('\n')
        markup = types.InlineKeyboardMarkup()

        _session = create_session()
        current_buttons = get_buttons(_session, post.ID)

        for but in current_buttons:
            delete_button(_session, but)

        for row in buttons:
            if len(row.split('-')) < 2:
                continue

            source, link = row.split('-')

            source = source.lstrip(' ').rstrip(' ')
            link = link.replace(' ', '')

            add_button(_session, post.PostID, source, link)

            _button = Button(text=source, url=link)
            markup.add(_button)

        await wait_until_send(message.from_user.id, "Новые кнопки:", reply_markup=markup)            

                

    async def change_post_time(message, post):
        input_format = message.text

        try:
            time = date_time.strptime(input_format, TIME_FORMAT)

            change_post_field(message, post, "Time")
        except Exception as e:
            await wait_until_send(message.from_user.id,
                            "Неверный формат времени. Попробуйте еще раз\n")

            message = await wait_until_send(
                message.from_user.id, f"*Время*, установленное сейчас (часы, минуты): {post.Time}\n*Введите* новое:", parse_mode='Markdown')
            bot.register_next_step_handler(message, change_post_time, post)

    async def change_post_date(message, post):
        input_format = message.text

        try:
            date = date_time.strptime(input_format, DATE_FORMAT)

            change_post_field(message, post, "Date")
        except Exception as e:
            await wait_until_send(message.from_user.id,
                            "Неверный формат даты. Попробуйте еще раз\n")

            message = await wait_until_send(
                message.from_user.id, f"*Дата*, установленная сейчас (день, месяц, год): {post.Date}\n*Введите* новую:", parse_mode='Markdown')
            bot.register_next_step_handler(message, change_post_date, post)

    async def change_post_field(message, post, field):
        author = message.from_user.id

        post_id = post.PostID

        if field == 'PostID':
            _field = message.id
        elif field == 'Category':
            _field = "person" if post.Category == "none" else "none"
        elif field == 'Time':
            _field = message.text.replace('.', ':')
        else:
            _field = message.text

        first_row = 'only picture'

        if message.text:
            first_row = message.text[:25]
        elif message.caption:
            first_row = message.caption[:25]

        if field == 'PostID':
            setattr(post, "FirstRow", first_row)

            _session = create_session()
            for _button in get_buttons(_session, post_id):
                update_button(_session, _button.ID, post_id=message.id)

        if field != 'Category':
            await wait_until_send(
                author, f"Содержимое поста было успешно заменено на:\n{message.text}")
        else:
            new_type = "Рубрика" if post.Category != "person" else "Гороскоп"
            await wait_until_send(
                author, f"Содержимое поста было успешно заменено на:\n*{new_type}*", parse_mode='Markdown')

        setattr(post, field, _field)

        database = create_session()
        update_post(database, post_id, post.PostID,
                    post.Category, post.Time, post.Date, post.FirstRow)

    @dp.callback_query_handler(func=lambda call: len(call.data.split(';')) > 1 and call.data.split(';')[1] == 'CANCEL')
    async def cancel(call) -> None:
        await wait_until_send(call.from_user.id,
                        "Действие было успешно отменено")
        return

    @dp.callback_query_handler(func=lambda call: call.data.split(";")[0] == "POST_MENU" and call.data.split(';')[1] == 'BACK')
    async def back_to_menu(call):
        bot.delete_message(call.from_user.id, call.message.id)

        _manager_access(call)

    @dp.callback_query_handler(func=lambda call: call.data.split(";")[0] == "POST_MENU" and call.data.split(';')[1] == 'CREATE')
    @show_log_
    async def create_post_(call, date: str = None, delete_message: bool = False) -> None:
        """ Создание постов, позже отправляющихся в различные каналы по определенному графику """
        id = call.from_user.id

        if delete_message:
            bot.delete_message(id, call.message.id)

        # Вопрос : Это рубрика?
        handler = 'IS_HEADING'
        markup = types.InlineKeyboardMarkup()

        yes = types.InlineKeyboardButton(
            "Да", callback_data=f'{handler};YES;{date}')
        no = types.InlineKeyboardButton(
            "Нет", callback_data=f'{handler};NO;{date}')

        back = Button(text="<-- Назад")
        cancel = Button(text="Отмена")

        if date:
            back.onClick(render_posts, date)
        else:
            back.onClick(_manager_access)

        cancel.onClick(cancel_manager)

        markup.row(yes, no)
        markup.row(back, cancel)

        await wait_until_send(id, "Пост является рубрикой?", reply_markup=markup)

    async def check_time(message, is_heading: bool, date: str):
        input_format = message.text
        if date=="None":
            date=None
        try:
            # correct format
            time = date_time.strptime(input_format, TIME_FORMAT)

            ask_date(message.chat.id, time, is_heading, date)
        except Exception as e:
            logger.error(e)
            # incorrect format
            await wait_until_send(
                message.chat.id, "Неверный формат времени. Попробуйте еще раз\n")
            ask_time(message.chat.id, is_heading, date)

    async def check_date(message, time, is_heading: bool):
        input_format = message.text

        try:
            # correct format
            date = date_time.strptime(input_format, DATE_FORMAT)

            date = date.replace(hour=time.hour, minute=time.minute + 1)

            current = datetime.now()
            current = current.replace(second=0)

            if date.timestamp() < current.timestamp():
                raise Exception("Incorrect date")

            ask_content(message.chat.id, date, time, is_heading)
        except Exception as e:
            # incorrect formatf
            await wait_until_send(message.chat.id,
                            "Неверный формат даты. Попробуйте еще раз\n")
            bot.register_next_step_handler(message,ask_date, time, is_heading)

    @dp.callback_query_handler(func=lambda call: call.data.split(";")[0] == "IS_HEADING")
    async def handle_first(call):
        """ Обработчик выбора (Это Рубрика?)"""
        author = call.from_user.id
        data = call.data.split(";")[1]
        date = call.data.split(';')[2]

        if data == 'YES':
            await wait_until_send(author, "Пост является рубрикой : записано")

            # время не спрашивается
            ask_date(author, datetime.now(), True, date)

        if data == 'NO':
            await wait_until_send(author, "Пост не является рубрикой : записано")

            # время спрашивается
            ask_time(author, False, date)

    # ---------------------------------------------------------------------------------------------

    @dp.message(func=lambda message: message.text.find("Посмотреть гороскоп другу") != -1)
    @dp.message(commands=["gen_user_mes"])
    @show_log_
    async def gen_user_mess(message):

        id = message.chat.id
        handlers.horoscopeusr.RegTmpUser(id)
        is_user_already_in_handler[id] = True
        text = message.text
        # try:
        # or functions.ListUserName(inpTelegramID=id)[0]==None:
        if handlers.horoscopeusr.RegUser(inpTelegramID=str(id))[0] == True:
            # print(horoscopeusr.RegUser(inpTelegramID=str(id))[0])

            await wait_until_send(id, config.inter_name)

            bot.register_next_step_handler (message, validation_name, message.id)
        elif functions.ListUserName(inpTelegramID=id)[0] == "":

            await wait_until_send(id, config.inter_name)

            bot.register_next_step_handler (message, validation_name, message.id)
        else:
            us = functions.GetUsers(id)[0]
            if us["Name"] == None:

                await wait_until_send(id, config.inter_name)

                bot.register_next_step_handler(
                        message, validation_name, message.id)
            elif us["Birthday"] == None:
                # Введите город,в котором вы родилисьы
                await wait_until_send(id, config.inter_date)

                bot.register_next_step_handler(
                        message, validation_birth, message.id)
            elif us["Birthplace"] == None:
                await wait_until_send(message.chat.id, config.inter_city)

                bot.register_next_step_handler(
                        message, validation_city, message.id)
            elif us["RegDate"] == None:
                keyboard1 = types.InlineKeyboardMarkup()
                keyboard1.row(types.InlineKeyboardButton(text="Утро", callback_data="tim;mor"),
                                types.InlineKeyboardButton(text="Вечер", callback_data="tim;evn"))

                mes = await wait_until_send(
                    id, config.inter_time_option, reply_markup=keyboard1)
            else:
                # await wait_until_send(id,"Выберите в меню то, что вам необходимо")

                # horoscopeusr.DelTmpUser(id)
                # user_info=horoscopeusr.GetTmpUserInfo(id)
                # if user_info["Name"]!=None and user_info["Gender_ID"]!=None and user_info["Birthday"]!=None:
                await wait_until_send(id, config.friend_block_start)
                # elif user_info["Name"]==None:
                #     await wait_until_send(id,"Чтобы мы могли отправить гороскоп вашему другу, нам необходимо знать его данные\nВведите имя вашего друга")

                validation_circle(message)
        # except Exception as e:
            #     print(e)
            #     # horoscopeusr.DelTmpUser(id)
            #     # horoscopeusr.RegTmpUser(id)
            # #     try:
            #     await wait_until_send(id, "Что-то пошло не так")
            # except:
            #     return 0
                # validation_circle(message)
        # bot.register_next_step_handler(message,validation_circle)

    async def validation_circle(message):
        id = message.chat.id
        text = message.text
        is_user_already_in_handler[id] = True
        if text.find("/") != -1 and text != "/gen_user_mes":
            main(message)
            return 0
        # print(horoscopeusr.GetTmpUserInfo(id))

        user_info = handlers.horoscopeusr.GetTmpUserInfo(id)[3]
        if user_info["Name"] == None:

            bot.register_next_step_handler(
                message, full_validation, "Name")
        elif user_info["Gender_ID"] == None:
            await wait_until_send(id, config.friend_block_insert_gender)

            bot.register_next_step_handler(
                message, full_validation, "Gender_ID")
        elif user_info["Birthday"] == None:
            await wait_until_send(id, config.friend_block_insert_Birthday)

            bot.register_next_step_handler(
                message, full_validation, "Birthday")
        else:
            new_user_horo = handlers.horoscopeproc.GenTmpUsrMess(id)[0]

            text = new_user_horo[2]+"\n\n"+new_user_horo[3]
            await wait_until_send(
                id, "Мы состоявляем гороскоп вашему другу, подождите некоторое время")

            Thread(target=send_friend_horo, args=(id, text)).start()
            # horoscopeusr.DelTmpUser(id)

    async def full_validation(message, type):
        id = message.chat.id
        text = message.text
        if text.find("/") != -1 and text != "/gen_user_mes":

            main(message)
            return 0

        is_user_already_in_handler[id] = True
        text = message.text
        result = functions.validation_ewerything(text, type)

        if result[0] == True:
            handlers.horoscopeusr.ChTmpUserInfo(
                inpTelegramID=id, inpFieldName=type, inpValue=result[1])

            validation_circle(message)
        else:
            await wait_until_send(id, "Введите данные в правильном формате")

            bot.register_next_step_handler(message, full_validation, type)

    @dp.message(commands=["send"])
    @show_log_
    async def send(message):
        try:
            id = int(message.chat.id)
            text = message.text
            if id in block_dict:
                block_dict.remove(id)
                
                return 0
            block_dict.append(id)
            # or functions.ListUserName(inpTelegramID=id)[0]==None:
            if handlers.horoscopeusr.RegUser(inpTelegramID=str(id))[0] == True:

                await wait_until_send(id, config.inter_name)

                bot.register_next_step_handler(
                    message, validation_name, True)
            elif functions.ListUserName(inpTelegramID=id)[0] == "":

                await wait_until_send(id, config.inter_name)

                bot.register_next_step_handler(
                    message, validation_name, message.id)
            else:
                us = functions.GetUsers(id)[0]
                if us["Name"] == None:
                    await wait_until_send(
                        id, 'Ваш персональный гороскоп будет сформирован после того, как вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
                    await wait_until_send(id, config.inter_name)

                    bot.register_next_step_handler(
                            message, validation_name, message.id)
                elif us["Birthday"] == None:
                    await wait_until_send(
                        id, 'Ваш персональный гороскоп будет сформирован после того, как вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
                    # Введите город,в котором вы родилисьы
                    await wait_until_send(id, config.inter_date)

                    bot.register_next_step_handler(
                            message, validation_birth, message.id)
                elif us["BirthTime"] == None:
                    await wait_until_send(
                        id, 'Ваш персональный гороскоп будет сформирован после того, как вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
                    await wait_until_send(id, config.inter_time)

                    bot.register_next_step_handler(
                            message, validation_time, message.id)
                elif us["Birthplace"] == None:
                    await wait_until_send(
                        id, 'Ваш персональный гороскоп будет сформирован после того, как вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')

                    await wait_until_send(id, config.inter_city)

                    bot.register_next_step_handler(
                            message, validation_city, message.id)
                elif us["RegDate"] == None:
                    await wait_until_send(
                        id, 'Ваш персональный гороскоп будет сформирован после того, как вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')

                    keyboard1 = types.InlineKeyboardMarkup()
                    keyboard1.row(types.InlineKeyboardButton(text="Утро", callback_data="tim;mor"),
                                    types.InlineKeyboardButton(text="Вечер", callback_data="tim;evn"))
                    mes = await wait_until_send(
                        id, config.inter_time_option, reply_markup=keyboard1)

                else:
                    # name=functions.ListUserName(inpTelegramID=int(id))[0]
                    
                    js = handlers.horoscopeproc.GenHourMessAll(
                        11, inpTelegramID=str(id))
                    txt = js[0]
                    # print(js)
                    today_send = txt[6]
                    if functions.select_all_active_until_table(id)["days_till_end"]+1<=0:
                        handlers.horoscopeusr.ChUserInfo(inpTelegramID=id,inpFieldName="SubscrType_ID",inpValue=5)
                        handlers.horoscopeusr.ChUserInfo(inpFieldName="IsActiveSub",inpTelegramID=id,inpValue=0)
                        subscribe(message)
                        return 0                                                                                                                                                                                                      
                    elif today_send:
                        
                        text = ""
                        text += (js[0][2]+"\n\n"+js[0][3])
                        mes = await wait_until_send(id, config.if_horo_sended)

                        Thread(target=send_mes, args=(js[0],)).start()

                        bot.register_next_step_handler(mes, main)
                    else:
                        text = ""
                        text += (js[0][2]+"\n\n"+js[0][3])
                        mes = await wait_until_send(
                            id, config.if_not_horo_sended)
                    # mes=await wait_until_send(id,config.if_horo_sended)

                        Thread(target=send_mes, args=(
                            js[0],)).start()

                        # bot.register_next_step_handler(mes,main)

                        bot.register_next_step_handler(mes, main)
        except Exception as err:
            await wait_until_send(id, "Что-то пошло не так,попроуйте еще раз")
            try:
                pass
            except:
                pass
            bot.register_next_step_handler(message, main)

    @dp.message(commands=["support"])
    @show_log_
    async def feedback(message):
        try:
            id = message.chat.id

            await wait_until_send(id, config.support)

        except:
            return 1

    @dp.message(commands=["change"])
    @show_log_
    async def change_tim(message):
        try:
            id = message.chat.id

            await wait_until_send(id, config.change_data)

        except:
            return 1

    @dp.message(commands=["subscribe"])
    @show_log_
    async def subscribe(message):
        
        id=message.chat.id
        print(functions.GetUsers(id)[0]["SubscrType_ID"])
        sub_type=int(functions.GetUsers(id)[0]["SubscrType_ID"])
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

            # await wait_until_send(id,"тут будет оплата")
    
    @dp.message(content_types=['text'])
    async def main(message):
        id = message.chat.id
        is_user_already_in_handler[id] = True

        text = message.text
        if text == "/send" or text == "/subscribe" or text == "/change" or text == "/feedback" or text == "full_delete_user_uga_buga" or text == "/gen_user_mes" or text == "Посмотреть гороскоп другу":
            if text == "/send":

                send(message)
            elif text == "/subscribe":

                subscribe(message)
            elif text == "/feedback":

                feedback(message)
            elif text == "/change":

                change_tim(message)
            elif text == "full_delete_user_uga_buga":
                full_del(message)
            else:
                gen_user_mess(message)
        # or functions.ListUserName(inpTelegramID=id)[0]==None:
        elif handlers.horoscopeusr.RegUser(inpTelegramID=str(id))[0] == True:
    
            await wait_until_send(id, config.inter_name)

            bot.register_next_step_handler (message, validation_name, message.id)
        text = message.text
        text1 = text.split()
        id = message.chat.id
        try:
            block_dict.remove(id)
        except:
            pass
        
        is_user_already_in_handler[id] = True
        text = message.text
        if handlers.horoscopeusr.RegUser(inpTelegramID=str(id))[0]:
            if len(text1) == 2:
                if int(text1[1]) == 20:
                    await wait_until_send(id, config.thanks_for_payment)
                try:
                    handlers.horoscopeusr.ChUserInfo(inpValue=int(
                        text1[1]), inpTelegramID=str(id), inpFieldName="Source_ID")
                except:
                    pass

            await wait_until_send_photo(id, config.inter_name,photo=photos["inter_name"])

        elif functions.ListUserName(inpTelegramID=id)[0] == "":
            if len(text1) == 2:
                try:
                    handlers.horoscopeusr.ChUserInfo(inpValue=int(
                        text1[1]), inpTelegramID=str(id), inpFieldName="Source_ID")
                    await registartion(id,text)
                except:
                    pass

            await wait_until_send_photo(id, config.inter_name,photo=photos["inter_name"])

        elif text == "/start":
            await wait_until_send(
                id, 'Здравствуйте.\n\nСпасибо,что вернулись в нашего бота. Вы получите гороскоп по расписанию.\n\nЕсли хотите получить его сейчас нажмите на соответствующую кнопку в меню')

        else:
            await registartion(id,text)

    

    
    @dp.callback_query_handler(func=lambda call: call.data.split(";")[0] == "sub")
    async def sub_options(call):
        try:

            id = call.from_user.id
            data = call.data
            data = data.split(";")
            is_new = data[1]
            days = int(data[2])
            delete_cache[id] = []

            if is_new == "n":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(
                    text="Да", callback_data="agr"+";"+str(days))
                but2 = types.InlineKeyboardButton(
                    text="Нет", callback_data="net")
                but = types.InlineKeyboardButton(
                    text="Назад", callback_data="2opt")

                keyboard.row(but1, but2)
                keyboard.add(but)

                await wait_until_send(id, "Стоимость подписки  на "+str(days)+" дней составит"+str(config.cost[days]) + "рублей.\n\nПеред оплатой подписки, пожалуйста, ознакомьтесь со следующими документами:\n\nСоглашение на обработку персональных данных" +
                                config.url_for_all+"\n\nСоглашение на обработку платежей "+config.url_for_costs[days]+".\n\nВы подтверждаете что согласны с политикой обработки персональных данных и платежей?", parse_mode="html", reply_markup=keyboard)
        except Exception as err:
            try:
                await wait_until_send(id, "Что-то пошло не так")
            except:
                return 0
        finally:
            try:
                bot.delete_message(chat_id=id, message_id=call.message.id)
            except:
                pass
    @dp.callback_query_handler(func=lambda call:call.data.find("offer") != -1)
    async def offert(call):
        try:
            days=call.data.split(";")[1]
            id = call.from_user.id
            keyboard=types.InlineKeyboardMarkup()
            but=InlineKeyboardButton(text="Назад",callback_data="agr;"+days)
            keyboard.add(but)
            await wait_until_send(id,config.offert,parse_mode="html",reply_markup=keyboard)
        finally:
            try:
                bot.delete_message(chat_id=id, message_id=call.message.id)
            except:
                pass
    @dp.callback_query_handler(func=lambda call: call.data.find("inf") != -1)
    async def sub_info(call):
        try:
            id = call.from_user.id
            keyboard = types.InlineKeyboardMarkup()
            but = types.InlineKeyboardButton(
                text="Назад", callback_data="2opt")
            keyboard.add(but)

            await wait_until_send(id, "В подписку входит общее описание дня с точки зрения расположения звезд и планет, звездная карта дня и ваш персональный гороскоп, который будет составляться и направляться вам каждый день в указанное вами время.", reply_markup=keyboard, parse_mode="html")
        except:

            try:
                await wait_until_send(id, "Что-то пошло не так")
            except:
                return 0
        finally:

            try:
                bot.delete_message(chat_id=id, message_id=call.message.id)
            except:
                pass

    @dp.callback_query_handler(func=lambda call: call.data.find("end") != -1)
    async def end_sub(call):
        try:
            id = call.from_user.id
            keyboard = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton(
                text="да", callback_data="fin_sub")
            but2 = types.InlineKeyboardButton(
                text="нет", callback_data="del")
            keyboard.row(but1, but2)
            await wait_until_send(id, '''Обращаем внимание, что при отказе от подписки функции бота отключаются и денежные средства, оставшиеся до окончания подписки, не возвращаются.

Вы точно хотите отказаться от подписки?''', reply_markup=keyboard)
        except Exception as err:
            try:
                await wait_until_send(id, "Что-то пошло не так")
            except:
                return 0
        finally:
            try:
                bot.delete_message(chat_id=id, message_id=call.message.id)
            except:
                pass
    @dp.callback_query_handler(func=lambda call: call.data.find("fin_sub")!=-1)
    async def fin_sub(call):
        try:
            id = call.from_user.id
            delete_sub(id=id)
            add_payment(sub_type=3,telegram_id=id,payment_id=str(functions.count_payments()),active_until="01.10.1000",days=30,payed=True,amount=0,link="UNSUB")

            await wait_until_send(id,'Подписка отменена. Вы можете в любой момент активировать ее заново через раздел меню "подписка".')
        except:
            await wait_until_send(id,"Мы не обнаружили у вас подписку")
        finally:
            try:
                bot.delete_message(chat_id=id, message_id=call.message.id)
            except:
                pass
    @dp.callback_query_handler(func=lambda call: call.data.find("del") != -1)
    async def delete(call):
        try:
            id = call.from_user.id
            await wait_until_send(
                id, "Спасибо, что продолжаете пользоваться Астроботом!")
        except:
            try:
                await wait_until_send(id, "Что-то пошло не так")
            except:
                return 0
        finally:
            try:
                bot.delete_message(chat_id=id, message_id=call.message.id)
            except:
                pass

    @dp.callback_query_handler(func=lambda call: call.data.find("end") != -1)
    async def fin_end(call):
        try:
            id = call.from_user.id
            await wait_until_send(
                id, "Ваша подписка отменена. Вы можете в любой момент активировать ее заново через  раздел меню 'подписка'.")
        except:
            try:
                await wait_until_send(id, "Что-то пошло не так")
            except:
                return 0
        finally:
            try:
                bot.delete_message(chat_id=id, message_id=call.message.id)
            except:
                pass
    @dp.callback_query_handler(func=lambda call: call.data.find("SUBSCR_ACT") != -1)#SUBSCR_ACT
    async def active_sub(call):
        id=call.from_user.id
        # print(functions.GetUsers(id)[0]["SubscrType_ID"])
        sub_type=int(functions.GetUsers(id)[0]["SubscrType_ID"])
        try:
            if id in delete_cache:
                for i in delete_cache[id]:
                    bot.delete_message(id, i)
        except:
            pass
        if sub_type==1 or sub_type==2:
            # print("here")
            keyboard=types.InlineKeyboardMarkup()
            but1=types.InlineKeyboardButton(text="Активировать подписку", callback_data="2opt;"+str(sub_type))
            keyboard.row(but1)
            # print(config.sub_type1_text(id))
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

            # await wait_until_send(id,"тут будет оплата")
    @dp.callback_query_handler(func=lambda call: call.data.find("ret") != -1)
    async def ret(call):
        try:
            id = call.from_user.id
            keyboard = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton(
                text="30 дней", callback_data="sub;n;30")
            but2 = types.InlineKeyboardButton(
                text="180 дней", callback_data="sub;n;180")
            but3 = types.InlineKeyboardButton(
                text="365 дней", callback_data="sub;n;365")
            but4 = types.InlineKeyboardButton(
                text="Что входит в подписку?", callback_data="inf")
            but5 = types.InlineKeyboardButton(
                text="Назад", callback_data="full_back")
            keyboard.row(but1, but2, but3)
            keyboard.add(but4)
            keyboard.add(but5)
            # if id in delete_cache:
            #     for i in delete_cache[id]:
            #         bot.delete_message(id, i)
                # delete_cache[id] = []
            await wait_until_send(id, 'Спасибо, что пользуетесь Астроботом.\n\nВ данный момент у вас действует пробный период подписки. Для вас доступны все функции бота!\n\nДо конца пробного периода осталось еще N дней.\n\nВы можете прямо сейчас активировать платную подписку.\n\nВ таком случае оставшееся время пробного периода суммируется с временем подписки.', reply_markup=keyboard)
        except Exception as err:
            try:
                await wait_until_send(id, "Что-то пошло не так")
            except:
                return 0
        finally:
            try:
                bot.delete_message(chat_id=id, message_id=call.message.id)
            except:
                pass

    @dp.callback_query_handler(func=lambda call: call.data.find("full_back") != -1)
    async def full_back(call):
        id = call.from_user.id
        await wait_until_send(
            id, "Для использования бота выберите кнопку в меню")
        try:
            bot.delete_message(chat_id=id, message_id=call.message.id)
        except:
            pass
    @dp.callback_query_handler(func=lambda call: call.data.split(";")[0] == "tim")
    async def time_select(call):
        try:
            id=call.from_user.id
            data=call.data
            data=data.split(";")
            if data[1]=="mor":
                functions.shedule_time_changer(inpTelegramID=id,shedule_time=int(0))


            else:
                functions.shedule_time_changer(inpTelegramID=id,shedule_time=int(1))
            mes=await wait_until_send(id,"Спасибо, все данные заполнены.\n\nПожалуйста, подождите. Формируем вашу натальную карту, на основе которой будет составляться ваш персональный ежедневный гороскоп.\n\nЕсли вы ошиблись при вводе, то отправьте корректные данные в поддержку @AstroBot_support. Мы исправим информацию, чтобы для вас формировался корректный гороскоп.")
            await wait_until_send(id,config.before_first_horo)
            Thread(target=send_natal_map,args=(id,)).start()
        except:
            try:
                await wait_until_send(id, "Что-то пошло не так")
            except:
                return 0
        finally:
            bot.delete_message(chat_id=id,message_id=call.message.id)
    @dp.callback_query_handler(func=lambda call: call.data.find("2opt") != -1)
    async def opt2(call):
        try:
            id=call.from_user.id
            sub_type=int(functions.GetUsers(id)[0]["SubscrType_ID"])
            # sub_type=functions.GetUsers(id)[0]["SubscrType_ID"]
            keyboard = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton(
                text="30 дней", callback_data="agr;30")
            but2 = types.InlineKeyboardButton(
                text="180 дней", callback_data="agr;180")
            but3 = types.InlineKeyboardButton(
                text="365 дней", callback_data="agr;365")
            but4 = types.InlineKeyboardButton(
                text="Что входит в подписку?", callback_data="inf")
            but5 = types.InlineKeyboardButton(
                text="Назад", callback_data="full_back")
            keyboard.row(but1, but2, but3)
            keyboard.add(but4)
            keyboard.add(but5)
            if sub_type==1:
                await wait_until_send(id,'Спасибо, что пользуетесь ботом "Твой гороскоп"\n\nВ данный момент у вас действует пробный период, подписки.'+ config.cost_text,reply_markup=keyboard,parse_mode="html")     
            elif sub_type==2 or sub_type==4 or sub_type==5 or sub_type==3:
                await wait_until_send(id,config.cost_text,reply_markup=keyboard,parse_mode="html")
            # elif sub_type==2:
            #     await wait_until_send(id,"Ваш пробный период использования бота 'Твой гороскоп' подошел к концу.\n\nЕсли Вы хотите дальше получать Ваш персональный ежедневный гороскоп, необходимо оплатить подписку.\n\nВ данный момент доступно 3 варианта подписки: на 30, 180 и 365 дней.\n\nСтоимость на 30 дней - 69 рублей\n\nСтоимость на 180 дней - (зачеркнутная цена) актуальная цена\n\nСтоимость на 365 дней - (зачеркнутная цена) актуальная цена.\n\nНа какой срок Вы бы хотели активировать подписку?",reply_markup=keyboard)
        # bot.send_message
        except:
            try:
                await wait_until_send(id, "Что-то пошло не так")
            except:
                return 0
        finally:
            try:
                bot.delete_message(chat_id=id, message_id=call.message.id)
            except:
                pass

    @dp.callback_query_handler(func=lambda call: call.data.find("agr") != -1)
    async def agreement(call):
        try:

            data = call.data.split(";")
            days = int(data[1])
            id = call.from_user.id
            active_until = functions.GetUsers(id)[0]["ActiveUntil"]
            date_format = '%Y-%m-%d'
            active_until = datetime.strptime(active_until, date_format)
            active_until = datetime.strftime(active_until, DATE_FORMAT)                
            url=for_payments.make_recurse_pay(id=id,days=days,amount=config.cost[days],test=0)
            keyboard=types.InlineKeyboardMarkup()
            
            but1=types.InlineKeyboardButton(text="Назад",callback_data="2opt;"+str(days))
            but=types.InlineKeyboardButton(text="Оплата",url=url)
            but2=types.InlineKeyboardButton(text="Офферта",callback_data="offer;"+str(days))
            keyboard.row(but,but2)
            keyboard.add(but1)
            mess=await wait_until_send(id, "Стоимость подписки  на "+str(days)+" дней составит "+str(config.cost[days]) + " рублей.", reply_markup=keyboard)
            if id in delete_cache:
                for i in delete_cache[id]:
                    bot.delete_message(id, i)
            delete_cache[id] = []
        except Exception as err:
            from traceback import format_exc
            print(err)
            format_exc(err)
            try:
                await wait_until_send(id, "Что-то пошло не так")
            except:
                return 0
        finally:
            try:
                bot.delete_message(chat_id=id, message_id=call.message.id)
            except:
                pass
    @dp.callback_query_handler(func= lambda call:call.data.find("ge1nder")!=-1)
    async def gender(call):
        try:
            id = call.from_user.id
            data = call.data.split(";")
            text = int(data[1])
            handlers.horoscopeusr.ChUserInfo(
            inpValue=text, inpTelegramID=str(id), inpFieldName="Gender_ID")
            # Введите город,в котором вы родилисьы
            message=await wait_until_send_photo(id, config.inter_date,photo=photos["inter_date"])

            bot.register_next_step_handler(
                message, validation_birth, message.id)
        except:
            pass
        finally:
            # try:
            #     bot.delete_message(id,del_id+1)
            # except:
            #     pass
            try:

                bot.delete_message(id,call.message.id)
            except:
                pass
    @dp.callback_query_handler(func=lambda call: call.data.find("net") != -1)
    async def no_agr(call):
        try:
            id = call.from_user.id
            mes = await wait_until_send(
                id, "К сожалению, вы не можете активировать подписку, пока не согласитесь с условиями обработки персональных данных и платежей. Нажмите 'Да', чтобы подтвердить согласие с условиями.")
            delete_cache[id].append(mes.id)
        except:
            try:
                await wait_until_send(id, "Что-то пошло не так")
            except:
                return 0
        # finally:
            # bot.delete_message(chat_id=id,message_id=call.message.id)
    # @bot.inline_handler(func=lambda query : len(query.query) > 0)
    # async def empty_inline(query):
    #     text=query.query
    #     r = types.InlineQueryResultArticle(
    #         id='1',
    #         # parse_mode='html',
    #         title="AstologyBot",
    #         description="Отправить гороскоп",
    #         input_message_content=types.InputTextMessageContent(
    #         message_text="text"*1000))
    #     bot.answer_inline_query(query.id, [r])
    # keyboard=types.InlineKeyboardMarkup()
    # but1 = types.InlineKeyboardButton(
    #     text="Продлить подписку", callback_data="2opt;"+str(3))
    # but2 = types.InlineKeyboardButton(
    #     text="Отказаться от подписки", callback_data="end")
    # keyboard.row(but1, but2)
    # await wait_until_send(952863788, config.sub_type3_text(952863788), reply_markup=keyboard)
    # sub_type=int(functions.GetUsers(952863788)[0]["SubscrType_ID"])
    # print(sub_type)
    bot.polling(non_stop=True)
except Exception as e:
    logger.error(e)
    logger.warning("Reconnecting...")
    del(is_user_already_in_handler)
    is_user_already_in_handler = {}
    # from traceback import format_exc
    # format_exc(e)

    time.sleep(0.5)
    __main__()


__main__()
