from sqlalchemy import *
from controller import engine, Base, Session
from datetime import datetime as date_time
from utils import *
from sqlalchemy import DDL,event

DATE_FORMAT = '%d.%m.%Y'


def basic_check_date(date_string : str):
    try:
        date = date_time.strptime(date_string, DATE_FORMAT)
        return True
    except:
        return False

class Source(Base):
    """

    Модель источника прихода пользователя в бд

    ID : int
    title : str
    code : string
    price : int
    date:date
    type:str
    profit:int
    price_for_person:int
    price_for_customers:int
    amount_of_persons:int
    amount_of_customers:int
    amount_of_persons_who_ended_registr:int
    amount_of_payments:int
    price_for_ended_reg:int
    """

    __tablename__ = "Sources"

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
    
def add_person_to_source(source_id):
    session=Session()
    source=session.query(Source).filter_by(code=source_id).first()
    source.amount_of_person



def drop_table():
    Source.__table__.drop(engine)


def add_source(
        title: str,
        code: str,
        price: int,
        date : str,
        type : str) -> Source:
    """
    У нас стоят триггеры на автоматический подсчет цены за человека,прищедего в бот,
    поэтому не меняй на 0 ни один из стобцов бд,который начинается на amount, иначе получищь +100500 ошибок 
    """
    if not basic_check_date(date):
        raise Exception("Invalid date")

    source = Source(
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

    Session.add(source)
    Session.commit()

    return source


def update_source(code, new_title: str = None, new_price : int = None) -> None:
    """

    Меняет название источника

    """
    source = get_source(code)
    
    if new_title is not None:
        setattr(source, "title", new_title)

    if new_price is not None:
        setattr(source, "price", new_price)
        
    Session.commit()

    return


def delete_source(code: str = None, title: str = None) -> None:
    source = get_source(code, title)

    if source is not None:
        Session.delete(source)
        Session.commit()
        return

def get_sources(title: str = None, code = None, price = None, type = None) -> list:
    sources = _get_sources(title, code, price, type)
    return list(Session.scalars(sources))


def get_source(code: str = None, title: str = None) -> Source:
    """

    Получение объекта источника по его уникальному коду

    """

    source = _get_source(code, title)
    if source is not None:
        return Session.execute(source).scalar()


def _get_source(code: str, title: str):
    if code is not None:
        print(code)
        return select(Source).where(Source.code == code)

    return select(Source).where(Source.title == title)


def _get_sources(title, code, price, type) -> list:
    sources = select(Source)

    if title is not None:
        sources = sources.where(Source.title.contains(title))

    if code is not None:
        sources = sources.where(Source.code.contains(code))

    if type is not None:
        sources = sources.where(Source.type.contains(type))

    return sources
def update_price_list(code,type:str,delta_profit:int=0):
    """
    types:
    new_person(who start registration)
    new_ended_reg(who end registration)
    new_customer(who paid first time)
    new_payment(payment with source)
    
    """
    
    session=sessionmaker(engine)()
    source=session.query(Source).filter_by(code=code).first()
    kwarks={}


    if type=="new_person":
        new_amount_of_persons=source.amount_of_persons+1
        kwarks["amount_of_persons"]=new_amount_of_persons


    elif type=="new_ended_reg":
        new_amount_of_ended_registr=source.amount_of_persons_who_ended_registr+1
        kwarks["amount_of_persons_who_ended_registr"]=new_amount_of_ended_registr


    elif type=="new_payment":
        if source.payment_exists==False:#Если платежа не существует , то у нас и так по умолчанию стоит 1. ничего не меняем
            kwarks["payment_exists"]=True
            kwarks["profit"]=new_profit

        else:
            new_amount_of_payment=source.amount_of_persons_who_ended_registr+1
            new_profit=source.profit+delta_profit
            kwarks["amount_of_payments"]=new_amount_of_payment
            kwarks["profit"]=new_profit
        

    elif type=="new_customer":#Если подписчика не существует , то у нас и так по умолчанию стоит 1. ничего не меняем

        if source.customer_exists==False:
            kwarks["customer_exists"]=True
            kwarks["payment_exists"]=True
        else:

            new_amount_of_payment=source.amount_of_persons_who_ended_registr+1#Если у нас появился подписчик, то автоматом появился и платеж, что не всегда верно в обратную строну,
                                                                            #  поэтому добавляем платеж в бд автоматически
            new_amount_of_customers=source.amount_of_customers+1
            kwarks["amount_of_payments"]=new_amount_of_payment
            new_profit=source.profit+delta_profit

            kwarks["profit"]=new_profit

            kwarks["amount_of_customers"]=new_amount_of_customers

    session.query(Source).filter_by(code=code).update(kwarks)

    session.commit()


def update_price_list_with_id(id,type,delta_price):
    session=Session()
    user=session.query(User).filter_by(TelegramID=str(id)).first()
    source_id=user.Source_ID
    return update_price_list(source_id,type,delta_price)
# Source.__table__.drop(engine)

Base.metadata.create_all(engine)
