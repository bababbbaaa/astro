
# from os import confstr_names
import uuid
import time
import requests

from databaseInteraction.payments import Payment
from utils import logger
import json
merchant_password_2="x66wLEWHjhs5Se3C2Tzh"
from databaseInteraction.subscriptions import get_subs
LOGIN="Astrobot"
PASSWORD_FOR_ROBOKASSA="oLy0Vda8EbnP8wlR5Xi1"
idempotence_key = str(uuid.uuid4())
account_id_shop="jkdskd"
gateway_id_shop=""
MAIN_PASSWORD="oLy0Vda8EbnP8wlR5Xi1"
TEST_PASSWORD="ygAdIPC6I1c1qxER1Iu8"
terminal_key="1655217292751DEMO"
server_url="http://195.2.79.3:443/from_tinkoff"
url="https://securepay.tinkoff.ru/v2/"
import datetime
password="yzstq8hiehznrvxs"
import config

import robokassa
DATE_FORMAT = '%d.%m.%Y'
# Configuration.auth_token="test_hg21UOtBwCSu-Fbskhuy8FdTqycHUfycga-kdHg-VWo"

def Get_Data():
    return datetime.datetime.strftime(datetime.datetime.now(), DATE_FORMAT)

    
def make_payment(id,amount,days=30,test=0):
    if test==0:
        url=robokassa.generate_payment_link(LOGIN,MAIN_PASSWORD,cost=amount,number=id,description="Оплата подписки на астробота",is_test=0,days=days)
    else:
        url=robokassa.generate_payment_link(LOGIN,TEST_PASSWORD,cost=amount,number=id,description="Оплата подписки на астробота",is_test=1,days=days)
    return url
    
def make_recurse_pay(id,amount,days=30,test=0):
    if test==0:
        url=robokassa.generate_payment_link_recurse(LOGIN,MAIN_PASSWORD,cost=amount,number=id,description="Оплата подписки на астробота",is_test=0,days=days)
    else:
        url=robokassa.generate_payment_link_recurse(LOGIN,TEST_PASSWORD,cost=amount,number=id,description="Оплата подписки на астробота",is_test=1,days=days)
    return url       
def get_money_for_sub(id,amount=config.cost[30],days=30,test=0,tg_id=0):
    request=robokassa.earn_recurrent_pay("Astrobot",PASSWORD_FOR_ROBOKASSA,cost=amount,number=id,description="Оплата подписки на астробота",is_test=0,days=days,tg_id=tg_id)          
    return(request)
print(make_payment(952863788,69,30,1))
# def get_recurse_payment(id,amount=config.cost[30],days=30,test=0):

# request1=make_payment(100,69,test=1)
# # print(request1.text)
# # pay=get_state(json.loads(request1.text)["PaymentId"])
# print(request1)
# print()
# print(form_token({"Description":"test" ,
#     "Amount":"100000",
#     "TerminalKey":terminal_key,
#     "OrderId":"TokenExample"}))
# # print(form_token({"telegram_id":1,'{"Success":true,"ErrorCode":"0","TerminalKey":"1655217292751DEMO","Status":"NEW","PaymentId":"1537584969","OrderId":"None","Amount":6900,"PaymentURL":"https://securepayments.tinkoff.ru/RnTQJ20x"}'
#                     "days":2,
#                     "price":3,
#                     "date_end":4,
                    

# #         }))
# x=get_money_for_sub(952863793,amount=10)
# print(x)
# print(x.text)