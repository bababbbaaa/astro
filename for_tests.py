import functions
import config
from threading import Thread
import telebot
bot = telebot.TeleBot(config.TOKEN, parse_mode=None)
import time
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
                # horoscopeusr.ChUserInfo(inpValue=0,inpTelegramID=str(id),inpFieldName="IsActiveBot" )
                return err
            else:
                return err
def text_for_notifications(day,name,gender):
    day=int(day)
    if gender==1:
        dear="Дорогой"
    else:
        dear="Дорогая"
    if day==3:
        text="<b>"+dear+" "+name+"!"+'''

Спасибо, что Вы пользуетесь Астроботом!</b> 

Мы надеемся, что наш персональный гороскоп помогает лучше реализовывать ваши планы и выстраивать отношения с людьми. 

До конца пробного периода осталось всего 3 дня и мы подготовили для Вас специальное ПЕРСОНАЛЬНОЕ предложение, чтобы Вы могли получать ежедневный гороскоп на максимально выгодных условиях. 

<b>Срок действия предложения ограничен. Для активации нажмите на кнопку 👇🏻</b>'''
    elif day==1:
        text="<b>"+dear+" "+name+"!"+'''

Спасибо, что Вы пользуетесь Астроботом!</b> 

Мы надеемся, что наш персональный гороскоп помогает лучше реализовывать ваши планы и выстраивать отношения с людьми. 

До конца пробного периода остался всего 1 день и Ваше специальное ПЕРСОНАЛЬНОЕ предложение все еще действует! 

<b>Напоминаем, что срок действия предложения ограничен. Для активации нажмите на кнопку 👇🏻</b> '''
    elif day==0:
        text="<b>"+dear+" "+name+"!"+'''

Ваш пробный период в Астроботе завершен.</b> 

Если Вы хотите по-прежнему получать Ваш ежедневный персональный гороскоп, Вам нужно оформить подписку. 

Выгоднее всего это это будет, если Вы активируете Ваше ПЕРСОНАЛЬНОЕ предложение со специальными ценами. 

<b>Для активации нажмите на кнопку 👇🏻</b>'''
    elif day==-3:
        text="<b>"+dear+" "+name+"!"+'''</b>

<b>Вы уже 3 дня не получали Ваш персональный гороскоп! Еще не соскучились по нему? </b>

Рады сообщить Вам, что Ваше ПЕРСОНАЛЬНОЕ предложение со специальными ценами на подписку все еще в силе! Для активации нажмите на кнопку 👇🏻'''

    elif day==-10:
        text="<b>"+dear+" "+name+"!"+'''</b>

Сегодня последний день, когда можно оформить подписку на Астробота, воспользовавшись вашим ПЕРСОНАЛЬНЫМ предложением. 

Для активации нажмите на кнопку 👇🏻'''
    return text
def make_notificartion_with_keyboard(id,photo,end_time,name,gender,caption=None):
    keyboard=telebot.types.InlineKeyboardMarkup()
    # but1 = telebot.types.InlineKeyboardButton(
    #     text="30 дней", callback_data="agr;30")
    # but2 = telebot.types.InlineKeyboardButton(
    #     text="180 дней", callback_data="agr;180")
    # but3 = telebot.types.InlineKeyboardButton(
    #     text="365 дней", callback_data="agr;365")
    # but4 = telebot.types.InlineKeyboardButton(
    #     text="Что входит в подписку?", callback_data="inf")
    # but5 = telebot.types.InlineKeyboardButton(
    # #     text="Назад", callback_data="full_back")
    # keyboard.row(but1, but2, but3)
    # keyboard.add(but4)
    # keyboard.add(but5)
    cod1="sal"
    but1=telebot.types.InlineKeyboardButton(text="Получить персональное предложение",callback_data=cod1)
    keyboard.add(but1)
    id=id

    
    x=wait_until_send_photo(id,caption=text_for_notifications(end_time,name,gender),photo=photo,reply_markup=keyboard,parse_mode="html")

all_service_messages=[functions.select_all_active_until_table(id=952863788)]
photos={}
photos["0"]=open("days/"+"0.jpg","rb").read()

photos["3"]=open("days/"+"3.jpg","rb").read()

photos["-3"]=open("days/"+"-3.jpg","rb").read()

photos["1"]=open("days/"+"1.jpg","rb").read()
photos["-10"]=open("days/"+"-10.jpg","rb").read()
# breakpoint()
for j in range(5):
    for i in range(len(all_service_messages)):
        try:
            days=all_service_messages[i]["days_till_end"]
            name=all_service_messages[i]["name"]
            gender=all_service_messages[i]["gender"]
            # if days==7:
            #     print(days)
            if days in config.days_for_mailing:
                
                # end_time=str(functions.select_all_active_until_table(id)["days_till_end"]+1)
                try:
                    id=all_service_messages[i]["id"]
                    Thread(target=make_notificartion_with_keyboard,args=(id,photos[str(days)],days,name,gender)).start()#Отправляем в процесс id
                except:
                    Thread(target=make_notificartion_with_keyboard,args=(id,photos[str(0)],days,name,gender)).start()#Отправляем в процесс id
                    # make_notificartion_with_keyboard(all_service_messages[i]["id"],photos[str(days)])
                finally:
                    time.sleep(1/15)
        except:
            continue