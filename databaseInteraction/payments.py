from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from posixpath import abspath
from os.path import join

user = 'admin2'
password = "Sergey123"
host = '185.209.29.236'
port = 3306
database = 'horoscope'
connection_string = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database)
# connection_string = 'sqlite:///' + abspath(join('../horoscope.db'))

engine = create_engine(
    url=connection_string
)
Base = declarative_base()

DATE_FORMAT = '%d.%m.%Y'

class Payment(Base):
    """
    
    Модель платежа

    """

    __tablename__ = 'Payments'

    ID = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    sub_type = Column(Integer, nullable=False)
    telegram_id = Column(String, nullable=False)
    payment_id = Column(String, nullable=False)
    active_until = Column(String, nullable=False)
    days = Column(Integer, nullable=False)
    payed = Column(Boolean, nullable=False)
    amount = Column(Integer, nullable=False)
    link = Column(String, nullable=False)
    

def _get_payment(telegram_id : str):
    return select(Payment).where(Payment.telegram_id == telegram_id)

def get_payment(telegram_id : str) -> Payment:
    _session = sessionmaker(engine)()
    payment = _get_payment(telegram_id)

    payments= _session.scalars(payment)
    return list(payments)


def _get_payments():
    return select(Payment).where(Payment.payed==False)


def get_payments():
    _session = sessionmaker(engine)()
    payment = _get_payments()
    payments= _session.scalars(payment)
    return list(payments)



def add_payment(
    sub_type : int,
    telegram_id : str,
    payment_id : str,
    active_until : str,
    days : int,
    payed : bool,
    amount : int,
    link : str
) -> Payment:

    active_until = datetime.strptime(active_until, DATE_FORMAT)
    active_until = datetime.strftime(active_until, DATE_FORMAT)

    new_payment = Payment(
                    sub_type = sub_type,
                    telegram_id=telegram_id,
                    payment_id = payment_id,
                    active_until = active_until,
                    days = days,
                    payed = payed,
                    amount=amount,
                    link=link
    )

    _session = sessionmaker(engine)()

    _session.add(new_payment)
    _session.commit()

    return new_payment

def delete_payment(telegram_id : str) -> None:
    _session = sessionmaker(engine)()

    payment = _get_payment(telegram_id)

    _session.delete(_session.execute(payment).scalar())
    _session.commit()

    return

def update_payment(
    telegram_id,
    sub_type : int = None,
    link : str = None
) -> None:

    _session = sessionmaker(engine)()

    payment = get_payment(_session, telegram_id)

    if sub_type:
        setattr(payment, "sub_type", sub_type)

    if link is not None:
        setattr(payment, "link", link)

    _session.commit()

    return

def _drop_table():
    Payment.__table__.drop(engine)

Base.metadata.create_all(engine)
