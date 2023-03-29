text1=''' <a href='https://t.me/+U2gUa3vgt1lkYjMy'>Канал «мать двух чертят» </a>ведет обычная мама двух обычных подростков. Такое провокационное название автор придумала как противопоставление всем каналам с розовыми слюнями о прекрасном материнстве и детях-ангелочках. Чтобы сразу уже из названия было понятно, что на канале не стоит ждать текстов про то, что быть родителем – это просто. Автор не понаслышке знает, что ни разу не просто, хотя иногда и очень весело.

 <a href='https://t.me/+U2gUa3vgt1lkYjMy'>Канал «мать двух чертят»</a> – это возможность поделиться собственным опытом, мыслями о воспитании детей и историями, которые могут поднять настроение другим родителям или дать им повод задуматься. 

Если вы – идеальная мама самых воспитанных детей, которые учатся на одни пятерки,  едят только здоровую веду, не ругаются матом и дружат со всеми окружающими, тогда проходите мимо. А если вы – нормальная мама с обычными трудностями, вам точно будет интересно почитать «мать двух чертят». <a href='https://t.me/+U2gUa3vgt1lkYjMy'>Подписывайтесь!</a>
'''
path='days/add_mdc.jpg'
photo=open(path,"rb").read()
# photo=f.read()
import time
import telebot 
mark=telebot.types.InlineKeyboardMarkup()
but=telebot.types.InlineKeyboardButton(text='Подписаться на канал',url='https://t.me/+U2gUa3vgt1lkYjMy')
mark.add(but)
from databaseInteraction import *
from mailing import wait_until_send_photo, wait_until_send
from threading import Thread
session=sessionmaker(engine)()
users=session.query(User).filter(User.SubscrType_ID==5,User.IsActiveBot==1).all()
# users=session.query(User).filter(User.TelegramID==5127634821).all()
# 5127634821
# 952863788
# def wait_until_send_photo(id,photo,caption,reply_markup=None,parse_mode=None,url=None):
i=0
for user in users:
    Thread(target=wait_until_send_photo,kwargs=({"id":user.TelegramID,"photo":photo,"caption":text1,"reply_markup":mark,"parse_mode":"html"})).start()
    
    if i%5000==0:
        wait_until_send(952863788,"номер:"+str(i))
        wait_until_send(5127634821,"номер:"+str(i))
    i+=1 
    time.sleep(1/10)
# from datetime import datetime
# # from databaseInteraction import *
# subs=session.query(Subscription).all()
# count=0
# ues=datetime.strptime("29.03.2023","%d.%m.%Y")
# now=datetime.now()
# for sub in subs:
#     date=datetime.strptime(sub.End,"%d.%m.%Y")
#     if date>=ues:
#         count+=1 
# print(count)
# # from databaseInteraction import *
# dicti={30:{},180:{},365:{}}
# dicti2={30:0,180:0,365:0}
# list_of_base=[]
# pays=session.query(User).filter(User.SubscrType_ID==3, ).all()
# for pay in pays:
#     if not (pay.TelegramID in list_of_base):
#         if get_sub(pay.TelegramID)==None:
#             continue
#         after_pays=session.query(Payment).filter(Payment.telegram_id==pay.TelegramID,Payment.amount!=0,Payment.payed==1).all()
#         maxi_days=0
#         for i in range(len(after_pays)):
#             if after_pays[i].days>=maxi_days:
#                 maxi_days=after_pays[i].days
#         try:
#             if not (len(after_pays) in dicti[maxi_days]):
#                 dicti[maxi_days][len(after_pays)]=0
#         except:
#             dicti[maxi_days]={}
#             if not (len(after_pays) in dicti[maxi_days]):
#                 dicti[maxi_days][len(after_pays)]=0
#         # if len(after_pays)>37:
#         #     print(pay.telegram_id)
#         #     break
#         # if maxi_days==180 and len(after_pays) in [3,4]:
#         #     print(pay.telegram_id)
#         try:
#             dicti2[maxi_days]+=1
#         except:
#             dicti2[maxi_days]=1
#         dicti[maxi_days][len(after_pays)]+=1
#         list_of_base.append(pay.TelegramID)
# print(dicti)
# print(dicti2)