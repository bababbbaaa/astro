import sys
# sys.path.append("../")
from datetime import datetime,timedelta
from mailing import *
session=sessionmaker(engine)()
from databaseInteraction import *

date1=datetime.strptime("23.01.2023","%d.%m.%Y")
date_yesterday=datetime.now()-timedelta(days=1)
# session.query(User).filter_by(SubscrType_ID=3)
user = select(User)

user=user.where(User.ActiveUntil<=date1)
user=user.where(User.SubscrType_ID==3)
session.query(User).filter(User.SubscrType_ID==3,User.ActiveUntil<=date1).update({"SubscrType_ID":5,"ActiveUntil":date_yesterday})
session.commit()
session=sessionmaker(engine)()
# recurent_subs=session.query(Subscription).all()
# i=0

# DATA=datetime.strptime("01.01.2023","%d.%m.%Y")


# while i<len(recurent_subs):
#     date1=recurent_subs[i].End
#     date1=datetime.strptime(date1,"%d.%m.%Y")
#     if not (date1>DATA and date1<date_yesterday):
#          recurent_subs.pop(i)
#     else:
#          i+=1
# with open("data.txt","w") as file:
#     text=""
#     for i in range(len(recurent_subs)):
#         text+="\n"+str(recurent_subs[i].TelegramID)
#     print(text,file=file)
# for i in range(len(recurent_subs)):
            
#             # print(0)
            
#             # print(recurent_subs[i].PayID,"Pay1111")
#             if recurent_subs[i].Type==3:
#                 amount=69
#             else:
#                 amount=config.cost
#             days1=30
#             if int(float(recurent_subs[i].Type))==330 or int(float(recurent_subs[i].Type==config.cost[180])):
#                 days1=180
#             if int(float(recurent_subs[i].Type))==580 or int(float(recurent_subs[i].Type==config.cost[365])):
#                 days1=365
#             pay=for_payments.get_money_for_sub(id=int(recurent_subs[i].PayID),amount=int(float(recurent_subs[i].Type)),days=days1,test=0,tg_id=recurent_subs[i].TelegramID)
#             # minues_one_try(telegram_id=recurent_subs[i].TelegramID)
#             # from_old_sub_to_new(recurent_subs[i].TelegramID)
#             # print(pay.text)
#             try:
#                 if "ERROR" not in pay.text:#Если автоплатеж не удался, то включается функция,которая закидывает информацию о автоплатеже а таблицу payments, Где проверяется то, оплатили ли счет
#                     # set_field(id=int(recurent_subs[i].TelegramID),end=end)
#                     try:
#                         add_success_payment(telegram_id=recurent_subs[i].TelegramID,payment_id=str(count_payments()),days=30,price=0,type_of_payment="TRY REC")
#                     except:
#                         pass
#                     add_payment(sub_type=3,telegram_id=recurent_subs[i].TelegramID,payment_id=str(count_payments()),active_until="01.10.1000",days=days1,payed=True,amount=0,link="try REC")

#                 else:
#                     try:
#                         add_success_payment(telegram_id=recurent_subs[i].TelegramID,payment_id=str(count_payments()),days=30,price=0,type_of_payment="TRY REC")
#                     except:
#                         pass
#                     # add_payment(sub_type =2,telegram_id = id,payment_id = payment_id,active_until = active_until,days = days,payed = False,amount = config.cost[days],link = url)
#             except Exception as err:
#                 try:
#                     wait_until_send(952863788,str(err))
#                 except:
#                     pass
#                 continue
#         # try:
#         #     wait_until_send(952863788,"списание закончилось")
#         # except:
#         #     pass