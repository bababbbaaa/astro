
from controller import *
from asyncio import *
import commands

from utils import *
from aiogram import *

# activate handlers
import handlers

if __name__ == "__main__":
    print(f'START {datetime.now()}')
    executor.start_polling(dp,skip_updates=True, on_startup=startup)   