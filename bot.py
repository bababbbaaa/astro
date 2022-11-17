
from mics import *
from asyncio import *

from utils import *
from handlers.registration import *
from handlers.sub_handlers import *
import random
user = {}
from aiogram import *


if __name__ == "__main__":
    print(f'START {datetime.now()}')
    executor.start_polling(dp,skip_updates=True)
    