from aiogram import *
import config
from databaseInteraction import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=config.TOKEN, parse_mode="html")
dp = Dispatcher(bot=bot, storage=MemoryStorage())
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

block_dict = list()
delete_cache = dict()

Base.metadata.create_all(engine)
photos = {}

for i in config.photos:
    photos[i] = open(config.photos[i], "rb").read()

is_user_already_in_handler = dict()
