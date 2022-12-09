from aiogram import *
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.orm import sessionmaker
import config

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


engine = create_engine(
    url=connection_string,pool_size=30,max_overflow=5
)

Session = sessionmaker(engine)()

block_dict = list()
delete_cache = dict()

Base.metadata.create_all(engine)
photos = {}

for i in config.photos:
    photos[i] = open(config.photos[i], "rb").read()

is_user_already_in_handler = dict()