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
    



class SuccessPayments(Base):
    __tablename__="success_payments"

    ID = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    sub_type = Column(Integer, nullable=False)
    telegram_id = Column(String, nullable=False)
    payment_id = Column(String, nullable=False)
    active_until = Column(String, nullable=False)
    days = Column(Integer, nullable=False)
    payed = Column(Boolean, nullable=False)
    amount = Column(Integer, nullable=False)
    link = Column(String, nullable=False)
    source_id=Column(BIGINT)



    def get_user(self):
        session=sessionmaker(engine)()
        user=session.query(User).filter_by(TelegramID=self.telegram_id)
        return user