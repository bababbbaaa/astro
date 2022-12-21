import decimal
import hashlib
from urllib import parse
from urllib.parse import urlparse

from requests import request
import requests
from databaseInteraction.payments import add_payment
from utils import *

import functions
#позиции наменклатуры для налогов
nomenklarue_30={
          "sno":"usn_income",
          "items": [
            {
              "name": "Подписка на астробот на 30 дней",
              "quantity": 1,
              "sum": 69,
              "payment_method": "full_payment",
              "payment_object": "commodity",
              "tax": "none"
            }]}
nomenklarue_180={
          "sno":"usn_income",
          "items": [
            {
              "name": "Подписка на астробот на 180 дней",
              "quantity": 1,
              "sum": 330,
              "payment_method": "full_payment",
              "payment_object": "commodity",
              "tax": "none"
            }]}

nomenklarue_365={
          "sno":"usn_income",
          "items": [
            {
              "name": "Подписка на астробот на 365 дней",
              "quantity": 1,
              "sum": 580,
              "payment_method": "full_payment",
              "payment_object": "commodity",
              "tax": "none"
            }]}
nomenklatura={30:nomenklarue_30,180:nomenklarue_180,365:nomenklarue_365}






def calculate_signature(*args) -> str:
    """Create signature MD5.
    """
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


def parse_response(request: str) -> dict:
    """
    :param request: Link.
    :return: Dictionary.
    """
    params = {}

    for item in urlparse(request).query.split('&'):
        key, value = item.split('=')
        params[key] = value
    return params


def check_signature_result(
    order_number: int,  # invoice number
    received_sum: decimal,  # cost of goods, RU
    received_signature: hex,  # SignatureValue
    password: str  # Merchant password
) -> bool:
    signature = calculate_signature(received_sum, order_number, password)
    if signature.lower() == received_signature.lower():
        return True
    return False


# Формирование URL переадресации пользователя на оплату.

def generate_payment_link(
    merchant_login:str,  # Merchant login
    merchant_password_1: str,  # Merchant password
    cost: decimal,  # Cost of goods, RU
    number: int,  # Invoice number
    description: str,  # Description of the purchase
    days=30,
    is_test = 0,
    
    robokassa_payment_url = 'https://auth.robokassa.ru/Merchant/Index.aspx',
) -> str:
    """URL for redirection of the customer to the service.
    """
    signature = calculate_signature(
        merchant_login,
        cost,
        0,
        merchant_password_1,
        "Shp_days="+str(days),
        "Shp_id="+str(number),
        
    )

    data = {
        'MerchantLogin': merchant_login,
        'OutSum': cost,
        'InvId': 0,
        'Description': description,
        'SignatureValue': signature,
        'IsTest': is_test,
        "Shp_id":number,
        "Shp_days":days,
    }
    return f'{robokassa_payment_url}?{parse.urlencode(data)}'


# Получение уведомления об исполнении операции (ResultURL).

def result_payment(merchant_password_2: str, request: str) -> str:
    """Verification of notification (ResultURL).
    :param request: HTTP parameters.
    """
    param_request = parse_response(request)
    cost = param_request['OutSum']
    number = param_request['InvId']
    signature = param_request['SignatureValue']

    signature = calculate_signature(cost, number, signature)

    if check_signature_result(number, cost, signature, merchant_password_2):
        return f'OK{param_request["InvId"]}'
    return "bad sign"

def generate_payment_link_recurse(
    merchant_login:str,  # Merchant login
    merchant_password_1: str,  # Merchant password
    cost: decimal,  # Cost of goods, RU
    number: int,  # Invoice number
    description: str,  # Description of the purchase
    days=30,
    is_test = 0,
    
    robokassa_payment_url = 'https://auth.robokassa.ru/Merchant/Index.aspx',
) -> str:
    """URL for redirection of the customer to the service.
    """
    signature = calculate_signature(
        merchant_login,
        cost,
        count_payments(),
        nomenklatura[days],
        merchant_password_1,
        "Shp_days="+str(days),
        "Shp_id="+str(number),
        
    )

    data = {
        'MerchantLogin': merchant_login,
        'OutSum': cost,
        'InvoiceID': count_payments(),
        'Description': description,
        'SignatureValue': signature,
        'IsTest': is_test,
        "Recurring":"true",
        "receipt":nomenklatura[days],
        "Shp_id":number,
        "Shp_days":days,
    }
    add_payment(sub_type=3,telegram_id=str(number),payment_id=number,active_until="01.01.0001",days=30,payed=False,amount=69,link="None")
    return f'{robokassa_payment_url}?{parse.urlencode(data)}'
# add_payment(sub_type=3,telegram_id=str(1),payment_id=1,active_until="01.01.0001",days=30,payed=False,amount=69,link="None")
# Проверка параметров в скрипте завершения операции (SuccessURL).
def earn_recurrent_pay(merchant_login:str,  # Merchant login
    merchant_password_1: str,  # Merchant password
    cost: decimal,  # Cost of goods, RU
    number: int,  # Invoice number
    description: str,  # Description of the purchase
    days=30,
    is_test = 0,
    tg_id=0):
    url="https://auth.robokassa.ru/Merchant/Recurring"
    number1=count_payments()
    signature = calculate_signature(
        merchant_login,
        cost,
        number1,
        # nomenklatura[days],
        # merchant_password_1,
        "Shp_days="+str(days),
        "Shp_id="+str(tg_id),
        # "Shp_id":number,
        # "Shp_days":days,
        # "Shp_Rec="+str(1),
        "Shp_prev="+str(number)
        
    )

    data = {
        'MerchantLogin': merchant_login,
        'OutSum': cost,
        'InvoiceID': number1,
        "PreviousInvoiceID":number,
        'Description': description,
        'SignatureValue': signature,
        'IsTest': is_test,
        # "receipt":nomenklatura[days],
        "Shp_id":tg_id,
        "Shp_days":days,
        # "Shp_Rec":1,
        "Shp_prev":number
        }
    print(data,"data")
    request=requests.post(url,data=data)
    return(request)
def check_success_payment(merchant_password_1: str, request: str) -> str:
    """ Verification of operation parameters ("cashier check") in SuccessURL script.
    :param request: HTTP parameters
    """
    param_request = parse_response(request)
    cost = param_request['OutSum']
    number = param_request['InvId']
    signature = param_request['SignatureValue']

    signature = calculate_signature(cost, number, signature)

    if check_signature_result(number, cost, signature, merchant_password_1):
        return "Thank you for using our service"
    return "bad sign"
# x=earn_recurrent_pay("Astrobot","ygAdIPC6I1c1qxER1Iu8",cost=69,number=952863788,description="Оплата подписки на астробота",is_test=0)

