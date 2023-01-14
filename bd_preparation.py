from databaseInteraction import *
from openpyxl import *
from horoscopedb import *
import sys
# import parse_sources
from controller import *
import databaseInteraction
from datetime import datetime,timedelta

def transfer_to_success_payment(file):
    workbook = load_workbook(file)
    sheet=workbook.get_sheet_by_name('base')
    i=2
    session=sessionmaker(engine,autoflush=False)()
    while True:
        
        inv_id=str(sheet["A"+str(i)].value)
        if inv_id=="" or inv_id=="None":
            break

        
        x=session.query(SuccessPayment).filter_by(payment_id=inv_id).all()
        if len(x)==0:
            
            price=int(str(sheet["C"+str(i)].value))
            date=sheet["J"+str(i)].value
            # date=datetime.strptime(date,"%d.%m.%y %H:%M")
            params=str(sheet["L"+str(i)].value)
            try:
                params=params.split("&")
                kwargs={}


                for j in range(len(params)):
                    params[j]=params[j].split("=")
                    dictionary=params[j]
                    kwargs[dictionary[0]]=dictionary[1]
            except:
                i+=1
                continue
            days=int(kwargs["Shp_days"])

            active_until=date+timedelta(days=days)
            telegram_id=kwargs["Shp_id"]
            if "Shp_prev" in kwargs.keys():
                prev_id=kwargs["Shp_prev"]
            else:
                prev_id=None
            all_success_payments=session.query(SuccessPayment).filter_by(telegram_id=telegram_id).all()

            user=session.query(User).filter_by(TelegramID=telegram_id).first()
            try:
                payment_id=int(all_success_payments[0].payment_id)
                for pay in all_success_payments:
                    if int(pay.payment_id)<=payment_id:
                        payment_id=pay.payment_id
                    else:
                        if pay.type_of_payment!="SELF PAID":
                            session.query(SuccessPayment).filter_by(payment_id=pay.payment_id).update({
                            "type_of_payment":"SELF PAID"
                })
            except:
                payment_id=100000
            try:
                birth_day=datetime.strptime(user.Birthday,"%d.%m.%Y")
            except:
                birth_day=datetime.strptime("00:00","%H:%M")
            if user==None:
                    user_name=""
                    source_id=0
            else:
                user_name=user.Name
                source_id=user.Source_ID
            if prev_id!=None:


                new_payments=SuccessPayment(
                    telegram_id=telegram_id,
                    payment_id=inv_id,
                    days=days,
                    amount=price,
                    payment_date=date,
                    active_until=active_until,
                    user_name=user_name,
                    source_id=source_id,
                    payed=1,
                    type_of_payment="REC",
                    birth_day=birth_day
                )

                session.add(new_payments)
            elif int(payment_id)>int(inv_id):


                try:
                    session.query(SuccessPayment).filter_by(payment_id=all_success_payments[0].payment_id).update({
                    "type_of_payment":"SELF PAID"
                })
                except:
                    pass

                try:
                    birth_day=datetime.strptime(user.Birthday,"%d.%m.%Y")
                except:
                    birth_day=datetime.strptime("00:00","%H:%M")
                
                new_payments=SuccessPayment(
                    telegram_id=telegram_id,
                    payment_id=inv_id,
                    days=days,
                    amount=price,
                    payment_date=date,
                    active_until=active_until,
                    user_name=user_name,
                    source_id=source_id,
                    payed=1,
                    type_of_payment="FIRST PAY",
                    birth_day=birth_day
                )
                session.add(new_payments)


            else:


                new_payments=SuccessPayment(
                    telegram_id=telegram_id,
                    payment_id=inv_id,
                    days=days,
                    amount=price,
                    payment_date=date,
                    active_until=active_until,
                    user_name=user_name,
                    source_id=source_id,
                    payed=1,
                    type_of_payment="SELF PAID",
                    birth_day=birth_day
                )
                session.add(new_payments)
        session.commit()

        i+=1
    print(workbook)

def add_triggers():
    try:

        conn=ConnectDb()
        cur=conn.cursor()
        cur.execute(""" DROP TRIGGER change_price_of_source_person""")
        # cur.execute(""" DROP TRIGGER change_price_of_source_costumer""")
        # cur.execute(""" DROP TRIGGER change_price_of_source_ended_reg""")

        conn.commit()
        # x="""
        # delimiter //

        #         CREATE TRIGGER change_price_of_source_person BEFORE UPDATE ON Sources
        #          FOR EACH ROW
        #          BEGIN
        #          IF(NEW.amount_of_persons!=0 AND NEW.amount_of_customers!=0 AND NEW.amount_of_persons_who_ended_registr!=0)
        #             SET NEW.price_for_person = NEW.price/NEW.amount_of_persons ,
        #             NEW.price_for_customer = NEW.price/NEW.amount_of_customers,
        #             NEW.price_for_ended_reg = NEW.price/NEW.amount_of_persons_who_ended_registr;
        #             END IF;
        #         END;//
        #         """
        # cur.execute(x)

        conn.commit()
        cur.close()





    except Exception as err:
        print(f'error in function: {err}')

        
