text1=''' <a href='https://t.me/+U2gUa3vgt1lkYjMy'>Канал «мать двух чертят» </a>ведет обычная мама двух обычных подростков. Такое провокационное название автор придумала как противопоставление всем каналам с розовыми слюнями о прекрасном материнстве и детях-ангелочках. Чтобы сразу уже из названия было понятно, что на канале не стоит ждать текстов про то, что быть родителем – это просто. Автор не понаслышке знает, что ни разу не просто, хотя иногда и очень весело.

 <a href='https://t.me/+U2gUa3vgt1lkYjMy'>Канал «мать двух чертят»</a> – это возможность поделиться собственным опытом, мыслями о воспитании детей и историями, которые могут поднять настроение другим родителям или дать им повод задуматься. 

Если вы – идеальная мама самых воспитанных детей, которые учатся на одни пятерки,  едят только здоровую веду, не ругаются матом и дружат со всеми окружающими, тогда проходите мимо. А если вы – нормальная мама с обычными трудностями, вам точно будет интересно почитать «мать двух чертят». <a href='https://t.me/+U2gUa3vgt1lkYjMy'>Подписывайтесь!</a>
'''
path='days/add_mdc.jpg'
photo=open(path,"rb").read()
# photo=f.read()
import telebot 
mark=telebot.types.InlineKeyboardMarkup()
but=telebot.types.InlineKeyboardButton(text='Подписаться на канал',url='https://t.me/+U2gUa3vgt1lkYjMy')
mark.add(but)
from databaseInteraction import *
from mailing import wait_until_send_photo
from threading import Thread
session=sessionmaker(engine)()
users=session.query(User).filter(User.SubscrType_ID!=3,User.IsActiveBot==1).all()
# users=session.query(User).filter(User.TelegramID==5127634821).all()
# 5127634821
# 952863788
# def wait_until_send_photo(id,photo,caption,reply_markup=None,parse_mode=None,url=None):

for user in users:
    Thread(target=wait_until_send_photo,kwargs=({"id":user.TelegramID,"photo":photo,"caption":text1,"reply_markup":mark,"parse_mode":"html"})).start()


# from datetime import datetime
# # from databaseInteraction import *
# subs=session.query(Subscription).all()
# count=0
# now=datetime.now()
# for sub in subs:
#     date=datetime.strptime(sub.End,"%d.%m.%Y")
#     if date>now:
#         count+=1
# # print(count)
# # from databaseInteraction import *
# dicti={30:{},180:{},365:{}}
# list_of_base=[]
# pays=session.query(Payment).filter(Payment.link=="UNSUB", Payment.payment_id>=31071).all()
# for pay in pays:
#     if not (pay.telegram_id in list_of_base):

#         after_pays=session.query(Payment).filter(Payment.telegram_id==pay.telegram_id,Payment.amount!=0,Payment.payed==1).all()
#         maxi_days=0
#         for i in range(len(after_pays)):
#             if after_pays[i].days>=maxi_days:
#                 maxi_days=after_pays[i].days
#         if not (len(after_pays) in dicti[maxi_days]):
#             dicti[maxi_days][len(after_pays)]=0
#         if len(after_pays)>37:
#             print(pay.telegram_id)
#             break
#         if maxi_days==180 and len(after_pays) in [3,4]:
#             print(pay.telegram_id)

#         dicti[maxi_days][len(after_pays)]+=1
#         list_of_base.append(pay.telegram_id)
# print(dicti)