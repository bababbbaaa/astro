from aiogram import *
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.orm import sessionmaker
import config
import logging

bot = Bot(token=config.TOKEN, parse_mode="html")
dp = Dispatcher(bot=bot, storage=MemoryStorage())

user = 'admin2'
password = "Sergey123"
host = '185.209.29.236'
port = 3306
database = 'horoscope'
connection_string = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
    user, password, host, port, database)

Base = declarative_base()

###### LOGGING ######
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='app.log', filemode='a', format=LOG_FORMAT)
logger = logging.getLogger()


engine = create_engine(
    url=connection_string,pool_size=100,max_overflow=10
)

Session = sessionmaker(engine)()

block_dict = list()
delete_cache = dict()

Base.metadata.create_all(engine)
photos = {}

BaseWeb=declarative_base()
database="WEB"

connection_string = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
    user, password, host, port, database)

engine_web = create_engine(
    url=connection_string,pool_size=100,max_overflow=10
)

SessionWeb = sessionmaker(engine_web)()

BaseWeb.metadata.create_all(engine_web)
for i in config.photos:
    photos[i] = open(config.photos[i], "rb").read()

is_user_already_in_handler = dict()