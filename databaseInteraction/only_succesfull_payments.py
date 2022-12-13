from datetime import datetime , timedelta
from itertools import tee
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from posixpath import abspath
from os.path import join
from controller import engine, Base, Session


DATE_FORMAT = '%d.%m.%Y'


class User(Base):
    


    __tablename__="Users"
    ID = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    Name=Column(Text)
    IS_Main=Column(Integer)
    Gender_ID=Column(Integer)
    BirthTime=Column(VARCHAR(10))
    Birthday=Column(VARCHAR(20))
    Birthplace=Column(VARCHAR(255))
    DesTime_ID=Column(Integer)
    TimeZone=Column(Integer)
    TelegramID=Column(Text)
    RegDate=Column(DATE)
    RegDateFin=Column(DATE)
    IsActiveBot=Column(Integer)
    Balance=Column(DECIMAL(15,2))
    IsActiveSub=Column(INTEGER)
    SubscrType_ID=Column(Integer)                                
    ActiveUntil=Column(DATE)    
    DateSend=Column(DATE)
    IntrvMessBeg=Column(Integer)                                
    IntrvMessEnd=Column(Integer)
    StdShutoff=Column(Integer)
    TryPayRem=Column(Integer)
    Source_ID=Column(Integer)
    



class SuccessPayment(Base):
    __tablename__="success_payments"

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


    def get_user(self):
        session=sessionmaker(engine)()
        user=session.query(User).filter_by(TelegramID=self.telegram_id)
        return user

def add_success_payment(**kwargs) -> None:
    telegram_id=str(kwargs["telegram_id"])
    payment_id=str(kwargs["payment_id"])
    days=int(kwargs["days"])
    amount=int(float(kwargs["price"]))
    type_of_payment=str(kwargs["type_of_payment"])

    payment_date=datetime.today()
    active_until=payment_date+timedelta(days=days)

    session=sessionmaker(engine)()
    user=session.query(User).filter_by(TelegramID=telegram_id).first()
    user_name=user.Name
    source_id=user.Source_ID
    payed=1
    if source_id==None or source_id=="":
        source_id=0
    birth_day=user.Birthday

    if birth_day=="" or birth_day==None:
        birth_day=datetime.strptime("00:00","%H:%M")

    else:
        birth_day=datetime.strptime(birth_day,"%d.%m.%Y")
    new_success_payment=SuccessPayment(
        telegram_id=telegram_id,
        payment_id=payment_id,
        days=days,
        amount=amount,
        payment_date=payment_date,
        active_until=active_until,
        user_name=user_name,
        source_id=source_id,
        payed=payed,
        type_of_payment=type_of_payment,
        birth_day=birth_day

    )

    session=sessionmaker(engine)()
    session.add(new_success_payment)
    session.commit()

    return new_success_payment

payment_types = ['FIRST PAY', 'SELF PAID', 'REC']

def get_success_payments(
    telegram_id = None,
    source_id = None,
    payment_type = None,
    rec_available = None, # возможнен ли рекуррент
    ) -> list:

    session = sessionmaker(engine)()
    payments = select(SuccessPayment)

    if telegram_id is not None:
        payments = payments.where(SuccessPayment.telegram_id.contains(telegram_id))

    if source_id is not None:
        payments = payments.where(SuccessPayment.source_id == source_id)

    if payment_type is not None and payment_type != 3:
        type_ = payment_types[payment_type]

        payments = payments.where(SuccessPayment.type_of_payment == type_)

    return list(session.scalars(payments))

# SuccessPayment.__table__.drop(engine)
Base.metadata.create_all(engine)
