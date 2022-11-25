import requests
from datetime import datetime as date_time

DATE_FORMAT = '%d.%m.%Y'
TIME_FORMAT = '%H:%M'

def check_url(url: str) -> bool:
    try:
        requests.get(url)
    except:
        return False

    return True


def basic_check_date(date_string : str):
    try:
        date = date_time.strptime(date_string, DATE_FORMAT)
        return True
    except:
        return False

def check_date(date_string: str) -> bool:
    try:
        date = date_time.strptime(date_string, DATE_FORMAT)
        current = date_time.now()

        date = date.replace(hour=current.hour,
                            minute=current.minute, second=current.second)

        if date.timestamp() < current.timestamp():
            return False

    except:
        return False

    return True


def check_time(time_string: str) -> bool:
    try:
        time = date_time.strptime(time_string, TIME_FORMAT)
    except:
        return False

    return True


async def check_file_state(state_data):
    keys = ['is_heading', 'date', 'content', 'buttons']

    # если менеджер все предыдущие пункты создания поста
    for key in keys:
        if key not in state_data:
            return False

    # если пост не рубрика и при этом время не заполнено
    if not state_data['is_heading'] and 'time' not in state_data:
        return False

    return True
