from re import A
from controller import dp, bot
from datetime import datetime as date_time
from datetime import timedelta
from databaseInteraction import *
from aiogram.types import *
from utils import *
from datetime import date
from calendar import Calendar
from asyncio import *
from traceback import format_exc
from os import path
import config

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext


class NewPost(StatesGroup):
    is_heading = State()
    date = State()
    time = State()
    content = State()
    buttons = State()
    file = State()


months = ['Январь', "Февраль", "Март", "Апрель", "Май", "Июнь",
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]


@dp.callback_query_handler(lambda call: call.data.split(";")[0] == "POST_MENU" and call.data.split(';')[1] == 'CREATE')
async def create_post_(call, date: str = None, delete_message: bool = False) -> None:
    """ Создание постов, позже отправляющихся в различные каналы по определенному графику """
    id = call.from_user.id

    if delete_message:
        bot.delete_message(id, call.message.message_id)

    # Вопрос : Это рубрика?
    handler = 'IS_HEADING'
    markup = types.InlineKeyboardMarkup()

    yes = types.InlineKeyboardButton(
        "Да", callback_data=f'{handler};YES;{date}')
    no = types.InlineKeyboardButton(
        "Нет", callback_data=f'{handler};NO;{date}')

    back = InlineButton(text="<-- Назад")
    cancel = InlineButton(text="Отмена")

    if date:
        back.onClick(render_posts, date)
    else:
        back.onClick(_manager_access)

    cancel.onClick(cancel_manager)

    markup.row(yes, no)
    markup.row(back, cancel)

    await bot.send_message(id, "Пост является рубрикой?", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data.split(";")[0] == "IS_HEADING")
async def handle_first(call: CallbackQuery, state: FSMContext):
    """ Обработчик выбора (Это Рубрика?)"""
    author = call.from_user.id
    data = call.data.split(";")[1]
    date = call.data.split(';')[2]

    await NewPost.is_heading.set()
    async with state.proxy() as state_data:
        state_data['is_heading'] = True if data == 'YES' else False

    if data == 'YES':
        await bot.send_message(author, "Пост является рубрикой : записано")

        # время не спрашивается
        await NewPost.date.set()
        await bot.send_message(author, "Напишите дату отправку сообщения в формате день.месяц.год")

    if data == 'NO':
        await bot.send_message(author, "Пост не является рубрикой : записано")

        # время спрашивается
        await ask_time(call, state)


async def ask_time(message: CallbackQuery, state: FSMContext):
    author = message.from_user.id

    await NewPost.time.set()
    await bot.send_message(author, "Напишите время отправки сообщения в формате: часы:минуты")


@dp.message_handler(state=NewPost.time)
async def ask_date(message: CallbackQuery, state: FSMContext, manually=False):
    author = message.from_user.id

    if not check_time(message.text) and not manually:
        await bot.send_message(author, "Некорректный формат записи времени, попробуйте снова")
        await ask_time(message, state)
        return

    async with state.proxy() as state_data:
        if not manually:
            # если функция была вызвана не из-за записи некорретной даты в предыдущем вопросе
            state_data['time'] = message.text

    await NewPost.date.set()
    await bot.send_message(author, "Напишите дату отправку сообщения в формате день.месяц.год")


@dp.message_handler(state=NewPost.date)
async def ask_content(message: CallbackQuery, state: FSMContext):
    author = message.from_user.id

    check = check_date(message.text)
    if not check:
        await bot.send_message(author, "Некорректная дата, попробуйте снова")
        await ask_date(message, state, True)

        return

    async with state.proxy() as state_data:
        state_data['date'] = message.text

    await NewPost.content.set()
    await bot.send_message(author, "Введите содержимое поста, которое нужно будет отправить")


@dp.message_handler(state=NewPost.content)
async def ask_buttons(message: CallbackQuery, state: FSMContext):
    author = message.from_user.id

    async with state.proxy() as state_data:
        state_data['content'] = message

    await NewPost.buttons.set()
    await bot.send_message(author, "Хотите добавить кнопки в пост?\nЕсли *да*, то опишите кнопки в формате\n ``` Кнопка 1 - ссылка\n Кнопка 2 - ссылка```\n\nЕсли *нет*, напишите 'нет'", parse_mode="Markdown")


@dp.message_handler(state=NewPost.buttons)
async def ask_file(message: CallbackQuery, state: FSMContext):
    author = message.from_user.id

    async with state.proxy() as state_data:
        if state_data.get('buttons'):
            await send_post(message, state)

            return

        state_data['buttons'] = message.text

    await bot.send_message(author, "Либо отправьте файл в формате txt, либо напишите любой текст, чтобы не использовать файл")


