# # from urllib import request
# from re import X
# import telebot 
# # import requests
# # from threading import Thread
# # import horoscopeusr
# # import config
# # import for_payments
# # import telebot
# # from telebot import types
# # from posixpath import abspath
# # import functools
# # import string
# # import functions
# # from calendar import Calendar
# # import string
# # from sqlalchemy import *
# # from sqlalchemy.orm import sessionmaker
# # import horoscopedb
# # from databaseInteraction import *
# # from datetime import date, timedelta
# # from datetime import datetime as date_time

# # from rich.console import Console
# # request1=requests.post("http://127.0.0.1:5000/get_payment",data={"out_summ":69.000000,"OutSum":69.000000,
# # "inv_id":10,"InvId":10919,"crc":"7B9A8D50DF7D3F8EF9338CBD8AE1E127","SignatureValue":"7B9A8D50DF7D3F8EF9338CBD8AE1E127","PaymentMethod":"BankCard","IncSum":69.000000,"Shp_days":30,"Shp_id":952863788
# # })
# # # import horoscopeproc

# # from utils import *

# # TOKEN = config.TOKEN
# # delete_cache = {}
# # bot = telebot.TeleBot(TOKEN, parse_mode=None)
# # for i in range(1719514-1000,1719514+10):
# #     try:
# #         mes=bot.forward_message(952863788,1057824180,message_id=i)
# #         print(mes)
# #         break
# #     except Exception as err:
# #         print(err)
# #         continue
# # us_info=bot.get_chat_member(1057824180,1057824180)
# # print(us_info)
# # messages.getMessages
# # conn=horoscopedb.ConnectDb()
# # cur = conn.cursor()   
# # cur.execute("SELECT * FROM Users")
# # res = list()
# # records = cur.fetchall()
# # cur.close()
# # conn.commit()
# # for row in records:
# #     res.append({"ID":row[0],"Name":row[1],"is_main":row[2],"BirthTime":row[4],
# # "Birthday":row[5],"Gender_ID":row[3],'Birthplace':row[6],"DesTime_ID":row[7],
# # "TimeZone":row[8],"TelegramID":row[9],"RegDate":row[10],"IsActiveBot":row[12],
# # "Balance":row[13],"IsActiveSub":row[14],"SubscrType_ID": row[15],
# # "ActiveUntil":row[16],"DateSend":row[17],"Source_ID":row[22]
# # })
# # # message_id=1719513
# # # # res.reverse()
# # # # print(res)
# # # # result1=0
# # # # while True:
# # # #     try:
# # # #         print(result1)
# # # #         result=res[result1]
# # # #         result1+=1
# # # #         mes=bot.forward_message(952863788,1057824180,message_id=message_id)
# # # #         print(mes)
# # # #         print(result["TelegramID"])
# # # #         # if mes.
        
# # # #         if int(result["TelegramID"])==5127634821:
# # # #             message_id-=1
# # # #             result1=0
# # # #         else:
# # # # #             break
# # # # #     except Exception as err:
# # # # # #         # print(err)
# # # # add_payment(sub_type=3,telegram_id=1,payment_id=str(count_payments()),active_until="10.10.1000",days=30,payed=True,amount=69,link="REC")
# # # # # #         continue
# # # # # pay=for_payments.get_money_for_sub(id=int(10332),amount=69,days=30,test=0)
# # # # # add_payment(sub_type=3,telegram_id=1,payment_id=str(count_payments()),active_until="10.10.10",days=30,payed=True,amount=69,link="REC")
# # # # # # print(pay.text)
# # # # # pay=for_payments.get_money_for_sub(id=int(10359),amount=69,days=30,test=0)
# # # # # print(pay.text)
# # # # # add_payment(sub_type=3,telegram_id=1,payment_id=str(count_payments()),active_until="10.10.1000",days=30,payed=True,amount=69,link="REC")

