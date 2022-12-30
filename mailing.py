from ast import arg
import schedule
from threading import Thread
import time
from for_payments import Get_Data
import horoscopeproc
from datetime import datetime, date, timedelta
import config
import telebot
import time
import functions
from config import TOKEN
import horoscopeusr as horoscopeusr
from horoscopeusr import ChUserInfo
import for_payments

def Get_Data():
    return datetime.strftime(datetime.now(), DATE_FORMAT)

# from telebot import telebot.types
from databaseInteraction import *
from utils import *
import telebot
import random
import string







class Button(telebot.types.InlineKeyboardButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.callback_data = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(32))

    def onClick(self, coro, *args, **kwargs):
        try:
            @bot.callback_query_handler(lambda call: call.data == self.callback_data)
            def some_coro(call):
                return coro(call, *args, **kwargs)

        except Exception as e:
            logger.error(f'{coro} - handler exception --> {e}')
def change_active_until_date(start,date_end,days,base="subs"):
    if date_end.find("-")!=-1:
        date_end=datetime.strptime(date_end, "%Y-%m-%d")
        date_end=datetime.strftime(date_end, DATE_FORMAT)
    if datetime.strptime(start,DATE_FORMAT)>=datetime.strptime(date_end,DATE_FORMAT):
        uctive_until=datetime.strptime(start,DATE_FORMAT)+timedelta(days=days)
    else:
        uctive_until=datetime.strptime(date_end,DATE_FORMAT)+timedelta(days=days)
    if base=="users":
        end=datetime.strftime(uctive_until, "%Y-%m-%d")
    else:
        end = datetime.strftime(uctive_until, DATE_FORMAT)
    return(end)
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# write_pid()
def wait_until_send_photo(id,photo,caption,reply_markup=None,parse_mode=None,url=None):
    while True:
        try:
            mes=bot.send_photo(id,caption=caption,photo=photo,reply_markup=reply_markup,parse_mode=parse_mode)
            return mes
        except Exception as err:
            
            if 'error_code' not in vars(err).keys():
                return 0
            if err.error_code==400:
                    return err
            print(err)
            if err.error_code==429:
                continue

            elif err.error_code==403:
                horoscopeusr.ChUserInfo(inpValue=0,inpTelegramID=str(id),inpFieldName="IsActiveBot" )
                return err
            else:
                return err
def wait_until_send(id,text,reply_markup=None,parse_mode=None,url=None):
    while True:
        try:
            mes=bot.send_message(id,text,reply_markup=reply_markup,parse_mode=parse_mode)
            return mes
        except Exception as err:
            
            if 'error_code' not in vars(err).keys():
                return 0
                
            if err.error_code==429:
                return err

            elif err.error_code==400:
                if url!=None:
                    new_user_horo=horoscopeproc.GenTmpUsrMess(id)[0]
                    gender=new_user_horo[4]
                    name=new_user_horo[1]
                    horoscopeusr.RegTmpUser(id)
                    horoscopeusr.ChTmpUserInfo(inpTelegramID=id,inpValue=name,inpFieldName="Name")
                    horoscopeusr.ChTmpUserInfo(inpTelegramID=id,inpValue=gender,inpFieldName="Gender_ID")
                    text=new_user_horo[2]+"\n\n"+new_user_horo[3]
                else:
                    return err
            elif err.error_code==403:
                horoscopeusr.ChUserInfo(inpValue=0,inpTelegramID=str(id),inpFieldName="IsActiveBot" )
                return err
            else:
                return err



def wait_until_copy(id,forward_id,mes_id,reply_markup=None):
    while True:
        
        try:
            mes=bot.copy_message(id,forward_id,mes_id,reply_markup=reply_markup)
            return mes
        except Exception as err:
            
            if 'error_code' not in vars(err):
                return 0
            if err.error_code==403:
                horoscopeusr.ChUserInfo(inpValue=0,inpTelegramID=str(id),inpFieldName="IsActiveBot" )
                return(err)
            if err.error_code==429:
                return err
            else:
                return err



