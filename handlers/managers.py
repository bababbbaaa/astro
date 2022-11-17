from controller import dp, bot
from datetime import datetime as date_time
from databaseInteraction import *
from aiogram.types import *
from utils import *
from datetime import date
import config
from calendar import Calendar

months = ['Январь', "Февраль", "Март", "Апрель", "Май", "Июнь",
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]


# @show_log_
# async def calendar_handler(message, date: str, post: bool):
#     if date is None:
#         return

#     if post:
#         render_posts(message, date, False)
#         return

#     create_post_(message, date)

@show_log_
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
@show_log_
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
            # button.onClick(calendar_handler, formatted_date, '(' in number)

            markup_row_.append(button)

        markup_row(markup, markup_row_)

    await bot.send_message(
        author, f"Выбранная дата: *{months[today.month - 1]}* *{today.year}* Года", reply_markup=markup, parse_mode="Markdown")
