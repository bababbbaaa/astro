from aiogram import *
import config
from databaseInteraction import *
import sqlalchemy
import os
from datetime import datetime,timedelta
bot=Bot(token=config.TOKEN,parse_mode="html")
dp=Dispatcher(bot=bot)
# user = 'root'
# password = '24070509'
# host = '127.0.0.1'
# port = 3306
# database = 'base'
# connection_string = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
#             user, password, host, port, database
#         ) if os.environ.get('CONNECTION_STRING') is None else os.environ.get('CONNECTION_STRING')
connection_string = 'sqlite:///' + abspath(join('../horoscope.db'))

# connection_string="base"
engine = create_engine(
        url=connection_string
        
    )
block_dict=[]
delete_cache={}
Base.metadata.create_all(engine)
photos={}
for i in config.photos:
    photos[i]=open(config.photos[i],"rb").read()
is_user_already_in_handler={}