#--------------------------------Sending horoscopes



def morning_sender():
    try:
        date_today=Get_Data()
        #"date_pict\16.10.2022.png"
        path="date_pict/"+date_today+".png"
        pict=open(path,"rb").read()
        posts=horoscopeproc.GenHourMessAll(0)
        buttons=telebot.types.InlineKeyboardMarkup()
        but=telebot.types.InlineKeyboardButton(text="Получить персональный гороскоп",callback_data="SUBSCR_ACT")
        buttons.add(but)
        if posts[0][0]=='952863788':
            posts[0]=list(posts[0])
            posts[0][3]=""

        # for i in range(30):
        try:
            for i in range(len(posts)):
                
                first_part=posts[i][2]
                second_part=posts[i][3]
                id=posts[i][0]
                if second_part!="":
                    
                    txt=posts[i][2]+"\n\n"+posts[i][3]
                    Thread(target=mail_horoscope_after_photo,args=(id,pict,first_part,second_part)).start()

                    
                else:
                    Thread(target=wait_until_send_photo,args=(id,pict,first_part,buttons,"html")).start()
                # Thread(target=wait_until_send,args=(id,txt),kwargs={"parse_mode":"html"}, daemon=True).start()
                time.sleep(1/30)
            
        except:
            pass
        
        users=horoscopeproc.GetListUsersOnDesTime(1)


        posts = get_posts(sessionmaker(engine)(), category='person', date=Get_Data())
        for j in range(len(users)):
            for i in range(len(posts)): # get_posts -> (category, date, time, managerId, postId)

                managerID = posts[i].ManagerID
                postID = posts[i].PostID
                Thread(target=wait_until_copy,args=(users[j][0],managerID,postID), daemon=True).start()
                time.sleep(1/15)
        return True


    except:
        return False




def evening_sender():
    hour=1
    posts=horoscopeproc.GenHourMessAll(1)
    date=datetime.strftime(datetime.now()+timedelta(days=1), DATE_FORMAT)
    path="date_pict/"+date+".png"
    pict=open(path,"rb").read()
    posts=list(posts)
    posts[0]=list(posts[0])
    # posts=horoscopeproc.GenHourMessAll(0)
    buttons=telebot.types.InlineKeyboardMarkup()
    but=telebot.types.InlineKeyboardButton(text="Получить персональный гороскоп",callback_data="SUBSCR_ACT")
    buttons.add(but)
    if posts[0][0]=='952863788':
        posts[0]=list(posts[0])
        posts[0][3]=""

    # for i in range(30):
    try:
        for i in range(len(posts)):
            
            first_part=posts[i][2]
            second_part=posts[i][3]
            id=posts[i][0]
            if second_part!="":
                
                txt=posts[i][2]+"\n\n"+posts[i][3]
                Thread(target=mail_horoscope_after_photo,args=(id,pict,first_part,second_part)).start()
                # Thread(target=wait_until_send_photo,args=(id,pict,first_part,None,"html")).start()
                # time.sleep(1/10)
                # Thread(target=wait_until_send,args=(id,second_part,None,"html")).start()
            else:
                Thread(target=wait_until_send_photo,args=(id,pict,first_part,buttons,"html")).start()
            # Thread(target=wait_until_send,args=(id,txt),kwargs={"parse_mode":"html"}, daemon=True).start()
            time.sleep(1/15)
    except:
        pass
    
    users=horoscopeproc.GetListUsersOnDesTime(0)
    # posts=horoscopeproc.GetFromAstroSchool(inpCategory="person",inpDateSend=Get_Data())

    posts = get_posts(sessionmaker(engine)(), category='person', date=Get_Data())
    for j in range(len(users)):
        for i in range(len(posts)): # get_posts -> (category, date, time, managerId, postId)

            managerID = posts[i].ManagerID
            postID = posts[i].PostID
            Thread(target=wait_until_copy,args=(users[j][0],managerID,postID), daemon=True).start()
            time.sleep(1/15)
    return True


