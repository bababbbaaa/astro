from databaseInteraction import *
import datetime
from utils import *

def upload_sources_from_excel():
    rows = parse_source_from_excel()

    for row in rows:
        date, title, code, type, price = row

        formatted_date = datetime.strftime(date, DATE_FORMAT)

        new_source = add_source(title, code, price, formatted_date, type)

    sources = get_sources()

    for source in sources:
        print(source.title)
