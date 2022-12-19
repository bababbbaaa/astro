from datetime import datetime , timedelta
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from posixpath import abspath
from os.path import join
from controller import engine, BaseWeb, Session,SessionWeb,engine_web


DATE_FORMAT = '%d.%m.%Y'



class WebSuccessPayment(BaseWeb):
    __tablename__="web_success_payments"

    ID = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    telegram_id = Column(Text)
    payment_id = Column(Text, nullable=False)
    active_until = Column(Date, nullable=False)
    days = Column(Integer, nullable=False)
    payed = Column(Boolean, nullable=False)
    amount = Column(Integer, nullable=False)
    type_of_payment = Column(Text, nullable=False)
    source_id=Column(BIGINT)
    user_name=Column(Text)
    birth_day=Column(Date)
    payment_date=Column(Date)
    is_reccurent_success=Column(Integer)

class WebSource(BaseWeb):
    __tablename__="web_sources"
    
    ID = Column(Integer, nullable=False, unique=True, primary_key=True)
    title = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    date = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    price_for_person=Column(Integer)
    price_for_customer=Column(Integer)
    profit=Column(Integer)
    amount_of_persons=Column(Integer)
    amount_of_customers=Column(Integer)
    amount_of_persons_who_ended_registr=Column(Integer)
    amount_of_payments=Column(Integer)
    price_for_ended_reg=Column(Integer)
    payment_exists=Column(Boolean)
    customer_exists=Column(Boolean)

# def add_web_payment(telegram_id,
# payment_id,
# active_untildays,
# days,
# payed,
# amount,
# ):
def add_web_source(
        title: str,
        code: str,
        price: int,
        date : str,
        type : str) -> WebSource:
    """
    У нас стоят триггеры на автоматический подсчет цены за человека,прищедего в бот,
    поэтому не меняй на 0 ни один из стобцов бд,который начинается на amount, иначе получищь +100500 ошибок 
    """
    # if not basic_check_date(date):
    #     raise Exception("Invalid date")

    source = WebSource(
        title=title,
        code=code,
        price=price,
        date=date,
        type=type,
        price_for_person=0,
        price_for_customer=0,
        amount_of_persons=1,
        amount_of_customers=1,
        amount_of_persons_who_ended_registr=1,
        amount_of_payments=1,
        profit=0,
        price_for_ended_reg=0,
        payment_exists=False,
        customer_exists=False
        )

    SessionWeb.add(source)
    SessionWeb.commit()

    return source




BaseWeb.metadata.create_all(engine_web)