#----------------------------Send in sheduled time



def on_time_sender(time1 : str) -> bool:
    # all_days_posts=horoscopeproc.GetFromAstroSchool(inpDateSend=Get_Data())
    posts = get_posts(sessionmaker(engine)(), Get_Data(), time=time1)
    managerID = posts[0].ManagerID
    postID = posts[0].PostID
    buttons = get_buttons(sessionmaker(engine)(), postID)
    markup = telebot.types.InlineKeyboardMarkup()

    for button in buttons:
        _button = Button(text=button.Source, url=button.Url)
        markup.add(_button)
    if posts[0].FilePath==None:
        users=horoscopeproc.GetListUsersOnDesTime(1)
        users.extend(horoscopeproc.GetListUsersOnDesTime(0))
        for i in range(len(posts)):
            for j in range(len(users)):
                managerID = posts[i].ManagerID
                postID = posts[i].PostID

                Thread(target=wait_until_copy,args=(users[j][0], managerID ,postID,markup), daemon=True).start()
                time.sleep(1/15)
    else:
        path=posts[0].FilePath
        with open (path[1:],"r") as file:#post_files\17.10.2022_471681210.txt
            all_users=file.readlines()
            for i in range(len(all_users)):
                Thread(target=wait_until_copy,args=(all_users[i], managerID ,postID,markup), daemon=True).start()
                time.sleep(1/15)
    # return True


