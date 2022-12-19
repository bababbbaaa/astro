from datetime import datetime , timedelta
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from posixpath import abspath
from os.path import join
from controller import engine, BaseWeb, SessionWeb,engine_web


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
    user_name=Column(Text)
    source_id = Column(BIGINT)
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

    WebSource = WebSource(
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

    SessionWeb.add(WebSource)
    SessionWeb.commit()

    return WebSource

def update_web_source(code, new_title: str = None, new_price : int = None) -> None:
    """

    Меняет название источника

    """
    WebSource = get_web_source(code)
    
    if new_title is not None:
        setattr(WebSource, "title", new_title)

    if new_price is not None:
        setattr(WebSource, "price", new_price)
        
    SessionWeb.commit()

    return


def delete_web_source(code: str = None, title: str = None) -> None:
    WebSource = get_web_source(code, title)

    if WebSource is not None:
        SessionWeb.delete(WebSource)
        SessionWeb.commit()
        return

def get_web_sources(title: str = None, code = None, price = None, type = None) -> list:
    WebSources = _get_sources(title, code, price, type)
    return list(SessionWeb.scalars(WebSources))


def get_web_source(code: str = None, title: str = None) -> WebSource:
    """

    Получение объекта источника по его уникальному коду

    """

    WebSource = _get_source(code, title)
    if WebSource is not None:
        return SessionWeb.execute(WebSource).scalar()


def _get_source(code: str, title: str):
    if code is not None:
        return select(WebSource).where(WebSource.code == code)

    return select(WebSource).where(WebSource.title == title)


def _get_sources(title, code, price, type) -> list:
    WebSources = select(WebSource)

    if title is not None:
        WebSources = WebSources.where(WebSource.title.contains(title))

    if code is not None:
        WebSources = WebSources.where(WebSource.code.contains(code))

    if type is not None:
        WebSources = WebSources.where(WebSource.type.contains(type))

    return WebSources
# def update_price_list(code,type:str,delta_profit:int=0):
#     """
#     types:
#     new_person(who start registration)
#     new_ended_reg(who end registration)
#     new_customer(who paid first time)
#     new_payment(payment with WebSource)
    
#     """
    
#     SessionWeb=SessionWebmaker(engine)()
#     WebSource=SessionWeb.query(WebSource).filter_by(code=code).first()
#     kwarks={}


#     if type=="new_person":
#         new_amount_of_persons=WebSource.amount_of_persons+1
#         kwarks["amount_of_persons"]=new_amount_of_persons


#     elif type=="new_ended_reg":
#         new_amount_of_ended_registr=WebSource.amount_of_persons_who_ended_registr+1
#         kwarks["amount_of_persons_who_ended_registr"]=new_amount_of_ended_registr


#     elif type=="new_payment":
#         if WebSource.payment_exists==False:#Если платежа не существует , то у нас и так по умолчанию стоит 1. ничего не меняем
#             kwarks["payment_exists"]=True
#             kwarks["profit"]=new_profit

#         else:
#             new_amount_of_payment=WebSource.amount_of_persons_who_ended_registr+1
#             new_profit=WebSource.profit+delta_profit
#             kwarks["amount_of_payments"]=new_amount_of_payment
#             kwarks["profit"]=new_profit
        

#     elif type=="new_customer":#Если подписчика не существует , то у нас и так по умолчанию стоит 1. ничего не меняем

#         if WebSource.customer_exists==False:
#             kwarks["customer_exists"]=True
#             kwarks["payment_exists"]=True
#         else:

#             new_amount_of_payment=WebSource.amount_of_persons_who_ended_registr+1#Если у нас появился подписчик, то автоматом появился и платеж, что не всегда верно в обратную строну,
#                                                                             #  поэтому добавляем платеж в бд автоматически
#             new_amount_of_customers=WebSource.amount_of_customers+1
#             kwarks["amount_of_payments"]=new_amount_of_payment
#             new_profit=WebSource.profit+delta_profit

#             kwarks["profit"]=new_profit

#             kwarks["amount_of_customers"]=new_amount_of_customers

#     SessionWeb.query(WebSource).filter_by(code=code).update(kwarks)

#     SessionWeb.commit()

payment_types = ['FIRST PAY', 'SELF PAID', 'REC']

def get_success_web_payments(
    telegram_id = None,
    source_id = None,
    payment_type = None,
    rec_available = None, # возможнен ли рекуррент
    ) -> list:

    session = SessionWeb
    payments = select(WebSuccessPayment)

    if telegram_id is not None:
        payments = payments.where(WebSuccessPayment.telegram_id.contains(telegram_id))

    if source_id is not None:
        payments = payments.where(WebSuccessPayment.source_id.contains(source_id))

    if payment_type is not None and payment_type != 3:
        type_ = payment_types[payment_type]

        payments = payments.where(WebSuccessPayment.type_of_payment == type_)

    return list(SessionWeb.scalars(payments))

# WebSuccessPayment.__table__.drop(engine)
# Base.metadata.create_all(engine)


BaseWeb.metadata.create_all(engine_web)
