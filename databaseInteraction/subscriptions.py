# from datetime import datetime
# from sqlalchemy import *
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# from posixpath import abspath
# from os.path import join

# Base = declarative_base()

# LINK ='sqlite:///' + abspath(join('.', 'horoscope.db'))

# engine = create_engine(LINK)

# DATE_FORMAT = '%d.%m.%Y'
# TIME_FORMAT = '%H:%M'

# class Subscription(Base):
#     """
    
#     Модель подписки в базе данных

#     ID : int
#     TelgramID : int - id обладателя подписки
#     Type : int - тип подписки
#     Start : str - дата начала подписки
#     End : str - дата конца подписки
#     PayID : str - id платежа по yookasa

#     """

#     __tablename__ = 'Subscriptions'

#     ID = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
#     TelegramID = Column(Integer, nullable=False)
#     Type = Column(String, nullable=False)
#     Start = Column(String, nullable=False)
#     End = Column(Integer, nullable=False)
#     PayID = Column(String, nullable=False)

# # --------------------- PRIVATE METHODS ---------------------

# def _calculate_days(end) -> int:
#     """
    
#     Вычисляет, сколько полных дней между сегодня и введенной датой
#     Если введенная дата перед сегодня, то возвращается 0

#     """

#     now = datetime.strptime(datetime.strftime(datetime.now(), DATE_FORMAT), DATE_FORMAT)
#     end = datetime.strptime(end, DATE_FORMAT)

#     now_timestamp = now.timestamp()
#     end_timestamp = end.timestamp()

#     between = end_timestamp - now_timestamp

#     if between < 0:
#         return 0

#     return datetime.fromtimestamp(between).day

# def _get_subs_by_day(day : int) -> "list[Subscription]":
#     """
    
#     Возвращает подписки, у которых осталось введенное количество дней до истечения

#     """

#     _session = sessionmaker(engine)()

#     subs = _get_subs()
#     subs = _session.scalars(subs) 

#     result = list()

#     for sub in subs:
#         if _calculate_days(sub.End) == day:
#             result.append(sub)

#     return result

# def _drop_table():
#     Subscription.__table__.drop(engine)

# def delete_sub(id : str):
#     _session = sessionmaker(engine)()    

#     _session.delete(_session.execute(_get_sub(id)).scalar())
#     _session.commit()

# def _get_sub(id : int):
#     return select(Subscription).where(Subscription.TelegramID == id)

# def _get_subs(
#     type : str = None
#     ):

#     subs = select(Subscription)

#     if type:
#         subs = subs.where(Subscription.Type == type)

#     return subs

# # --------------------- PUBLIC METHODS ----------------------

# def add_sub(
#     id : int = '',
#     type : int = 3,
#     start : str = '',
#     end : str = '',
#     pay_id : str = '') -> Subscription:

#     """
    
#     Добавление новой подписки в базу данных

#     формат даты : DATE_FORMAT

#     """

#     _session = sessionmaker(engine)()

#     if start:
#         start = datetime.strptime(start, DATE_FORMAT)
#         start = datetime.strftime(start, DATE_FORMAT)

#     if end:
#         end = datetime.strptime(end, DATE_FORMAT)
#         end = datetime.strftime(end, DATE_FORMAT)
    
#     subscription = Subscription(
#                                 TelegramID=id,
#                                 Type=type,
#                                 Start=start,
#                                 End=end,
#                                 PayID=pay_id)
                                
#     _session.add(subscription)
#     _session.commit()

#     return subscription

# def get_subs_by_day(*days) -> "dict[int, list]":
#     """

#     Получение пользователей

#     :args:

#     *days : list - дни до конца подписки

#     :return: dict[day, list[Subscription(...)]]

#     Словарь, где ключ - количество дней до конца подписки (один из *days),
#              а значение - список подписок, у которых столько дней осталось до конца

#     """

#     result = dict()

#     for day in days:
#         subs = _get_subs_by_day(day)
#         result[day] = subs

#     return result

# def get_subs(
#     type : str = None
#     ) -> "list[Subscription]":
    
#     _session = sessionmaker(engine)()

#     return list(_session.scalars(_get_subs(type)))

# def get_sub( _session,id : int) -> Subscription:
#     sub =_get_sub(id)
#     _session = sessionmaker(engine)()
#     sub1=_session.execute(sub).scalar()
#     _session.commit()
#     return sub1

# def set_field(
#     id : int, 
#     new_id : int = None,
#     type : str = None, 
#     end : str = None,
#     pay_id : str = None) -> None:

#     _session = sessionmaker(engine)()
#     subscription = get_sub(_session, id)
#     _session.commit()

#     if new_id:
#         setattr(subscription, "TelegramID", new_id)