#--------------------------------------service message functions
def text_for_notifications(day):
    if str(day)=="0":
        return '''Добрый день!

Спасибо, что ты пользуешься Астроботом! Мы рады, что твой персональный гороскоп, составленный Астроботом по твоей натальной карте, помогает тебе строить планы, разбираться в различных ситуациях и получать максимум от каждого дня!

Период пробной подписки действует 7 дней. Составление персональных гороскопов для наших пользователей требует много ресурсов, поэтому по истечению пробного периода подписка становится платной. Но мы сделали оплату минимально возможной:

1)  на месяц - 69 рублей 
2)  на полгода со скидкой 20% - <strike>414</strike>, 330 рублей
3)  на год со скидкой 30% - <strike>828</strike>, 580 рублей. 

Твой пробный период закончился.

Ты можешь оформить подписку и до истечения пробного периода, в таком случае количество дней пробного периода и количество дней, оплаченных по подписке, суммируются. 

Оформи подписку прямо сейчас, и ты продолжишь каждый день получать персональный гороскоп, составленный нашим Астроботом по твоей натальной карте.

Прекрасного дня! 🌸'''
    else:
        days_text="дней"
        if str(day) =="3":
            days_text="дня"
        elif str(day)=="1":
            days_text="день"
        return'''Добрый день!

Спасибо, что ты пользуешься Астроботом! Мы рады, что твой персональный гороскоп, составленный Астроботом по твоей натальной карте, помогает тебе строить планы, разбираться в различных ситуациях и получать максимум от каждого дня!

Период пробной подписки действует 7 дней. Составление персональных гороскопов для наших пользователей требует много ресурсов, поэтому по истечению пробного периода подписка становится платной. Но мы сделали оплату минимально возможной:

1)  на месяц - 69 рублей 
2)  на полгода со скидкой 20% - <strike>414</strike>, 330 рублей
3)  на год со скидкой 30% - <strike>828</strike>, 580 рублей. 

У тебя остаётся ещё '''+str(day)+" "+days_text+'''.

Ты можешь оформить подписку и до истечения пробного периода, в таком случае количество дней пробного периода и количество дней, оплаченных по подписке, суммируются. 

Оформи подписку прямо сейчас, и ты продолжишь каждый день получать персональный гороскоп, составленный нашим Астроботом по твоей натальной карте.

Прекрасного дня! 🌸'''
def make_notificartion_with_keyboard(id,photo,end_time,caption=None):
    keyboard=telebot.types.InlineKeyboardMarkup()
    but1 = telebot.types.InlineKeyboardButton(
        text="30 дней", callback_data="agr;30")
    but2 = telebot.types.InlineKeyboardButton(
        text="180 дней", callback_data="agr;180")
    but3 = telebot.types.InlineKeyboardButton(
        text="365 дней", callback_data="agr;365")
    but4 = telebot.types.InlineKeyboardButton(
        text="Что входит в подписку?", callback_data="inf")
    but5 = telebot.types.InlineKeyboardButton(
        text="Назад", callback_data="full_back")
    keyboard.row(but1, but2, but3)
    keyboard.add(but4)
    keyboard.add(but5)
    id=id
    # sub_type=int(functions.GetUsers(id)[0]["SubscrType_ID"])
    # print(functions.select_all_active_until_table(id))
    # end_time=str(functions.select_all_active_until_table(id)["days_till_end"]+1)
    # if int(end_time)==1:
    #     x=wait_until_send(id,text_for_notifications(end_time),reply_markup=keyboard,parse_mode="html")
    # else:
    if caption!=None:
        x=wait_until_send_photo(id,caption=caption,photo=photo,reply_markup=keyboard,parse_mode="html")
    else:
        x=wait_until_send_photo(id,caption=text_for_notifications(end_time),photo=photo,reply_markup=keyboard,parse_mode="html")
    # if sub_type==1 or sub_type==2:
    #     end_time=functions.select_all_active_until_table(id)["days_till_end"]
    #     keyboard=telebot.types.InlineKeyboardMarkup()
    #     but1=telebot.types.InlineKeyboardButton(text="Активировать подписку", callback_data="2opt;"+str(sub_type))
    #     keyboard.row(but1)
    #     wait_until_send(id, config.sub_type1_text(id), reply_markup=keyboard)

    # if sub_type == 100:
    #     keyboard = telebot.types.InlineKeyboardMarkup()
    #     but1 = telebot.types.InlineKeyboardButton(text="Активировать подписку", callback_data="2opt;"+str(sub_type))
    #     keyboard.row(but1)
    #     wait_until_send(id, config.sub_type3_text(id), reply_markup=keyboard)

    # if sub_type == 3:
    #     keyboard = telebot.types.InlineKeyboardMarkup()
    #     but1 = telebot.types.InlineKeyboardButton(
    #         text="Продлить подписку", callback_data="2opt;"+str(sub_type))
    #     but2 = telebot.types.InlineKeyboardButton(
    #         text="Отказаться от подписки", callback_data="end")
    #     keyboard.row(but1, but2)
    #     wait_until_send(id, config.sub_type3_text(), reply_markup=keyboard)

    # if sub_type == 4 or sub_type == 5:
    #     keyboard = telebot.types.InlineKeyboardMarkup()
    #     but1 = telebot.types.InlineKeyboardButton(
    #         text="Активировать подписку", callback_data="2opt;"+str(sub_type))
    #     keyboard.row(but1)
    #     wait_until_send(id, config.sub_type4_text(), reply_markup=keyboard)

        # wait_until_send(id,"тут будет оплата")



def service_message() -> None:
    try:
        cool_subs=get_subs()
        already_registr_subs=[]
        recurent_subs=[]
        try:
            wait_until_send(952863788,"функция началась")
            # breakpoint()

            wait_until_send(5127634821,"рассылка началась")
        except:
            pass
        # breakpoint()
        # return("end")
        for i in range(len(cool_subs)):
            try:
                already_registr_subs.append(cool_subs[i].TelegramID)#формируем список тех, кто уже подписался
                # print(cool_subs[i].End)
                data=Get_Data()
                if cool_subs[i].End==Get_Data():
                    recurent_subs.append(cool_subs[i])#формируем список из тех, с кого списать деньги
            except:
                continue
        all_service_messages=functions.select_all_active_until_table()
        
        i=0
        if all_service_messages==None:
            all_service_messages=[]
        while i<len(all_service_messages):#Удаляем из списка рассылки тех, у кого рекурентная подписка
            
            if int(all_service_messages[i]["id"]) in already_registr_subs:
                all_service_messages.pop(i)
            elif all_service_messages[i]['days_till_end']+1==0:
                id=all_service_messages[i]["id"]
                ChUserInfo(inpTelegramID=id,inpFieldName="SubscrType_ID",inpValue=5)
                ChUserInfo(inpFieldName="IsActiveSub",inpTelegramID=id,inpValue=0)
                i+=1
            else:
                i+=1
        
        photos={}
        photos["0"]=open("days/"+"0.jpg","rb").read()

        photos["3"]=open("days/"+"3.jpg","rb").read()
        
        photos["7"]=open("days/"+"7.jpg","rb").read()

        photos["1"]=open("days/"+"1.jpg","rb").read()
        photos["10"]=open("days/"+"10.png","rb").read()
