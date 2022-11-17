DATA="16.06.2022"
import datetime

from sqlalchemy import null
# from socket import J1939_PGN_ADDRESS_COMMANDED
import config
import requests
TOKEN=config.TOKEN
import base64
from schedule import every, repeat, run_pending
import time

import telebot
import asyncio
import urllib.request as urllib2
import json
import os
import schedule
import time
from threading  import Thread
from schedule import repeat, every
def retranslate_media(file_id):
    bot = telebot.TeleBot(TOKEN)
    
    file_info = bot.get_file(file_id)
    # print(file_info,"file info")
    src="http://api.telegram.org/file/bot"+TOKEN+"/"+file_info.file_path
    # print(src)
    opened_file= urllib2.urlopen(src).read()
    return(opened_file)
def malll(Url, params,files):
    print(requests.post(url=Url, params=params,files=files).text)
    
def sender(type_of_content):
    data1=datetime.date.today()
    
    # print(data1)
    # print(type(data1))
    # print(dir(data1))
    mon=str(data1.month)
    day=str(data1.day)
    year=str(data1.year)
    if len(mon)<2:
        mon="0"+mon
    if len(day)<2:
        day="0"+day
    data=day+"."+mon+"."+year
    length_of_dir=os.listdir(type_of_content+"/"+data)
    # print(data)
    
    for i in range(1,len(length_of_dir)+1):
        try:

            print(len(length_of_dir))
            f=open(type_of_content+"/"+data+"/"+str(i)+".json","r")
            json_obj=json.loads(f.read())
            # print(json_obj)
            files={}
            content_type=json_obj["content_type"]
            tok=json_obj["TOKEN"]
            file=retranslate_media(json_obj["photo"])
            del(json_obj["photo"])
            # print(json_obj)
            # print(json_obj)
            
            media=[]
            Url = "https://api.telegram.org/bot"+tok+"/sendMediaGroup"
            # new_par={
            #     "chat_id":CHAT_ID,
            #     "media":media
            # }
            # media=json.dumps(media)
            if json_obj["caption"]==None:
                # print("capt null")
                json_obj["caption"]=" "
            # print(json_obj["caption"])
            # print(type(json_obj["caption"]))
            # print(new_par)
            media.append({"type": content_type, "media": "attach://"+content_type+str(0),"caption":json_obj["caption"],"caption_entities":json_obj["caption_entities"]})
            del(json_obj["caption"])
            del(json_obj["caption_entities"])
            files["photo"+str(0)] = file
            params = {
                "parse_mode": "html",
                "media":
                json.dumps(media)
            }
            del(file)
            # print(params)
            task=[]
            users=["952863788"]
            tim_betw=time.time()
            # for i in range(100):
            #     users.append(users[0])
            for i in range(len(users)):
                time.sleep(0.00000001)
                params["chat_id"]=str(users[i])
                Thread(target=malll,args=(Url,params,files,)).start()
        except Exception as err:
            print(err)
            continue
    return(0)
print(time.time())
tim1=time.time()
tim_bet=sender("person")
tim_last=time.time()
print(tim_bet)
# print(str(tim_last-tim_bet),"time from start of mailing till end")
# print(str((tim_last-tim1),"time from start func to end "))
# all_jobs = schedule.get_jobs()
# print(all_jobs)
# schedule.every().day.at("16:04").do(sender,"school")
# all_jobs = schedule.get_jobs()
# # schedule.every(1).minutes.do(sender,"school")
# while True:
#     schedule.run_pending()
#     time.sleep(10)
#     print(schedule.get_jobs())
@repeat(every().day.at("11:16"))
def something():
    print(sender("person"))
all_jobs = schedule.get_jobs()
print(all_jobs)