def upload_information_to_source():
    session=sessionmaker(engine)()
    session_web=sessionmaker(engine_web)()
    sources=session_web.query(WebSource).all()
    for i in range(len(sources)):
        try:
            code=sources[i].code
        except:
            code=0
        users_who_started_registration=session.query(databaseInteraction.User).filter_by(Source_ID=code).count()
        users_who_didint_ended_reg=session.query(databaseInteraction.User).filter_by(DesTime_ID=None,Source_ID=code).count()
        all_costumers=session.query(SuccessPayment).filter_by(type_of_payment="FIRST PAY",source_id=code).count()
        all_payments=session.query(SuccessPayment).filter_by(source_id=code).count()
        all_profit=0

        all_pay=session.query(SuccessPayment).filter_by(source_id=code).all()
        for pay in all_pay:
            all_profit+=int(pay.amount)

        amount_of_persons_who_ended_registr=users_who_started_registration-users_who_didint_ended_reg
        kwargs=dict()

        if all_payments==0:
            all_payments=1
            kwargs["payment_exists"]=False
        if all_costumers==0:
            all_costumers=1
            kwargs["customer_exists"]=False
        if users_who_started_registration==0:
            users_who_started_registration=1
        if amount_of_persons_who_ended_registr==0:
            amount_of_persons_who_ended_registr=1
        price=sources[i].price
        kwargs["profit"]=all_profit
        kwargs["amount_of_persons"]=users_who_started_registration
        kwargs["amount_of_persons_who_ended_registr"]=amount_of_persons_who_ended_registr
        kwargs["amount_of_payments"]=all_payments
        kwargs["amount_of_customers"]=all_costumers
        kwargs["price_for_person"]=price//users_who_started_registration
        kwargs["price_for_customer"]=price//all_costumers
        kwargs["price_for_ended_reg"]=price//amount_of_persons_who_ended_registr
        session_web.query(WebSource).filter_by(code=sources[i].code).update(kwargs)
    session.commit()   
    session_web.commit()


def tranfer_payments(date=None):
    session=Session()
    if date!=None:
        list_of_pay=session.query(SuccessPayment).filter_by(payment_date=date).all()
    else:
        list_of_pay=session.query(SuccessPayment).all()
    session_web=SessionWeb()
    for pay in list_of_pay:
        telegram_id=pay.telegram_id
        payment_id=pay.payment_id
        active_until=pay.active_until
        days=pay.days
        payed=pay.payed
        amount=pay.amount
        type_of_payment=pay.type_of_payment
        source_id=pay.source_id
        user_name=pay.user_name
        birth_day=pay.birth_day
        payment_date=pay.payment_date
        if type_of_payment=="TRY REC":
            is_reccurent_success=0
        else:
            is_reccurent_success=1
        pay=WebSuccessPayment(
            telegram_id=telegram_id,
            payment_id=payment_id,
            active_until=active_until,
            days=days,
            payed=payed,
            amount=amount,
            type_of_payment=type_of_payment,
            source_id=source_id,
            user_name=user_name,
            birth_day=birth_day,
            payment_date=payment_date,
            is_reccurent_success=is_reccurent_success
        )
        session_web.add(pay)
    session_web.commit()
    session.commit()





def delete_yandex_pay(file):
    workbook = load_workbook(file)
    sheet=workbook.get_sheet_by_name('base')
    i=2
    session=sessionmaker(engine,autoflush=False)()
    while True:
        payment_type=str(sheet["B"+str(i)].value)
        inv_id=str(sheet["A"+str(i)].value)
        if payment_type!="RUR Bank Card" and inv_id!='None':
            
            pay=session.query(SuccessPayment).filter_by(payment_id=int(inv_id)).all()

            if len(pay)!=0:
                pay=pay[0]
                sub=session.query(Subscription).filter_by(TelegramID=pay.telegram_id).all()
                if len(sub)!=0:
                    try:
                        delete_sub(id=pay.telegram_id)
                    except:
                        pass
        i+=1
       
#RUR Bank Card

# x=transfer_to_success_payment("base.xlsx")
# delete_yandex_pay("base.xlsx")
# # add_triggers()
# upload_information_to_source()