# # # # # pay=for_payments.get_money_for_sub(id=int(10378),amount=69,days=30,test=0)
# # # # # print(pay.text)
# # # # # add_payment(sub_type=3,telegram_id=1,payment_id=str(count_payments()),active_until="10.10.1000",days=30,payed=True,amount=69,link="REC")
# # # # LOGIN="Astrobot"
# # # # PASSWORD_FOR_ROBOKASSA="oLy0Vda8EbnP8wlR5Xi1"
# # # # # idempotence_key = str(uuid.uuid4())
# # # # account_id_shop="jkdskd"
# # # # gateway_id_shop=""
# # # # MAIN_PASSWORD="oLy0Vda8EbnP8wlR5Xi1"
# # # # TEST_PASSWORD="ygAdIPC6I1c1qxER1Iu8"
# # # # # pay=for_payments.get_money_for_sub(id=int(10853),amount=69,days=30,test=0,tg_id=)
# # # # # # print(pay.text)
# # # # # # add_payment(sub_type=3,telegram_id=1,payment_id=str(count_payments()),active_until="10.10.10",days=30,payed=True,amount=69,link="REC")

# # # # # pay=for_payments.get_money_for_sub(id=int(10210),amount=69,days=30,test=0)
# # # # # print(pay.text)
# # # # # add_payment(sub_type=3,telegram_id=1,payment_id=str(count_payments()),active_until="10.10.10",days=30,payed=True,amount=69,link="REC")

# # # # import robokassa
# # # # # add_payment(sub_type=3,telegram_id=2,payment_id=str(count_payments()),active_until="01.10.1000",days=30,payed=True,amount=0,link="try REC")
# # # # x=robokassa.earn_recurrent_pay("Astrobot",PASSWORD_FOR_ROBOKASSA,cost=69,number=10853,description="Оплата подписки на астробота",is_test=0,days=30,tg_id=5088332038)
# # # # print(x)
# # # # pass 
# # # DATE_FORMAT = '%d.%m.%Y'
# # # from datetime import date,timedelta

# # # import datetime
# # # # def change_active_until_date(start,date_end,days,base="subs"):
# # # #     if date_end.find("-")!=-1:
# # # #         date_end=datetime.strptime(date_end, "%Y-%m-%d")
# # # #         date_end=datetime.strftime(date_end, DATE_FORMAT)
# # # #     if datetime.strptime(start,DATE_FORMAT)>=datetime.strptime(date_end,DATE_FORMAT):
# # # #         uctive_until=datetime.strptime(start,DATE_FORMAT)+timedelta(days=days)
# # # #     else:
# # # #         uctive_until=datetime.strptime(date_end,DATE_FORMAT)+timedelta(days=days)
# # # #     if base=="users":
# # # #         end=datetime.strftime(uctive_until, "%Y-%m-%d")
# # # #     else:
# # # #         end = datetime.strftime(uctive_until, DATE_FORMAT)
# # # #     return(end)
# # # from sqlite3 import *
# # # conn = connect('horoscope.db')
# # # cur=conn.cursor()
# # # statements=cur.execute("SELECT * FROM Subscriptions")
# # # statements=statements.fetchall()
# # # for i in statements:
# # #     end=i[4]
# # #     if datetime.datetime.strptime(end,DATE_FORMAT)<=datetime.datetime.strptime("03.10.2022",DATE_FORMAT):
# # #         new_end=datetime.datetime.strptime(end,DATE_FORMAT)+timedelta(days=30)
# # #         new_end = datetime.datetime.strftime(new_end, DATE_FORMAT)
# # #         cur.execute("""UPDATE Subscriptions SET End = ? WHERE (ID = ?)""" ,(new_end,i[0]))
# # # cur.close()
# # # conn.commit()
# import config
# bot=telebot.TeleBot(token=config.TOKEN)
# # bot.forward_message(952863788,952863788,1635)
# # import horoscopeproc
# # id=494603937
# # # print(horoscopeproc.GenHourMessAll(
# # #                             11, inpTelegramID=str(id)))
# # import functions
# # import horoscopeusr
# # # or functions.ListUserName(inpTelegramID=id)[0]==None:
# # if horoscopeusr.RegUser(inpTelegramID=str(id))[0] == True:

# #     print(
# #                             id, '7Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
# # elif functions.ListUserName(inpTelegramID=id)[0] == "":

