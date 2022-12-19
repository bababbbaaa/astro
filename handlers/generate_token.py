import functions
from asyncio import *
from controller import *
from utils import *
import config
from aiogram.dispatcher.filters.state import State, StatesGroup

import functions

class Token(StatesGroup):
    name=State()
    token=State()

@dp.message_handler(commands=['gen_token'])
async def generate_token(message):
    id = message.chat.id

    if id not in config.managers:
        await wait_until_send(id, "Вы не менджер, в доступе отказано")
        return
    else:
        await wait_until_send(
            id, "Введите название паблика,чтобы сгенирировать токен")
    await Token.name.set()
@dp.message_handler(state=Token.name)
async def enter_token_name(message: CallbackQuery, state: FSMContext):
    id = message.chat.id
    public_name = message.text
    # InsertIntoTable("AstroSchool",(("Category","334234423"),("MessageID",555)),)
    token = random.randint(100000000, 999999999)
    date=datetime.now().date()
    date=datetime.strftime(date,"%d.%m.%Y")
    add_source(title=public_name,code=token,price=0,date=date,
    type="канал")
    add_web_source(title=public_name,code=token,price=0,date=date,
    type="канал")
    await wait_until_send(id, "Паблик записан, вот ссылка для "+public_name +
                    " https://t.me/"+config.bot_name[1:]+"?start="+str(token)+"\n\nавтоматически тип источника записался как канал, если необходимо, заменить в вэбе инфу")
    await state.finish()