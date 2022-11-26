from time import sleep
from rich import print as pretty_print
from rich.table import Table
from rich.live import Live
from traceback import format_exc
from os import path
import json, os

sessions = os.listdir('sessions')
threads = list()

def clear():
    os.system("cls")

def parse_json(file_name):
    data = open(path.join('static', f'{file_name}.json'),
                'r', encoding='utf-8').read()
    return json.loads(data)

def update_states(status: str, last_message: str, worker):
    """"

    Заполняет states.json, чтобы потом можно было смотреть в мониторе, 
    как аккаунты работают

    """

    states = parse_json('states')
    states[worker] = (status, last_message)

    json.dump(
        states,
        open(path.join('static', 'states.json'), 'w', encoding='utf-8'),
        indent=4,
        sort_keys=True,
        ensure_ascii=False
    )


def generate_monitor():
    table = Table(title="Auth Test 66.26.11", width=100)

    table.add_column("Account", justify="left", style="green", no_wrap=True)
    table.add_column("Status", style="green", justify="center")
    table.add_column("Message", justify="right", style="blue")

    states = parse_json('states')

    for nickname in states:
        status, message = states[nickname]
        table.add_row(nickname, status, message)

    return table

accounts = set()

for session in sessions:
    nickname = session.split('.')[0]
    accounts.add(nickname)

for account in accounts:
    update_states("[red]STOPPED", "NONE", account)

clear()

with Live(generate_monitor(), refresh_per_second=5) as live:
    while True:
        try:
            sleep(.5)

            live.update(generate_monitor())
        except KeyboardInterrupt:
            pretty_print("[green]Successfully exited. Monitor stopped.")
            
            update_states("[red]EXITED", "NONE")
            sleep(10)

            exit()

        except Exception as e:
            format_exc(e)