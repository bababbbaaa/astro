
from databaseInteraction import *


import databaseInteraction

def upload_information_to_source():
    session=Session()
    session_web=SessionWeb()
    sources=session.query(Source).all()
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

        kwargs["profit"]=all_profit
        kwargs["amount_of_persons"]=users_who_started_registration
        kwargs["amount_of_persons_who_ended_registr"]=amount_of_persons_who_ended_registr
        kwargs["amount_of_payments"]=all_payments
        kwargs["amount_of_customers"]=all_costumers
        session_web.query(Source).filter_by(code=sources[i].code).update(kwargs)
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
        payments=session_web.query(WebSuccessPayment).filter_by(payment_id=payment_id).first()
        if payments==None:
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

tranfer_payments(date=datetime.today())

upload_information_to_source()