@dp.message_handler(content_types=[ContentType.DOCUMENT], state='*')
async def get_files(message: CallbackQuery, state: FSMContext):
    await NewPost.file.set()
    async with state.proxy() as state_data:
        check = await check_file_state(state_data)

        if not check:
            return

        await send_post(message, state)


async def send_post(message: CallbackQuery, state: FSMContext):
    author = message.from_user.id

    async with state.proxy() as state_data:
        is_heading = state_data['is_heading']
        date = state_data['date']
        time = state_data.get('time')
        post = state_data['content']
        buttons = state_data['buttons']

        file = message
        if message.text is not None:
            file = None

    await state.finish()

    if file is not None:
        file_info = await bot.get_file(file.document.file_id)
        download = await bot.download_file(file_info.file_path)
        today = get_today()

        name = f'{today}_{generate_token(9)}.txt'
        file_path = path.join('post_files', name)

        with open(file_path, "wb") as write_stream:
            download.seek(0)

            write_stream.write(download.read())

    buttons = parse_buttons(buttons)
    markup = make_markup_by_list(buttons, post.message_id)

    if time is not None:
        time = date_time.strptime(time, TIME_FORMAT)
    else:
        time = datetime.now()

    date = date_time.strptime(date, DATE_FORMAT)

    try:
        content = str()

        content += '*Мета данные*:\n'
        content += f'*Рубрика* {"Да" if is_heading else "Нет"}\n'
        content += f'*Дата*: {date.year} год, {months[date.month - 1]}, {date.day}-е число\n'
        content += f'*Время*: {time.hour} *часов* {time.minute} *минут*\n'
        content += '*Вызвать* календарь: /calendar'

        db_time = f'{time.hour}:{time.minute}'
        db_date = f'{date.day}.{date.month}.{date.year}'

        db_date = date_time.strptime(db_date, DATE_FORMAT)

        month = str(db_date.month)
        day = str(db_date.day)
        year = str(db_date.year)

        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day

        db_date = day + "." + month + "." + year

        db_message = post.message_id
        db_author = post.chat.id
        db_category = "person" if is_heading else "none"

        db_first_row = "only picture"

        if post.text:
            db_first_row = post.text[:25]

        if post.caption:
            db_first_row = post.caption[:25]

        await bot.send_message(author, content, parse_mode='Markdown')
        await bot.copy_message(author, author, post.message_id, reply_markup=markup)

        database = create_session()
        add_post(
            database,
            category=db_category,
            managerId=db_author,
            postId=db_message,
            date=db_date,
            time=db_time,
            first_row=db_first_row,
            path=file_path)
    except Exception as e:
        print(format_exc(e))
        await bot.send_message(author, f'```{e}```', parse_mode="Markdown")


@dp.callback_query_handler(lambda call: call.data.split(';')[0] == 'POST_MENU' and call.data.split(';')[1] == 'POSTS')
async def choose_post(message):
    author = message.from_user.id
    await bot.delete_message(author, message.message.message_id)

    markup = types.InlineKeyboardMarkup()
    dates = set()

    posts_in_date = dict()

    for post in get_posts(create_session()):
        date = post.Date

        if date not in posts_in_date:
            posts_in_date[date] = int()

        posts_in_date[date] += 1

        dates.add(date)

    for date in dates:
        button = InlineButton(text=f"{date} ({posts_in_date[date]} поста)")
        button.onClick(render_posts, date=date)

        markup.add(button)

    await wait_until_send(
        author, "Выберите дату, на которую был запланирован пост", reply_markup=markup)


@dp.message_handler(commands=["manager_access"])
async def _manager_access(message) -> None:
    try:
        author = message.chat.id
    except:
        author = message.from_user.id

    try:
        await bot.delete_message(message.from_user.id, message.message.message_id)
    except:
        pass

    if author not in config.managers:
        await wait_until_send(author, "Вы не менджер, в доступе отказано")
        return

    handler = 'POST_MENU'
    markup = types.InlineKeyboardMarkup()

    create = types.InlineKeyboardButton(
        "Создать", callback_data=f"{handler};CREATE")
    choice = types.InlineKeyboardButton(
        "К постам", callback_data=f"{handler};POSTS")
    cancel = InlineButton(text="Отмена")

    cancel.onClick(cancel_manager)

    markup.row(cancel, create)
    markup.add(choice)

    await wait_until_send(author, "*МЕНЮ*",
                          parse_mode="Markdown", reply_markup=markup)


async def show_post(call, post_id):
    author = call.from_user.id
    buttons = get_buttons(create_session(), post_id)
    markup = make_markup(buttons)

    await wait_until_copy(author, author, post_id, reply_markup=markup)