#     if type:
#         setattr(subscription, "Type", type)

#     if end!=None:
#         setattr(subscription, "End", end)

#     if pay_id:
#         setattr(subscription, "PayID", pay_id)

#     _session.commit()

#     return
    
# Base.metadata.create_all(engine)
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from posixpath import abspath
from os.path import join

Base = declarative_base()

LINK ='sqlite:///' + abspath(join('.', 'horoscope.db'))

engine = create_engine(LINK)

DATE_FORMAT = '%d.%m.%Y'
TIME_FORMAT = '%H:%M'

class Subscription(Base):
    """
    
    Модель подписки в базе данных
    ID : int
    TelgramID : int - id обладателя подписки
    Type : int - тип подписки
    Start : str - дата начала подписки
    End : str - дата конца подписки
    PayID : str - id платежа по yookasa
    """

    __tablename__ = 'Subscriptions'

    ID = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    TelegramID = Column(Integer, nullable=False)
    Type = Column(String, nullable=False)
    Start = Column(String, nullable=False)
    End = Column(Integer, nullable=False)
    PayID = Column(String, nullable=False)

# --------------------- PRIVATE METHODS ---------------------

def _calculate_days(end) -> int:
    """
    
    Вычисляет, сколько полных дней между сегодня и введенной датой
    Если введенная дата перед сегодня, то возвращается 0
    """

    now = datetime.strptime(datetime.strftime(datetime.now(), DATE_FORMAT), DATE_FORMAT)
    end = datetime.strptime(end, DATE_FORMAT)

    now_timestamp = now.timestamp()
    end_timestamp = end.timestamp()

    between = end_timestamp - now_timestamp

    if between < 0:
        return 0

    return datetime.fromtimestamp(between).day

def _get_subs_by_day(day : int) -> "list[Subscription]":
    """
    
    Возвращает подписки, у которых осталось введенное количество дней до истечения
    """

    _session = sessionmaker(engine)()

    subs = _get_subs()
    subs = _session.scalars(subs) 

    result = list()

    for sub in subs:
        if _calculate_days(sub.End) == day:
            result.append(sub)

    return result

def _drop_table():
    Subscription.__table__.drop(engine)

def delete_sub(id : str):
    _session = sessionmaker(engine)()    

    _session.delete(_session.execute(_get_sub(id)).scalar())
    _session.commit()

def _get_sub(id : int):
    return select(Subscription).where(Subscription.TelegramID == id)

def _get_subs(
    type : str = None
    ):

    subs = select(Subscription)

    if type:
        subs = subs.where(Subscription.Type == type)

    return subs

# --------------------- PUBLIC METHODS ----------------------

def add_sub(
    id : int = '',
    type : int = 3,
    start : str = '',
    end : str = '',
    pay_id : str = '') -> Subscription:

    """
    
    Добавление новой подписки в базу данных
    формат даты : DATE_FORMAT
    """

    _session = sessionmaker(engine)()

    if start:
        start = datetime.strptime(start, DATE_FORMAT)
        start = datetime.strftime(start, DATE_FORMAT)

    if end:
        end = datetime.strptime(end, DATE_FORMAT)
        end = datetime.strftime(end, DATE_FORMAT)
    
    subscription = Subscription(
                                TelegramID=id,
                                Type=type,
                                Start=start,
                                End=end,
                                PayID=pay_id)
                                
    _session.add(subscription)
    _session.commit()

    return subscription

def get_subs_by_day(*days) -> "dict[int, list]":
    """
    Получение пользователей
    :args:
    *days : list - дни до конца подписки
    :return: dict[day, list[Subscription(...)]]
    Словарь, где ключ - количество дней до конца подписки (один из *days),
             а значение - список подписок, у которых столько дней осталось до конца
    """

    result = dict()

    for day in days:
        subs = _get_subs_by_day(day)
        result[day] = subs

    return result

def get_subs(
    type : str = None
    ) -> "list[Subscription]":
    
    _session = sessionmaker(engine)()

    return list(_session.scalars(_get_subs(type)))

def get_sub( id : int) -> Subscription:
    sub =_get_sub(id)
    _session = sessionmaker(engine)()
    return _session.execute(sub).scalar()

def set_field(
    id : int, 
    new_id : int = None,
    type : str = None, 
    end : str = None,
    pay_id : str = None) -> None:

    _session = sessionmaker(engine)()
    subscription = get_sub(_session, id)

    if new_id:
        setattr(subscription, "TelegramID", new_id)

    if type:
        setattr(subscription, "Type", type)

    if end:
        setattr(subscription, "End", end)

    if pay_id:
        setattr(subscription, "PayID", pay_id)

    _session.commit()

    return
    
Base.metadata.create_all(engine)