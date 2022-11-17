import os
from attr import attr
import requests
import json
import hashlib
email = 'test@test.com';
emailCompany = 'testCompany@test.com';
phone = '89179990000';



isShipping = False;
hash_object = hashlib.sha256(b'Hello World')
url="https://securepay.tinkoff.ru/v2/"
TerminalKey="1655217292751DEMO"#1655217292751DEMO
id=952863788
password="yzstq8hiehznrvxs"
token=[ 
    {"PaymentId":password}, 
    {"TerminalKey":TerminalKey}]
text=""
for i in token:
    print(str(i))
    for j in i:
        text+=i[j]
print(text)
text=bytes(text,"utf-8")
text=hashlib.sha256(text)
text=text.hexdigest()
print(text)

DATA    = {
                    'Email'          :"sergey07050924@gmail.com",
                    'Connection_type' :'example'
                }
receipt={'EmailCompany' :"sergey07050924@gmail.com",
    'Email'        : "sergey0705092@gmail.com",
    'Taxation'     : "100",
    'Items':"subscribe"}

params={
      "TerminalKey": TerminalKey,
    "Amount": "5000",
    "OrderId": str(id),
    "Description": "Подписка на гороскоп",

}
def Get_State(payment_id):
    token=[ 
    {"PaymentId":int(payment_id)}, 
    {"TerminalKey":TerminalKey}]
    text=""
    byt=bytes()
    for i in token:
        print(str(i))
        for j in i:
            text=str(i[j])
            byt+=bytes(text,"utf-8")
    
    text=byt
    text=hashlib.sha256(text)
    token=text.hexdigest()
    print(token)
    params={
    "TerminalKey" : TerminalKey,
    "PaymentId" : int(payment_id),
    "Token" : token
    }
    arams=json.dumps(params)
    headers={"Content-Type": "application/json"}
    req=requests.post("https://securepay.tinkoff.ru/v2/GetState",data=params,headers=headers)
    txt=req.text
    print(txt)
    try:
        txt=json.loads(txt)

        return(txt)
    except:
        return(False)
def Init_tin_payment(price,id):
    params={
      "TerminalKey": TerminalKey,
    "Amount": str(price*100),
    "OrderId": str(id),
    "Description": "Подписка на гороскоп в телеграмм",
    "Recurrent":"Y",
    "CustomerKey":str(id)}
    params=json.dumps(params)
    headers={"Content-Type": "application/json"}
    req=requests.post("https://securepay.tinkoff.ru/v2/Init",data=params,headers=headers)
    txt=req.text
    txt=json.loads(txt)
    return(txt)
# def 

obj=Init_tin_payment(50,id=id)
pay_id=obj["PaymentId"]
print(Get_State(pay_id))