# #     print(
# #                             id, '2Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
# # else:
# #     us = functions.GetUsers(id)[0]
# #     if us["Name"] == None:
# #         print(
# #             id, '3Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')

# #     elif us["Birthday"] == None:
# #         print(
# #             id, '4Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
# #     elif us["BirthTime"] == None:
# #         print(
# #             id, '5Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
# #     elif us["Birthplace"] == None:
# #         print(
# #             id, '6Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
# #     elif us["RegDate"] == None:
# #         print(
# #             id, '9Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')

# #     else:
# #         # name=functions.ListUserName(inpTelegramID=int(id))[0]
        
# #         js = horoscopeproc.GenHourMessAll(
# #             11, inpTelegramID=str(id))
# #         txt = js[0]
# #         # print(js)
# #         today_send = txt[6]
# #         if functions.select_all_active_until_table(id)["days_till_end"]+1<=0:
# #             horoscopeusr.ChUserInfo(inpTelegramID=id,inpFieldName="SubscrType_ID",inpValue=5)
# #             horoscopeusr.ChUserInfo(inpFieldName="IsActiveSub",inpTelegramID=id,inpValue=0)
# #             # subscribe(message)
                                                                                                                                                                                                                
# #         elif today_send:
            
# #             text = ""
# #             text += (js[0][2]+"\n\n"+js[0][3])
# #             print(
# #                             id, '10Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
# #         else:
# #             text = ""
# #             text += (js[0][2]+"\n\n"+js[0][3])
# #             print(
# #                             id, '100Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')

# #             # bot.register_next_step_handler(mes,main)

# # import time
# # import horoscopeproc
# # import functions
# # horoscope=horoscopeproc.GenHourMessAll(11,110796470)
# # print(len(horoscope[0]))
# # x=functions.select_all_active_until_table(110796470)
# # print(x)
# x="https://t.me/+-k8MSbOEqeVhMzc6"
# print(x.split("-"))
# # from threading import Thread
# # def wait_until_send(id,text,reply_markup=None,parse_mode=None,url=None):
# #     while True:
# #         try:
# #             mes=bot.send_message(id,text,reply_markup=reply_markup,parse_mode=parse_mode)
# #             return mes
# #         except Exception as err:
            
# #             if 'error_code' not in vars(err).keys():
# #                 return 0
                
# #             if err.error_code==429:
# #                 return err

# #             elif err.error_code==400:
# #                 return err
# #             elif err.error_code==403:
# #                 return err
# # with open("НеОконченаРегистрация.txt","r") as x:
# #     x=x.readlines()
# #     for id in x:
# #         id=int(id)
# #         Thread(target=wait_until_send,args=(id,"Добрый день! Мы рады, что вы заглянули в наш Астробот. К сожалению, вы не закончили регистрацию, возможно, бот был перегружен обращениями и зависал. Мы будем рады, если вы попробуете зарегистрироваться еще раз - сейчас все должно работать хорошо. Для этого остановите и перезапустите Астробот и ответьте на вопросы заново. Если у вас все равно возникли проблемы с регистрацией, пожалуйста, напишите нам в поддержку в @AstroBot_support. Прекрасного дня! 🌸",None,"html")).start()
# #         time.sleep(1/28)
# import datetime
# # print(datetime.datetime.strftime(datetime.datetime.now(),"%H:%M"))
import horoscopeusr as horoscopeusr
import horoscopeproc
import functions
# print(horoscopeproc.GenHourMessAll(11,"245188029"))1358174961
import time
import functions
# time1=time.time()
# x=functions.GetUsers("952863788")
# time2=time.time()
# print(time2-time1)
# # print(x)
# time1=time.time()
# x=functions.RegMainUser("121313131")
# time2=time.time()
# print(time2-time1)
# time1=time.time()
# x=functions.GetUsers("1358174961")
# time2=time.time()
# print(time2-time1)
# # print(x)
# time1=time.time()
# x=horoscopeproc.GenHourMessAll(11,"1358174961")
# time2=time.time()
# print(time2-time1)
import horoscopedb
conn=horoscopedb.ConnectDb()
cur=conn.cursor()
res=cur.execute("SELECT * FROM Users")
print(res)