#         # breakpoint()

        for i in range(len(all_service_messages)):
            try:
                days=all_service_messages[i]["days_till_end"]+1
                # if days==7:
                #     print(days)
                if days in config.days_for_mailing:
                    
                    # end_time=str(functions.select_all_active_until_table(id)["days_till_end"]+1)
                    try:
                        id=all_service_messages[i]["id"]
                        Thread(target=make_notificartion_with_keyboard,args=(id,photos[str(days)],days)).start()#Отправляем в процесс id
                    except:
                        Thread(target=make_notificartion_with_keyboard,args=(id,photos[str(0)],days)).start()#Отправляем в процесс id
                        # make_notificartion_with_keyboard(all_service_messages[i]["id"],photos[str(days)])
                    finally:
                        time.sleep(1/15)
                if days==-3:
                    id=all_service_messages[i]["id"]
                    # print(all_service_messages[i]["id"],all_service_messages[i])
                    caption="""Заметили, что последние 3 дня даются вам тяжелее обычного? 
Все потому, что вы забыли оформить подписку на Астробота, который составляет для вас ежедневный персональный гороскоп с учетом вашей натальной карты! 

Оформите подписку прямо сейчас, и вы сможете строить планы, разбираться в различных ситуациях и получать максимум от каждого дня!"""
                    Thread(target=make_notificartion_with_keyboard,args=(id,photos[str(3)],days,caption)).start()
                    time.sleep(1/15)  
                if days==-10:
                    id=all_service_messages[i]["id"]
                    caption="""Заметили, что последние 10 дней даются вам тяжелее обычного? 
Все потому, что вы забыли оформить подписку на Астробота, который составляет для вас ежедневный персональный гороскоп с учетом вашей натальной карты! 

Оформите подписку прямо сейчас, и вы сможете строить планы, разбираться в различных ситуациях и получать максимум от каждого дня!"""
                    Thread(target=make_notificartion_with_keyboard,args=(all_service_messages[i]["id"],photos[str(10)],days,caption)).start() 
                    time.sleep(1/15)
            except:
                continue
