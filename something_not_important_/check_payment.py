
from datetime import date,timedelta,datetime
from threading import Thread
from databaseInteraction import *
import config
from telebot import types
import telebot
import for_payments
import time
from yookassa import Payment as Pay
TOKEN=config.TOKEN
delete_cache={}
import horoscopeproc as horoscopeproc
import horoscopeusr as horoscopeusr
bot = telebot.TeleBot(TOKEN, parse_mode=None)
from horoscopeusr import ChUserInfo
def change_active_until_date(start,date_end,days,base="subs"):
    if datetime.strptime(start,DATE_FORMAT)>=datetime.strptime(date_end,DATE_FORMAT):
        uctive_until=datetime.strptime(start,DATE_FORMAT)+timedelta(days=days)
    else:
        uctive_until=datetime.strptime(date_end,DATE_FORMAT)+timedelta(days=days)
    if base=="users":
        end=datetime.strftime(uctive_until, "%Y-%m-%d")
    else:
        end = datetime.strftime(uctive_until, DATE_FORMAT)
    return(end)

def wait_until_send(id,text,reply_markup=None,parse_mode=None,url=None):
    while True:
        try:
            mes=bot.send_message(id,text,reply_markup=reply_markup,parse_mode=parse_mode)
            return mes
        except Exception as err:
            if 'error_code' not in vars(err).keys():
                return 0
                
            if err.error_code==429:
                continue

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



def payment_cancelled(id):
    keyboard=types.InlineKeyboardMarkup()
    but1=types.InlineKeyboardButton(text="Активировать подписку", callback_data="2opt;"+str(1))
    keyboard.row(but1)
    wait_until_send(id,'Не уадлось оформить подписку, просим вас попробовать снова',reply_markup=keyboard)

def __main__():
    def insert_into_subs(id):
        return
    while True:
        payments=get_payments()
        for i in range(len(payments)):
            payment_request=payments[i]
            payment_response = Pay.find_one(payment_request.payment_id)
            if payment_response.status=="canceled":
                Thread(target=payment_cancelled,args=(payment_request.telegram_id,)).start()
                delete_payment(payment_request.telegram_id)
            elif payment_response.paid==True:
                try:
                    # print(dir(payment_response))
                    metadata=payment_response.metadata
                    pay_id=payment_response.payment_method.id
                    days=metadata["days"]
                    id=metadata["telegram_id"]
                    end=change_active_until_date(start=for_payments.Get_Data(),date_end=metadata["date_end"],days=int(days))
                    end_for_users=change_active_until_date(start=for_payments.Get_Data(),date_end=metadata["date_end"],days=int(days),base="users")
                    if get_sub(id)!=None:
                        delete_sub(id)
                    add_sub(id=id,start=for_payments.Get_Data(),end=end,pay_id=pay_id)
                    ChUserInfo(inpTelegramID=id,inpFieldName="ActiveUntil",inpValue=end_for_users)
                    delete_payment(str(metadata["telegram_id"]))
                    ChUserInfo(inpTelegramID=id,inpFieldName="IsActiveSub",inpValue=1)
                    wait_until_send(id,config.thanks_for_payment)
                except Exception as err:
                    print(err)
                    break
            else:
                # try:
                #     print(dir(payment_response.confirmation))
                #     print(payment_response.confirmation.confirmation_url)
                #     print(dir(payment_response.confirmation))
                # except:
                pass
        time.sleep(4)
__main__()