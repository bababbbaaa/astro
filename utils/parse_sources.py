"""

ВАЖНО !!!

Чтобы нормально конвертировать xlsx в xls, зайдите в эксель/либре и пересохраните
файл в другом формате, в ином случае ничего просто не будет работать, потому что
структура файла не поменяется, и он будет распознаваться, как xlsx

"""


import xlrd
import datetime

book = xlrd.open_workbook('sources.xls')
page = book.sheet_by_index(1)

for rx in range(1, page.nrows - 1):
    error, date, title, code, type_, price = page.row(rx)

    date = datetime.datetime(*xlrd.xldate_as_tuple(date.value,
                                                          book.datemode))

    title = title.value
    code = code.value
    type_ = type_.value
    price = int(price.value)


    print(date, title, code, type_, price)