async def _show_post_(message, post_id):
    await show_post(message, post_id)
    await bot.delete_message(message.from_user.id, message.message.message_id)

    author = message.from_user.id
    markup = types.InlineKeyboardMarkup()

    edit = InlineButton(text="Изменить")
    delete = InlineButton(text="Удалить")
    cancel = InlineButton(text="Отмена")
    back = InlineButton(text="<-- Назад")

    # edit.onClick(choose_post, post_id)
    # delete.onClick(_delete_post, post_id)
    cancel.onClick(cancel_manager)

    markup.row(back, cancel)
    markup.row(edit, delete)

    await bot.send_message(author, "Выберите действиe:", reply_markup=markup)


async def cancel_manager(message):
    await bot.delete_message(message.from_user.id, message.message.message_id)

    await bot.send_message(
        message.from_user.id, "*Вызвать* календарь: /calendar", parse_mode="Markdown")


async def render_posts(call: Message | CallbackQuery, date, delete_message: bool = True):
    author = call.from_user.id

    if delete_message:
        await bot.delete_message(author, call.message.message_id)

    database = create_session()
    posts = get_posts(database, date=date)

    markup = types.InlineKeyboardMarkup()
    back_handler = 'POST_MENU'

    back = types.InlineKeyboardButton(
        text="<- Назад", callback_data=f'{back_handler};BACK')
    cancel = InlineButton(text="Отмена")
    create = InlineButton(text="Создать")

    cancel.onClick(cancel_manager)
    # create.onClick(create_post_, date, True)

    markup.row(back, cancel)
    markup.add(create)

    for post in posts:
        category = post.Time if post.Category != 'person' else "Рубрика"
        category += f" ({post.FirstRow}...)"

        button = InlineButton(text=category)
        button.onClick(_show_post_, post.PostID)

        markup.add(button)

    await bot.send_message(author, date, reply_markup=markup)


async def calendar_handler(message, date: str, post: bool):
    if date is None:
        return

    if post:
        render_posts(message, date, False)
        return

    await create_post_(message, date)


async def turn_calendar_page(message: CallbackQuery, current_date, months: int):
    step_month = current_date.month + months
    step_year = current_date.year

    if step_month == 13:
        step_month = 1
        step_year += 1

    if step_month == 0:
        step_month = 12
        step_year -= 1

    current_month = days_in_month(step_month, step_year)

    if months == -1:
        current_month = -current_month

    new_date = current_date + timedelta(days=current_month)

    await show_calendar(message, new_date)
    await bot.delete_message(message.from_user.id, message.message.message_id)


@dp.message_handler(commands=['calendar'])
async def show_calendar(message: Message, handled_date=None):
    try:
        author, chat, me = await general_info(message)
    except:
        author = message.from_user.id

    if author not in config.managers:
        await bot.send_message(author, "Вы не менеджер, в доступе отказано")
        return

    today = date.today()

    dates = dict()
    posts = get_posts(create_session())

    for post in posts:
        post_date = post.Date

        if dates.get(post_date) is None:
            dates[post_date] = 0

        dates[post_date] += 1

    if handled_date is not None:
        today = handled_date

    calendar = Calendar()
    weeks = calendar.monthdays2calendar(today.year, today.month)

    markup = InlineKeyboardMarkup(row_width=8)
    previous = InlineButton(text="<-----------")
    next = InlineButton(text="----------->")

    previous.onClick(turn_calendar_page, today, -1)
    next.onClick(turn_calendar_page, today, 1)

    markup.row(previous, next)

    monday_ = InlineButton(text="Пн")
    tuesday_ = InlineButton(text="Вт")
    wednesday_ = InlineButton(text="Ср")
    thursday_ = InlineButton(text="Чт")
    friday_ = InlineButton(text="Пт")
    saturday_ = InlineButton(text="Сб")
    sunday_ = InlineButton(text="Вс")

    markup.row(monday_, tuesday_, wednesday_,
               thursday_, friday_, saturday_, sunday_)

    for week in weeks:
        markup_row_ = list()
        for day in week:
            number = day[0]
            formatted_date = None
            if number:
                day_date = today.replace(day=number)
                formatted_date = date_time.strftime(
                    day_date, DATE_FORMAT)

                if formatted_date in dates:
                    number = f"{number} ({dates[formatted_date]})"

            number = str(number)
            button_width = 10

            button = InlineButton(text=number)
            button.width = button_width
            button.onClick(calendar_handler, formatted_date, '(' in number)

            markup_row_.append(button)

        markup_row(markup, markup_row_)

    await bot.send_message(
        author, f"Выбранная дата: *{months[today.month - 1]}* *{today.year}* Года", reply_markup=markup, parse_mode="Markdown")