#         print(recurent_subs)
        # breakpoint()  

        print(10)
        try:
            wait_until_send(952863788,"рассылка закончилась")
        except:
            pass
        for i in range(len(recurent_subs)):
            
            # print(0)
            
            # print(recurent_subs[i].PayID,"Pay1111")
            if recurent_subs[i].Type==3:
                amount=69
            else:
                amount=config.cost
            days1=30
            if int(float(recurent_subs[i].Type))==330 or int(float(recurent_subs[i].Type==config.cost[180])):
                days1=180
            if int(float(recurent_subs[i].Type))==580 or int(float(recurent_subs[i].Type==config.cost[365])):
                days1=365
            pay=for_payments.get_money_for_sub(id=int(recurent_subs[i].PayID),amount=int(float(recurent_subs[i].Type)),days=days1,test=0,tg_id=recurent_subs[i].TelegramID)
            # print(pay.text)
            try:
                if "ERROR" not in pay.text:#Если автоплатеж не удался, то включается функция,которая закидывает информацию о автоплатеже а таблицу payments, Где проверяется то, оплатили ли счет
                    # set_field(id=int(recurent_subs[i].TelegramID),end=end)
                    try:
                        add_success_payment(telegram_id=recurent_subs[i].TelegramID,payment_id=str(count_payments()),days=30,price=0,type_of_payment="TRY REC")
                    except:
                        pass
                    add_payment(sub_type=3,telegram_id=recurent_subs[i].TelegramID,payment_id=str(count_payments()),active_until="01.10.1000",days=days1,payed=True,amount=0,link="try REC")

                else:
                    try:
                        add_success_payment(telegram_id=recurent_subs[i].TelegramID,payment_id=str(count_payments()),days=30,price=0,type_of_payment="TRY REC")
                    except:
                        pass
                    # add_payment(sub_type =2,telegram_id = id,payment_id = payment_id,active_until = active_until,days = days,payed = False,amount = config.cost[days],link = url)
            except Exception as err:
                try:
                    wait_until_send(952863788,str(err))
                except:
                    pass
                continue
        try:
            wait_until_send(952863788,"списание закончилось")
        except:
            pass

    except Exception as err:
        try:
            wait_until_send(952863788,str(err))
        except:
            pass
        print("errr")
        
        logger.error(err)

        return 0

def mail_after_err():
    try:
        all_service_messages=functions.select_all_active_until_table()
        keyboard=telebot.types. InlineKeyboardMarkup()
        but1 = telebot.types.InlineKeyboardButton(
            text="30 дней", callback_data="agr;30")
        but2 = telebot.types.InlineKeyboardButton(
            text="180 дней", callback_data="agr;180")
        but3 = telebot.types.InlineKeyboardButton(
            text="365 дней", callback_data="agr;365")
        but4 = telebot.types.InlineKeyboardButton(
            text="Что входит в подписку?", callback_data="inf")
        but5 = telebot.types.InlineKeyboardButton(
            text="Назад", callback_data="full_back")
        keyboard.row(but1, but2, but3)
        keyboard.add(but4)
        keyboard.add(but5)
        photo=open("days/0.jpg","rb").read()
        for i in range(len(all_service_messages)):
            print(i)
            days=all_service_messages[i]["days_till_end"]+1
            if days<=-1 and days!=-10 and days!=-3:
                
                wait_until_send_photo(photo=photo,id=all_service_messages[i]["id"],caption="""Добрый день! Наверняка, вы убедились, что последнее время вам гораздо сложнее принимать решения, возникают непредвиденные трудности, да и в общем жизнь дается вам тяжелее обычного? 

Оформите прямо сейчас подписку на Астробота, который составляет для вас ежедневный персональный гороскоп с учетом вашей натальной карты, и вы сможете строить планы, разбираться в различных ситуациях и получать максимум от каждого дня! Чтобы подписаться нажмите /subscribe""",reply_markup=keyboard,parse_mode="html")
                time.sleep(1/15)
    except Exception as err:
        logger.warning(err)

        
# -------------------------------------Make shedule every day

from config import managers
from utils import logger

DATE_FORMAT = '%d.%m.%Y'

# from apscheduler.schedulers.background import BackgroundScheduler

# scheduler = BackgroundScheduler()

def remind_managers():
    tomorrow = date.today() + timedelta(days=1)
    tomorrow_date = datetime.strftime(tomorrow, DATE_FORMAT)

    posts = get_posts(create_session(), date = tomorrow_date)

    if posts:
        logger.info('Post is already scheduled')
        return

    logger.warning('Managers did not schedule any posts')
    logger.info("Reminding managers...")

    for manager in managers:
        logger.debug(f"Remind message sent to {manager}")
        wait_until_send(manager, "*На завтра не было запланировано ни одного поста!*", parse_mode="Markdown")

REMIND_TIME = '20:00'

def mail_horoscope_after_photo(id,pict,first_part,second_part):
    wait_until_send_photo(id,pict,first_part,parse_mode="html")
    time.sleep(1/10)
    wait_until_send(id,second_part,parse_mode="html")