# # # from urllib import request
# # from re import X
# # import telebot 
# import requests
# # # from threading import Thread
# # # import horoscopeusr
# # # import config
# # # import for_payments
# # # import telebot
# # # from telebot import types
# # # from posixpath import abspath
# # # import functools
# # # import string
# # # import functions
# # # from calendar import Calendar
# # # import string
# # # from sqlalchemy import *
# # # from sqlalchemy.orm import sessionmaker
# # # import horoscopedb
# # # from databaseInteraction import *
# # # from datetime import date, timedelta
# # # from datetime import datetime as date_time
# # out_summ=69.000000&OutSum=69.000000&inv_id=16799&InvId=16799&crc=502F0B1930B9DCAD0E0D6084CBA804A0&SignatureValue=502F0B1930B9DCAD0E0D6084CBA804A0&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=an177@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=610893809

# #out_summ=69.000000&OutSum=69.000000&inv_id=17574&InvId=17574&crc=A22A6FAD29799C1B21B12A2D5F79B773&SignatureValue=A22A6FAD29799C1B21B12A2D5F79B773&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=1707910@gmail.com&Fee=2.690000&Shp_days=30&Shp_id=629955174&Shp_prev=13639
# #out_summ=69.000000&OutSum=69.000000&inv_id=15228&InvId=15228&crc=5C279FD13D8B5796D4EA7494A19505E2&SignatureValue=5C279FD13D8B5796D4EA7494A19505E2&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=natalyailyina@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=635405278
#out_summ=69.000000&OutSum=69.000000&inv_id=19811&InvId=19811&crc=2062FC7FA250F008BC58873A8CEB35DA&SignatureValue=2062FC7FA250F008BC58873A8CEB35DA&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=YandexPayPSR&EMail=serg3jk0zl@yandex.ru&Fee=2.690000&Shp_days=30&Shp_id=952863788
# import requests
# #out_summ=69.000000&OutSum=69.000000&inv_id=16896&InvId=16896&crc=861B8AA4513C4A71900631C364E27121&SignatureValue=861B8AA4513C4A71900631C364E27121&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=bobalinaa@gmail.com&Fee=2.690000&Shp_days=30&Shp_id=297067072&Shp_prev=14763
# import requests
# # # # # # # from rich.console import Console
# request1=requests.post("http://195.2.79.3:443/get_payment",data={"out_summ":330.000000,"OutSum":330.000000,
# "inv_id":18434,"InvId":18434,"crc":"7B9A8D50DF7D3F8EF9338CBD8AE1E127","SignatureValue":"7A922835773700B51A21FF20B69BDB84","PaymentMethod":"BankCard","IncSum":330.000000,"Shp_days":180,"Shp_id":367565935,
# })
# print(request1.text)
# from databaseInteraction import * 970984910
#out_summ=69.000000&OutSum=69.000000&inv_id=19553&InvId=19553&crc=DBACC458D2042EADEB0FC221324A0B04&SignatureValue=DBACC458D2042EADEB0FC221324A0B04&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=Pabra1976@icloud.com&Fee=2.690000&Shp_days=30&Shp_id=808266836

# x=add_success_payment(telegram_id=0,payment_id=10,days=int(0),price=0,type_of_payment="SELF PAID")
# print(x)

# try:
#     x=10/0
# except Exception as err:
#     er=err
#     print(err)
# # # # import horoscopeproc

# # # from utils import *
# """fetch("https://partner.robokassa.ru/Operation/Search",

#  { "headers": 
#  { "accept": "*/*", "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "content-type": "application/x-www-form-urlencoded; charset=UTF-8", "sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"", "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": "\"Android\"", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "x-requested-with": "XMLHttpRequest"
#   },
#   "referrer": "https://partner.robokassa.ru/Operation?ShopId=6ad51909-4535-4237-8f7a-1c1b614c7519", "referrerPolicy": "strict-origin-when-cross-origin", "body": "SearchOp=SearchOp&__RequestVerificationToken=hAS0Z0KBIxo19-TlSvNz1KWZh8aWZ6i6YtcZtA60owxZqNW9n7eUhPt-TrRQc6vbgtyFW7SIP0Pv8eWNjD9AfVbJKs3S5N63SN4MZZu0B6GWMgRc0&DateFromMode=d&DateTillMode=d&FilterId=3749e51d-ad02-4779-826f-a51dd4cced04&FilterType=OperationsSearch&SortDirection=DSC&ColumnName=Sum&FilterName=&RowsPerPage=50&Country=RU&ShopForSearch=6ad51909-4535-4237-8f7a-1c1b614c7519&TotalRows=-1&SearchData=&CustomerEmail=&MaxSeconds=86399&MinSeconds=0&Days=&IncCurrLabel=&selectItemIncCurrLabel=&sMinSum=&sMaxSum=&OpState=OpDone&selectItemOpState=OpDone&X-Requested-With=XMLHttpRequest", 
# "method": "POST", "mode": "cors", "credentials": "include" });"""
# headers= { "accept": "*/*", "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "content-type": "application/x-www-form-urlencoded; charset=UTF-8", "sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"", "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": "\"Android\"", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "x-requested-with": "XMLHttpRequest"
#   }
# URL="https://partner.robokassa.ru/Operation/Search"

# import requests

# cookies = {
#     'mars': 'c6185f47e523465aba1a9bc66b11544e',
#     '.RBXPCID': '3emTn316eD9LSRf0WjPLCmPA8PC-0RIEejf6VM-NkUdZL_77mK7c8E5v-Yi1R6OO4g0SjA2',
#     'RoboxCulture_v2': 'ru',
#     '_ym_uid': '1660130256285645296',
#     '_ym_d': '1660130256',
#     'dbl': 'c076cdcfe3e64ce2a34779e02dc918f9',
#     'cf_clearance': 'viNiWJIcHafN5E9qPpaE0VdYl4Ns_9ZBhMckwEYsKoo-1661764279-0-150',
#     '_gcl_au': '1.1.1590171616.1665955588',
#     '__RequestVerificationToken': 'YWZ6LIl_pbl78AnqI3i__7tzT7fuo_nI-9ZYkQEJrUB8QQpeI9HY6LfCMUeIoxTb6al-Py_5F2JzX4meOjoQATVlxE41',
#     '_gid': 'GA1.2.1336783306.1669320498',
#     '_ym_isad': '1',
#     'ASP.NET_SessionId': 'eg2ufcxu2qrpdjvwebchfc4h',
#     'tmr_lvid': '0913fcb003063153b583e45bbe1ac48b',
#     'tmr_lvidTS': '1658137496438',
#     '_ym_visorc': 'b',
#     '.RBXPCID': '_woxB_vlbRfXdC9aAD03vbrcI24B7YN3xBUuloFZ4v7P7Cm_H7CqTho1tzuTt6uWTPMqUQ2',
#     '.RBXPC1': '172386668693E88AA0D36120E7A62E82C59AFEA28F082841EEA27366F59BF138FD65CB72EDAC77FD70E8126A4770D6F1F4C1467518DDFA607060D5D63270F8815E8DE19A4F1573AD8B8B2FC854025B0F07EB8AD2AE8B485450AFF2A5DA4A4D5667AE85E111A3AB8C0BF073BDA42D0F01EB3BF43C',
#     '.RBXPCROLES': 'IjfqOGla70f_fEz9YwrYfFzF0ymnAGl4yq_KVJ0bRaOAZJlCqFdAvymuQuYd9buOpzSUEur9dPZerQVWwg52Z7NA6FYQDgvvENF4SBCHCTWPaielI5IhQUU3LfLBzASh0Jzz_xQuM0vlCoHjdjU_E4ZZDdBiz0jPH0t3TtAJCA0AjQLk6fYOWt2Bjfeuqz2mRBx99b5adcRhxWcEBGrQqAY6p4l5vk6Ev7MLXuX-AZ-rA3oFpDpjvKFMB75xTHKq2MKXXPXV3_ZOtRYGhTljm2E8_fBx2Hi114E6guvP5Gjo29ELUBxi9xRX3TtcXAfoUN62yBYgYlrT3oxyrzr0QCt0Wx7CyEKCQj8GzNvoiQy9JzVg4ewACCuLWk8J_pvZfsQMuR8ZUQ_y3wCCgkwspKAraAt8a-sXuyvr-VXnYpQTqhZMVn2ByjohmLnOC4YoAAOQhe-vLr13p4CMSolpp3vngns18uh-5idD-z3f7mUDcU4t2cXgjmEWyi1-nviy3vLGUAK5qgW5QBBIUXCKG8C52pJM5Gghk5RRLqSgp63q9DJbaBsWor1POlsoMv_Gi4Lpj2OdSBTy3USubWgomnWHDjVGX7jwdIYOST8aGt2RS_XLk1LFUokQzW6QqSCcNtUQpw2',
#     '_ga_01GQYDTSB3': 'GS1.1.1669378028.57.1.1669378219.0.0.0',
#     'tmr_detect': '1%7C1669378219483',
#     '_ga': 'GA1.2.-399892839',
#     '_dc_gtm_UA-3853420-3': '1',
#     '_gali': 'SearchOp',
# }

# headers = {
#     'authority': 'partner.robokassa.ru',
#     'accept': '*/*',
#     'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
#     'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     # Requests sorts cookies= alphabetically
#     # 'cookie': 'mars=c6185f47e523465aba1a9bc66b11544e; .RBXPCID=3emTn316eD9LSRf0WjPLCmPA8PC-0RIEejf6VM-NkUdZL_77mK7c8E5v-Yi1R6OO4g0SjA2; RoboxCulture_v2=ru; _ym_uid=1660130256285645296; _ym_d=1660130256; dbl=c076cdcfe3e64ce2a34779e02dc918f9; cf_clearance=viNiWJIcHafN5E9qPpaE0VdYl4Ns_9ZBhMckwEYsKoo-1661764279-0-150; _gcl_au=1.1.1590171616.1665955588; __RequestVerificationToken=YWZ6LIl_pbl78AnqI3i__7tzT7fuo_nI-9ZYkQEJrUB8QQpeI9HY6LfCMUeIoxTb6al-Py_5F2JzX4meOjoQATVlxE41; _gid=GA1.2.1336783306.1669320498; _ym_isad=1; ASP.NET_SessionId=eg2ufcxu2qrpdjvwebchfc4h; tmr_lvid=0913fcb003063153b583e45bbe1ac48b; tmr_lvidTS=1658137496438; _ym_visorc=b; .RBXPCID=_woxB_vlbRfXdC9aAD03vbrcI24B7YN3xBUuloFZ4v7P7Cm_H7CqTho1tzuTt6uWTPMqUQ2; .RBXPC1=172386668693E88AA0D36120E7A62E82C59AFEA28F082841EEA27366F59BF138FD65CB72EDAC77FD70E8126A4770D6F1F4C1467518DDFA607060D5D63270F8815E8DE19A4F1573AD8B8B2FC854025B0F07EB8AD2AE8B485450AFF2A5DA4A4D5667AE85E111A3AB8C0BF073BDA42D0F01EB3BF43C; .RBXPCROLES=IjfqOGla70f_fEz9YwrYfFzF0ymnAGl4yq_KVJ0bRaOAZJlCqFdAvymuQuYd9buOpzSUEur9dPZerQVWwg52Z7NA6FYQDgvvENF4SBCHCTWPaielI5IhQUU3LfLBzASh0Jzz_xQuM0vlCoHjdjU_E4ZZDdBiz0jPH0t3TtAJCA0AjQLk6fYOWt2Bjfeuqz2mRBx99b5adcRhxWcEBGrQqAY6p4l5vk6Ev7MLXuX-AZ-rA3oFpDpjvKFMB75xTHKq2MKXXPXV3_ZOtRYGhTljm2E8_fBx2Hi114E6guvP5Gjo29ELUBxi9xRX3TtcXAfoUN62yBYgYlrT3oxyrzr0QCt0Wx7CyEKCQj8GzNvoiQy9JzVg4ewACCuLWk8J_pvZfsQMuR8ZUQ_y3wCCgkwspKAraAt8a-sXuyvr-VXnYpQTqhZMVn2ByjohmLnOC4YoAAOQhe-vLr13p4CMSolpp3vngns18uh-5idD-z3f7mUDcU4t2cXgjmEWyi1-nviy3vLGUAK5qgW5QBBIUXCKG8C52pJM5Gghk5RRLqSgp63q9DJbaBsWor1POlsoMv_Gi4Lpj2OdSBTy3USubWgomnWHDjVGX7jwdIYOST8aGt2RS_XLk1LFUokQzW6QqSCcNtUQpw2; _ga_01GQYDTSB3=GS1.1.1669378028.57.1.1669378219.0.0.0; tmr_detect=1%7C1669378219483; _ga=GA1.2.-399892839; _dc_gtm_UA-3853420-3=1; _gali=SearchOp',
#     'origin': 'https://partner.robokassa.ru',
#     'referer': 'https://partner.robokassa.ru/Operation?ShopId=6ad51909-4535-4237-8f7a-1c1b614c7519',
#     'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
#     'sec-ch-ua-mobile': '?1',
#     'sec-ch-ua-platform': '"Android"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
#     'x-requested-with': 'XMLHttpRequest',
# }

# data = {
#     'SearchOp': 'SearchOp',
#     '__RequestVerificationToken': 'hAS0Z0KBIxo19-TlSvNz1KWZh8aWZ6i6YtcZtA60owxZqNW9n7eUhPt-TrRQc6vbgtyFW7SIP0Pv8eWNjD9AfVbJKs3S5N63SN4MZZu0B6GWMgRc0',
#     'DateFromMode': 'd',
#     'DateTillMode': 'd',
#     'FilterId': '3749e51d-ad02-4779-826f-a51dd4cced04',
#     'FilterType': 'OperationsSearch',
#     'SortDirection': 'DSC',
#     'ColumnName': 'Sum',
#     'FilterName': '',
#     'RowsPerPage': '50',
#     'Country': 'RU',
#     'ShopForSearch': '6ad51909-4535-4237-8f7a-1c1b614c7519',
#     'TotalRows': '-1',
#     'SearchData': '',
#     'CustomerEmail': '',
#     'MaxSeconds': '86399',
#     'MinSeconds': '0',
#     'Days': '',
#     'IncCurrLabel': '',
#     'selectItemIncCurrLabel': '',
#     'sMinSum': '',
#     'sMaxSum': '',
#     'OpState': 'OpDone',
#     'selectItemOpState': 'OpDone',
#     'X-Requested-With': 'XMLHttpRequest',
# }
# import requests

# headers = {
#     'authority': 'partner.robokassa.ru',
#     'accept': '*/*',
#     'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
#     'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'cookie': 'mars=c6185f47e523465aba1a9bc66b11544e; .RBXPCID=3emTn316eD9LSRf0WjPLCmPA8PC-0RIEejf6VM-NkUdZL_77mK7c8E5v-Yi1R6OO4g0SjA2; RoboxCulture_v2=ru; _ym_uid=1660130256285645296; _ym_d=1660130256; dbl=c076cdcfe3e64ce2a34779e02dc918f9; cf_clearance=viNiWJIcHafN5E9qPpaE0VdYl4Ns_9ZBhMckwEYsKoo-1661764279-0-150; _gcl_au=1.1.1590171616.1665955588; __RequestVerificationToken=YWZ6LIl_pbl78AnqI3i__7tzT7fuo_nI-9ZYkQEJrUB8QQpeI9HY6LfCMUeIoxTb6al-Py_5F2JzX4meOjoQATVlxE41; _gid=GA1.2.1336783306.1669320498; _ym_isad=1; ASP.NET_SessionId=eg2ufcxu2qrpdjvwebchfc4h; tmr_lvid=0913fcb003063153b583e45bbe1ac48b; tmr_lvidTS=1658137496438; _ym_visorc=b; .RBXPCID=_woxB_vlbRfXdC9aAD03vbrcI24B7YN3xBUuloFZ4v7P7Cm_H7CqTho1tzuTt6uWTPMqUQ2; .RBXPC1=172386668693E88AA0D36120E7A62E82C59AFEA28F082841EEA27366F59BF138FD65CB72EDAC77FD70E8126A4770D6F1F4C1467518DDFA607060D5D63270F8815E8DE19A4F1573AD8B8B2FC854025B0F07EB8AD2AE8B485450AFF2A5DA4A4D5667AE85E111A3AB8C0BF073BDA42D0F01EB3BF43C; .RBXPCROLES=IjfqOGla70f_fEz9YwrYfFzF0ymnAGl4yq_KVJ0bRaOAZJlCqFdAvymuQuYd9buOpzSUEur9dPZerQVWwg52Z7NA6FYQDgvvENF4SBCHCTWPaielI5IhQUU3LfLBzASh0Jzz_xQuM0vlCoHjdjU_E4ZZDdBiz0jPH0t3TtAJCA0AjQLk6fYOWt2Bjfeuqz2mRBx99b5adcRhxWcEBGrQqAY6p4l5vk6Ev7MLXuX-AZ-rA3oFpDpjvKFMB75xTHKq2MKXXPXV3_ZOtRYGhTljm2E8_fBx2Hi114E6guvP5Gjo29ELUBxi9xRX3TtcXAfoUN62yBYgYlrT3oxyrzr0QCt0Wx7CyEKCQj8GzNvoiQy9JzVg4ewACCuLWk8J_pvZfsQMuR8ZUQ_y3wCCgkwspKAraAt8a-sXuyvr-VXnYpQTqhZMVn2ByjohmLnOC4YoAAOQhe-vLr13p4CMSolpp3vngns18uh-5idD-z3f7mUDcU4t2cXgjmEWyi1-nviy3vLGUAK5qgW5QBBIUXCKG8C52pJM5Gghk5RRLqSgp63q9DJbaBsWor1POlsoMv_Gi4Lpj2OdSBTy3USubWgomnWHDjVGX7jwdIYOST8aGt2RS_XLk1LFUokQzW6QqSCcNtUQpw2; _ga_01GQYDTSB3=GS1.1.1669378028.57.1.1669378219.0.0.0; tmr_detect=1%7C1669378219483; _ga=GA1.2.-399892839; _dc_gtm_UA-3853420-3=1; _gali=SearchOp',
#     'origin': 'https://partner.robokassa.ru',
#     'referer': 'https://partner.robokassa.ru/Operation?ShopId=6ad51909-4535-4237-8f7a-1c1b614c7519',
#     'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
#     'sec-ch-ua-mobile': '?1',
#     'sec-ch-ua-platform': '"Android"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
#     'x-requested-with': 'XMLHttpRequest',
#     'authority': 'partner.robokassa.ru',
#     'accept': '*/*',
#     'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
#     'cookie': 'mars=c6185f47e523465aba1a9bc66b11544e; .RBXPCID=3emTn316eD9LSRf0WjPLCmPA8PC-0RIEejf6VM-NkUdZL_77mK7c8E5v-Yi1R6OO4g0SjA2; RoboxCulture_v2=ru; _ym_uid=1660130256285645296; _ym_d=1660130256; dbl=c076cdcfe3e64ce2a34779e02dc918f9; cf_clearance=viNiWJIcHafN5E9qPpaE0VdYl4Ns_9ZBhMckwEYsKoo-1661764279-0-150; _gcl_au=1.1.1590171616.1665955588; __RequestVerificationToken=YWZ6LIl_pbl78AnqI3i__7tzT7fuo_nI-9ZYkQEJrUB8QQpeI9HY6LfCMUeIoxTb6al-Py_5F2JzX4meOjoQATVlxE41; _gid=GA1.2.1336783306.1669320498; _ym_isad=1; ASP.NET_SessionId=eg2ufcxu2qrpdjvwebchfc4h; tmr_lvid=0913fcb003063153b583e45bbe1ac48b; tmr_lvidTS=1658137496438; _ym_visorc=b; .RBXPCID=_woxB_vlbRfXdC9aAD03vbrcI24B7YN3xBUuloFZ4v7P7Cm_H7CqTho1tzuTt6uWTPMqUQ2; .RBXPC1=172386668693E88AA0D36120E7A62E82C59AFEA28F082841EEA27366F59BF138FD65CB72EDAC77FD70E8126A4770D6F1F4C1467518DDFA607060D5D63270F8815E8DE19A4F1573AD8B8B2FC854025B0F07EB8AD2AE8B485450AFF2A5DA4A4D5667AE85E111A3AB8C0BF073BDA42D0F01EB3BF43C; tmr_detect=1%7C1669378295644; .RBXPCROLES=f6LebUPoc7ehSUN9YiOVyigDAGUkWANJ1rdYdz6c2YLQNu9MJyVCipeAsHrhJc_uEF17NXS0VUztCMwxr0Zw0lmuf6f5l6O4FG_jJAuxUCrsqQPc6orhnpA0c9Iz8Wzq2cY3r0bZkILJH_QeiY1UDCPH2cxSw3BACs0cb0MioDhZ3UfslOCl1FKF9Gr7Y3lSYuSoPnAw1KVI3oqWBRxJMbKjLqzPBajL9HEB_j9H1VJG8aCIoP_XS1oIsDxz7JV2biGapDPbMKUBQl7IY9Wj-4g6KZGRZ5dTn9iKZHTp7bM2sbx98ONFwPbYvEy65V2QILKaaYEX-f8vxaMND4bnczmF78Xg8VILdFhBIQwakQ2dccdQkXxaO5G9g2HCPozVye85nmODlalLfyUqOqikuBJw_rBeKKw9rdcYI3k6EwHLvqrENZ5wWA-JBDAs2o2xA042ppWprK0gIjAWJU9NwskixPjVDKvf626W2pcj8CTfAs6xerMQ9u4AOdR5iexVYC94xa1dKGRYmxY5iqdBB1qy_O6ggte3neX2p78o8gnXs2Udc8emx1GaId06RyUkZaSDRliuIkATIorCZbRyiBvNVI4ZjmBuoKwxcVyaXQ_w7wuG6H3MnFK_Lth6ijfLuiS3OA2; _dc_gtm_UA-3853420-3=1; _gat_gtag_UA_3853420_3=1; _ga_01GQYDTSB3=GS1.1.1669378028.57.1.1669379028.0.0.0; _ga=GA1.2.-399892839',
#     'referer': 'https://partner.robokassa.ru/Operation?ShopId=6ad51909-4535-4237-8f7a-1c1b614c7519',
#     'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
#     'sec-ch-ua-mobile': '?1',
#     'sec-ch-ua-platform': '"Android"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
#     'x-requested-with': 'XMLHttpRequest',
# }

# params = {
#     'Id': '254659780',
#     'OriginNomenclatureCode': 'true',
#     '_': '1669379067930',
# }

# response = requests.get('https://partner.robokassa.ru/Operation/GetOpDetails', params=params, headers=headers)
# # response = requests.post('https://partner.robokassa.ru/Operation/Search', cookies=cookies, headers=headers, data=data)
# print( dir(response))
# print(response.text)
# # TOKEN = config.TOKEN
# # delete_cache = {}
# # bot = telebot.TeleBot(TOKEN, parse_mode=None)
# # for i in range(1719514-1000,1719514+10):
# #     try:
# #         mes=bot.forward_message(952863788,1057824180,message_id=i)
# #         print(mes)
# #         break
# #     except Exception as err:
# #         print(err)
# #         continue
# # us_info=bot.get_chat_member(1057824180,1057824180)
# # print(us_info)
# # messages.getMessages
# # conn=horoscopedb.ConnectDb()
# # cur = conn.cursor()   
# # cur.execute("SELECT * FROM Users")
# # res = list()
# # records = cur.fetchall()
# # cur.close()
# # conn.commit()
# # for row in records:
# #     res.append({"ID":row[0],"Name":row[1],"is_main":row[2],"BirthTime":row[4],
# # "Birthday":row[5],"Gender_ID":row[3],'Birthplace':row[6],"DesTime_ID":row[7],
# # "TimeZone":row[8],"TelegramID":row[9],"RegDate":row[10],"IsActiveBot":row[12],
# # "Balance":row[13],"IsActiveSub":row[14],"SubscrType_ID": row[15],
# # "ActiveUntil":row[16],"DateSend":row[17],"Source_ID":row[22]
# # })
# # # message_id=1719513
# # # # res.reverse()
# # # # print(res)
# # # # result1=0
# # # # while True:
# # # #     try:
# # # #         print(result1)
# # # #         result=res[result1]
# # # #         result1+=1
# # # #         mes=bot.forward_message(952863788,1057824180,message_id=message_id)
# # # #         print(mes)
# # # #         print(result["TelegramID"])
# # # #         # if mes.
        
# # # #         if int(result["TelegramID"])==5127634821:
# # # #             message_id-=1
# # # #             result1=0
# # # #         else:
# # # # #             break
# # # # #     except Exception as err:
# # # # # #         # print(err)
# # # # add_payment(sub_type=3,telegram_id=1,payment_id=str(count_payments()),active_until="10.10.1000",days=30,payed=True,amount=69,link="REC")
# # # # # #         continue
# # # # # pay=for_payments.get_money_for_sub(id=int(10332),amount=69,days=30,test=0)
# # # # # add_payment(sub_type=3,telegram_id=1,payment_id=str(count_payments()),active_until="10.10.10",days=30,payed=True,amount=69,link="REC")
# # # # # # print(pay.text)
# # # # # pay=for_payments.get_money_for_sub(id=int(10359),amount=69,days=30,test=0)
# # # # # print(pay.text)
# # # # # add_payment(sub_type=3,telegram_id=1,payment_id=str(count_payments()),active_until="10.10.1000",days=30,payed=True,amount=69,link="REC")

# # # # # pay=for_payments.get_money_for_sub(id=int(10378),amount=69,days=30,test=0)
# # # # # print(pay.text)
# # # # # add_payment(sub_type=3,telegram_id=1,payment_id=str(count_payments()),active_until="10.10.1000",days=30,payed=True,amount=69,link="REC")
# # # # LOGIN="Astrobot"
# # # # PASSWORD_FOR_ROBOKASSA="oLy0Vda8EbnP8wlR5Xi1"
# # # # # idempotence_key = str(uuid.uuid4())
# # # # account_id_shop="jkdskd"
# # # # gateway_id_shop=""
# # # # MAIN_PASSWORD="oLy0Vda8EbnP8wlR5Xi1"
# # # # TEST_PASSWORD="ygAdIPC6I1c1qxER1Iu8"
# # # # # pay=for_payments.get_money_for_sub(id=int(10853),amount=69,days=30,test=0,tg_id=)
# # # # # # print(pay.text)
# # # # # # add_payment(sub_type=3,telegram_id=1,payment_id=str(count_payments()),active_until="10.10.10",days=30,payed=True,amount=69,link="REC")

# # # # # pay=for_payments.get_money_for_sub(id=int(10210),amount=69,days=30,test=0)
# # # # # print(pay.text)
# # # # # add_payment(sub_type=3,telegram_id=1,payment_id=str(count_payments()),active_until="10.10.10",days=30,payed=True,amount=69,link="REC")

# # # # import robokassa
# # # # # add_payment(sub_type=3,telegram_id=2,payment_id=str(count_payments()),active_until="01.10.1000",days=30,payed=True,amount=0,link="try REC")
# # # # x=robokassa.earn_recurrent_pay("Astrobot",PASSWORD_FOR_ROBOKASSA,cost=69,number=10853,description="Оплата подписки на астробота",is_test=0,days=30,tg_id=5088332038)
# # # # print(x)
# # # # pass 
# # # DATE_FORMAT = '%d.%m.%Y'
# # # from datetime import date,timedelta

# # # import datetime
# # # # def change_active_until_date(start,date_end,days,base="subs"):
# # # #     if date_end.find("-")!=-1:
# # # #         date_end=datetime.strptime(date_end, "%Y-%m-%d")
# # # #         date_end=datetime.strftime(date_end, DATE_FORMAT)
# # # #     if datetime.strptime(start,DATE_FORMAT)>=datetime.strptime(date_end,DATE_FORMAT):
# # # #         uctive_until=datetime.strptime(start,DATE_FORMAT)+timedelta(days=days)
# # # #     else:
# # # #         uctive_until=datetime.strptime(date_end,DATE_FORMAT)+timedelta(days=days)
# # # #     if base=="users":
# # # #         end=datetime.strftime(uctive_until, "%Y-%m-%d")
# # # #     else:
# # # #         end = datetime.strftime(uctive_until, DATE_FORMAT)
# # # #     return(end)
# # # from sqlite3 import *
# # # conn = connect('horoscope.db')
# # # cur=conn.cursor()
# # # statements=cur.execute("SELECT * FROM Subscriptions")
# # # statements=statements.fetchall()
# # # for i in statements:
# # #     end=i[4]
# # #     if datetime.datetime.strptime(end,DATE_FORMAT)<=datetime.datetime.strptime("03.10.2022",DATE_FORMAT):
# # #         new_end=datetime.datetime.strptime(end,DATE_FORMAT)+timedelta(days=30)
# # #         new_end = datetime.datetime.strftime(new_end, DATE_FORMAT)
# # #         cur.execute("""UPDATE Subscriptions SET End = ? WHERE (ID = ?)""" ,(new_end,i[0]))
# # # cur.close()
# # # conn.commit()
# import config
# bot=telebot.TeleBot(token=config.TOKEN)
# # bot.forward_message(952863788,952863788,1635)
# # import horoscopeproc
# # id=494603937
# # # print(horoscopeproc.GenHourMessAll(
# # #                             11, inpTelegramID=str(id)))
# # import functions
# # import horoscopeusr
# # # or functions.ListUserName(inpTelegramID=id)[0]==None:
# # if horoscopeusr.RegUser(inpTelegramID=str(id))[0] == True:

# #     print(
# #                             id, '7Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
# # elif functions.ListUserName(inpTelegramID=id)[0] == "":

# #     print(
# #                             id, '2Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
# # else:
# #     us = functions.GetUsers(id)[0]
# #     if us["Name"] == None:
# #         print(
# #             id, '3Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')

# #     elif us["Birthday"] == None:
# #         print(
# #             id, '4Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
# #     elif us["BirthTime"] == None:
# #         print(
# #             id, '5Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
# #     elif us["Birthplace"] == None:
# #         print(
# #             id, '6Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
# #     elif us["RegDate"] == None:
# #         print(
# #             id, '9Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')

# #     else:
# #         # name=functions.ListUserName(inpTelegramID=int(id))[0]
        
# #         js = horoscopeproc.GenHourMessAll(
# #             11, inpTelegramID=str(id))
# #         txt = js[0]
# #         # print(js)
# #         today_send = txt[6]
# #         if functions.select_all_active_until_table(id)["days_till_end"]+1<=0:
# #             horoscopeusr.ChUserInfo(inpTelegramID=id,inpFieldName="SubscrType_ID",inpValue=5)
# #             horoscopeusr.ChUserInfo(inpFieldName="IsActiveSub",inpTelegramID=id,inpValue=0)
# #             # subscribe(message)
                                                                                                                                                                                                                
# #         elif today_send:
            
# #             text = ""
# #             text += (js[0][2]+"\n\n"+js[0][3])
# #             print(
# #                             id, '10Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')
# #         else:
# #             text = ""
# #             text += (js[0][2]+"\n\n"+js[0][3])
# #             print(
# #                             id, '100Ваш персональный гороскоп будет сформирован после того, как Вы введете все необходимые данные. Пожалуйста, закончите регистрацию.')

# #             # bot.register_next_step_handler(mes,main)

# # import time
# # import horoscopeproc
# # import functions
# # horoscope=horoscopeproc.GenHourMessAll(11,110796470)
# # print(len(horoscope[0]))
# # x=functions.select_all_active_until_table(110796470)
# # print(x)
# x="https://t.me/+-k8MSbOEqeVhMzc6"
# print(x.split("-"))
# # from threading import Thread
# # def wait_until_send(id,text,reply_markup=None,parse_mode=None,url=None):
# #     while True:
# #         try:
# #             mes=bot.send_message(id,text,reply_markup=reply_markup,parse_mode=parse_mode)
# #             return mes
# #         except Exception as err:
            
# #             if 'error_code' not in vars(err).keys():
# #                 return 0
                
# #             if err.error_code==429:
# #                 return err

# #             elif err.error_code==400:
# #                 return err
# #             elif err.error_code==403:
# #                 return err
# # with open("НеОконченаРегистрация.txt","r") as x:
# #     x=x.readlines()
# #     for id in x:
# #         id=int(id)
# #         Thread(target=wait_until_send,args=(id,"Добрый день! Мы рады, что вы заглянули в наш Астробот. К сожалению, вы не закончили регистрацию, возможно, бот был перегружен обращениями и зависал. Мы будем рады, если вы попробуете зарегистрироваться еще раз - сейчас все должно работать хорошо. Для этого остановите и перезапустите Астробот и ответьте на вопросы заново. Если у вас все равно возникли проблемы с регистрацией, пожалуйста, напишите нам в поддержку в @AstroBot_support. Прекрасного дня! 🌸",None,"html")).start()
# #         time.sleep(1/28)
# import datetime
# # print(datetime.datetime.strftime(datetime.datetime.now(),"%H:%M"))
# import horoscopeusr as horoscopeusr
# import horoscopeproc
# import functions
# # print(horoscopeproc.GenHourMessAll(11,"245188029"))1358174961
# import time
# import functions
# time1=time.time()
# x=functions.GetUsers("952863788")
# time2=time.time()
# print(time2-time1)
# # print(x)
# time1=time.time()
# x=functions.RegMainUser("121313131")
# time2=time.time()
# print(time2-time1)
# time1=time.time()
# x=functions.GetUsers("1358174961")
# time2=time.time()
# print(time2-time1)
# # print(x)
# time1=time.time()
# x=horoscopeproc.GenHourMessAll(11,"1358174961")
# time2=time.time()
# print(time2-time1)
# import horoscopedb
# # from utils import *
# from databaseInteraction import *
# from controller import *
# from utils import *
# session=Session
# result=session.query(Post).first()
# # print(result)
# for i in range(100):
#     res=add_payment(sub_type=3,telegram_id="952863788",payment_id=str(count_payments()),active_until="01.10.1000",days=30,payed=True,amount=0,link="UNSUB")
# print(session.query(Payment).count())
# # session=create_session()
# # conn=horoscopedb.ConnectDb()
# # cur=conn.cursor()
# # res=cur.execute("SELECT * FROM Users")
# # # print(res)
# # print (res)
# from mailing import *

# photos={}
# photos["0"]=open("days/"+"0.jpg","rb").read()

# photos["3"]=open("days/"+"3.jpg","rb").read()

# photos["7"]=open("days/"+"7.jpg","rb").read()

# photos["1"]=open("days/"+"1.jpg","rb").read()
# photos["10"]=open("days/"+"10.png","rb").read()
# x=make_notificartion_with_keyboard(id=952863788,photo=photos["3"],end_time=3)
# x=make_notificartion_with_keyboard(id=952863788,photo=photos["3"],end_time=3)

# y=make_notificartion_with_keyboard(952863788,photos[str(0)],0)
# z=make_notificartion_with_keyboard(952863788,photos[str(1)],1)
# caption="""Заметили, что последние 3 дня даются вам тяжелее обычного? 
# Все потому, что вы забыли оформить подписку на Астробота, который составляет для вас ежедневный персональный гороскоп с учетом вашей натальной карты! 

# Оформите подписку прямо сейчас, и вы сможете строить планы, разбираться в различных ситуациях и получать максимум от каждого дня!"""
# make_notificartion_with_keyboard(952863788,photos[str(3)],3,caption)

# caption="""Заметили, что последние 10 дней даются вам тяжелее обычного? 
# Все потому, что вы забыли оформить подписку на Астробота, который составляет для вас ежедневный персональный гороскоп с учетом вашей натальной карты! 

# Оформите подписку прямо сейчас, и вы сможете строить планы, разбираться в различных ситуациях и получать максимум от каждого дня!"""
# # # print(id,all_service_messages[i])
# # u=make_notificartion_with_keyboard(952863788,photos[str(10)],10,caption) 



# # print(x)

# # import horoscopeproc
# # x=horoscopeproc.GenHourMessAll(1,788258764)
# # # print(x)
# # import controller
# # from databaseInteraction import *

# # from threading import Thread 
# # import horoscopedb
# # TOKEN="5393264409:AAFd137o2MSINcbYLK_9s2UZso_0OAXUBmU"
# # import telebot
# # conn=horoscopedb.ConnectDb()
# # cursor=conn.cursor()
# # bot = telebot.TeleBot(TOKEN, parse_mode=None)
# # import time
# # list_of_users=cursor.execute("SELECT TelegramID FROM horoscope.Users WHERE SubscrType_ID=3 or SubscrType_ID=1;")
# # list_of_users=cursor.fetchall()
# # conn.commit()
# # for i in range(len(list_of_users)):
# #     Thread(target=bot.send_message,args=(list_of_users[i][0],"""
# #     Уважаемые подписчики, к сожалению, сегодня в нашем боте произошел технический сбой, в связи с чем утренние гороскопы не были разосланы вовремя. Сейчас все исправлено и вы должны были получить ваш гороскоп. Если все-таки он вам не пришел, просим написать в поддержку или воспользоваться командой /send в меню. Приносим свои извинения за случившееся, постараемся избежать повторения в дальнейшем. Приятного дня!
# #     """)).start()
# #     time.sleep(1/15)
# # session=sessionmaker(engine)()

# # x=session.query(User).filter_by(TelegramID="952863788").update({"TelegramID":"0"})
# # session.commit()

# # session.delete(x)
# # session.commit()


# # import horoscopeusr
# # x=horoscopeusr.ChUserInfo(inpValue=int(
# #                     298208027), inpTelegramID=str(952863788), inpFieldName="Source_ID")
# # # print(x)
# # import horoscopeusr

# # x=horoscopeusr.DelTmpUser()
# # print(x)
# from datetime import datetime,timedelta
# from databaseInteraction import *
# from openpyxl import *
# def transfer_to_success_payment(file):
#     workbook = load_workbook(file)
#     sheet=workbook.get_sheet_by_name('users')
#     i=2
#     session=sessionmaker(engine)()
#     while True:
        
#         inv_id=str(sheet["A"+str(i)].value)
#         if inv_id=="" or inv_id=="None":
#             break


#         x=session.query(SuccessPayment).filter_by(payment_id=inv_id).all()
#         if len(x)==0:
            
#             price=int(str(sheet["C"+str(i)].value))
#             date=sheet["J"+str(i)].value
#             # date=datetime.strptime(date,"%d.%m.%y %H:%M")
#             params=str(sheet["L"+str(i)].value)
#             params=params.split("&")
#             kwargs={}


#             for i in range(len(params)):
#                 params[i]=params[i].split("=")
#                 dictionary=params[i]
#                 kwargs[dictionary[0]]=dictionary[1]

#             days=int(kwargs["Shp_days"])

#             active_until=date+timedelta(days=days)
#             telegram_id=kwargs["Shp_id"]
#             if "Shp_prev" in kwargs.keys():
#                 prev_id=kwargs["Shp_prev"]
#             else:
#                 prev_id=None
#             all_success_payments=session.query(SuccessPayment).filter_by(telegram_id=telegram_id).all()

#             user=session.query(User).filter_by(TelegramID=telegram_id).first()

#             try:
#                 payment_id=int(all_success_payments[0].payment_id)
#                 for i in range(len(all_success_payments)):
#                     if all_success_payments[0].payment_id<payment_id:
#                         payment_id=all_success_payments[0].payment_id
#             except:
#                 payment_id=100000
#             if prev_id!=None:


#                 new_payments=SuccessPayment(
#                     telegram_id=telegram_id,
#                     payment_id=inv_id,
#                     days=days,
#                     amount=price,
#                     payment_date=date,
#                     active_until=active_until,
#                     user_name=user.Name,
#                     source_id=user.Source_ID,
#                     payed=1,
#                     type_of_payment="REC",
#                     birth_day=datetime.strptime(user.Birthday,"%d.%m.%Y")
#                 )

#                 session.add(new_payments)
#             elif int(payment_id)>int(inv_id):

                
#                 try:
#                     session.query(SuccessPayment).filter_by(payment_id=all_success_payments[0].payment_id).update({
#                     "type_of_payment":"SELF PAID"
#                 })
#                 except:
#                     pass


#                 new_payments=SuccessPayment(
#                     telegram_id=telegram_id,
#                     payment_id=inv_id,
#                     days=days,
#                     amount=price,
#                     payment_date=date,
#                     active_until=active_until,
#                     user_name=user.Name,
#                     source_id=user.Source_ID,
#                     payed=1,
#                     type_of_payment="FIRST PAY",
#                     birth_day=datetime.strptime(user.Birthday,"%d.%m.%Y")
#                 )
#                 session.add(new_payments)


#             else:


#                 new_payments=SuccessPayment(
#                     telegram_id=telegram_id,
#                     payment_id=inv_id,
#                     days=days,
#                     amount=price,
#                     payment_date=date,
#                     active_until=active_until,
#                     user_name=user.Name,
#                     source_id=user.Source_ID,
#                     payed=1,
#                     type_of_payment="SELF PAID",
#                     birth_day=datetime.strptime(user.Birthday,"%d.%m.%Y")
#                 )
#                 session.add(new_payments)
#         i+=1
#     print(workbook)
#     session.commit()
# x=transfer_to_success_payment("Astrobot_07.11.2022-13.11.2022.xlsx")
# # # print(x)
# import horoscopeproc
# import horoscopeusr
# # first_part=horoscopeproc.GenHourMessAll(0,850703853)[0][2]
# # # for i in range(len(x)):
# # #     if x[i][0]==850703853:
# # #         print(1)
# # from threading import Thread
# # import telebot
# # # import sys 
# # # print (sys.path)
# # import morning  
# # date_today=morning.Get_Data()
# # #"date_pict\16.10.2022.png"
# # path="date_pict/"+date_today+".png"
# # pict=open(path,"rb").read()
# # buttons=telebot.types.InlineKeyboardMarkup()
# # but=telebot.types.InlineKeyboardButton(text="Получить персональный гороскоп",callback_data="SUBSCR_ACT")

# # Thread(target=morning.wait_until_send_photo,args=(850703853,pict,first_part,None,"html")).start()
# x=horoscopeproc.GenHourMessAll(0,9090909090909090)
# print(x)







# import horoscopedb
# import config
# import telebot
# from telebot import types
# bot=telebot.TeleBot(token=config.TOKEN)
# from datetime import datetime
# from threading import Thread
# import time
# conn=horoscopedb.ConnectDb()
# cur=conn.cursor()
# cur.execute("SELECT * FROM Users WHERE IsActiveBot=1 AND SubscrType_ID=5")
# res=cur.fetchall()
# mark_up=types.ReplyKeyboardRemove()
# today=datetime.now().date()
# # days_till_end=end_date-today_data
# # days_till_end=days_till_end.days
# bot.send_message(5127634821,"рассылка началась")

# text='''Добрый день! Наверняка, вы убедились, что последнее время вам гораздо сложнее принимать решения, возникают непредвиденные трудности, да и в общем жизнь дается вам тяжелее обычного? 

# Оформите прямо сейчас подписку на Астробота, который составляет для вас ежедневный персональный гороскоп с учетом вашей натальной карты, и вы сможете строить планы, разбираться в различных ситуациях и получать максимум от каждого дня! Чтобы подписаться нажмите /subscribe'''
# with open("05_12_test.jpg","rb") as photo:
#     photo=photo.read()
# # bot.send_photo(952863788,caption=text,photo=photo,reply_markup=mark_up)
# # bot.send_photo(952863788,caption=text,photo=photo,reply_markup=mark_up)
# res=list(res)
# res=res[::-1]
# # breakpoint()
# for i in range(len(res)):
#     x=res[i]
#     date=x[16]-today
#     days=date.days
#     if days not in config.days_for_mailing and days!=-10 and days!=-3:
#         Thread(target=bot.send_photo,args=(x[9],photo,text),kwargs={"reply_markup":mark_up}).start()
#         time.sleep(1/10)

# bot.send_message(5127634821,"рассылка закончилась")




# # import horoscopeproc
# # id=5432089379
# # js = horoscopeproc.GenHourMessAll(11, inpTelegramID=str(id))
# # print(js)\
# x=bot.get_chat("573614210")
# print(x)


import requests

requets=requests.post("http://127.0.0.1:5000/get_amount_of_sources",json={})
print(requets.text)
# from databaseInteraction import *
# import time

# x=SessionWeb.query(WebSource).all()
# print(len(x))
# Session.commit()
# time.sleep(60)

# x=SessionWeb.query(WebSource).all()
# print(len(x))
# print(get_success_web_payments())
# from for_payments import *


# pay=get_money_for_sub(id=int(28104),amount=69,days=30,test=0,tg_id=952863788)
# # pay=robokassa.generate_payment_link_recurse(LOGIN,MAIN_PASSWORD,cost=69,number=952863788,description="Оплата подписки на астробота",is_test=0,days=30)
# print(pay.text)

# out_summ=69.000000&OutSum=69.000000&inv_id=28212&InvId=28212&crc=FB6DDBFABEE9AD2D2942B120852FFB3E&SignatureValue=FB6DDBFABEE9AD2D2942B120852FFB3E&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=katrin.kachalina@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=773884210

# out_summ=69.000000&OutSum=69.000000&inv_id=28243&InvId=28243&crc=4AFF5E05601D1EDB2E881578BDC2F114&SignatureValue=4AFF5E05601D1EDB2E881578BDC2F114&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=shyrpaliza@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=410566780&Shp_prev=16791

# import requests
# # import json
# requets=requests.post("http://127.0.0.1:5000/get_payment",data={"out_summ":69.000000,"OutSum":69.000000,
# "inv_id":28243,"InvId":28243,"crc":"7B9A8D50DF7D3F8EF9338CBD8AE1E127","SignatureValue":"7A922835773700B51A21FF20B69BDB84","PaymentMethod":"BankCard","IncSum":330.000000,"Shp_days":30,"Shp_id":410566780,"Shp_prev":16791
# })

# # data={"out_summ":330.000000,"OutSum":330.000000,
# # "inv_id":18434,"InvId":18434,"crc":"7B9A8D50DF7D3F8EF9338CBD8AE1E127","SignatureValue":"7A922835773700B51A21FF20B69BDB84","PaymentMethod":"BankCard","IncSum":330.000000,"Shp_days":180,"Shp_id":367565935,
# # })


# print(requets.text)

# from threading import Thread
# from config import *
# import telebot
# text1='''
# Дорогие подписчики!

# Пришло время рассказать вам об астрологе, без чьей помощи мы не смогли бы создать наш Астробот. Это автор канала Ретроградный Меркурий, один из самых популярных и ироничных астрологов в Телеграмме, чьи гороскопы читаются, как захватывающий роман, и одновременно астрологически безупречно точны.

# Наша команда выражает огромную благодарность за помощь автору канала Ретроградный Меркурий и надеется на продолжение совместной работы.

# И да, мы завидуем тем, кто прочтет гороскопы в первый раз, вас ждет незабываемое удовольствие от чтения, прилив энергии и море позитивных изменений в жизни!

# <a href="https://t.me/+54rR3Kjo59w3NDQy">Переходите по ссылке и наслаждайтесь! </a>

# Ваш Астробот.'''
# import time
# from databaseInteraction import *
# bot=telebot.TeleBot(token=TOKEN)
# photo=open("photo_2022-12-21_12-16-46.jpg","rb").read()
# session=sessionmaker(engine)()
# users=session.query(User).filter_by(IsActiveBot=1,SubscrType_ID=5).all()
# Thread(target=bot.send_photo,args=(5127634821,photo,text1,"html")).start()
# Thread(target=bot.send_photo,args=(952863788,photo,text1,"html")).start()


# for i in range(len(users)):
#     Thread(target=bot.send_photo,args=(users[i].TelegramID,photo,text1,"html")).start()
#     # bot.send_photo(id,)
#     # pass
#     time.sleep(1/10)

# Thread(target=bot.send_photo,args=(5127634821,photo,text1,"html")).start()
# Thread(target=bot.send_photo,args=(952863788,photo,text1,"html")).start()




# from databaseInteraction import *

# session_web=sessionmaker(engine_web)()
# session=sessionmaker(engine)()

# x=session.query(Payment).filter_by(link='try REC').all()

# for i in range(len(x)):
#     payment=x[i].payment_id

#     sess=session.query(SuccessPayment).filter_by(payment_id=payment).first()
#     if sess==None:
#         # users=session.query(User).filter_by(TelegramID=sess.telegram_id).first()
#         add_success_payment(telegram_id=x[i].telegram_id,payment_id=x[i].payment_id,days=x[i].days,price=0,type_of_payment="TRY REC")
# session.commit()
# session=sessionmaker(engine)()

# x=session.query(Payment).filter_by(link='REC').all()
# for i in range(len(x)):
#     sess=session.query(SuccessPayment).filter_by(telegram_id=x[i].telegram_id,type_of_payment="TRY REC"
#     ).first()
#     if sess!=None:
#         session.query(telegram_id=x[i].telegram_id,type_of_payment="TRY REC").update(
#             {"amount":69,"type_of_payment":"REC"}
#         )
#     session.commit()
# lists=["out_summ=69.000000&OutSum=69.000000&inv_id=28288&InvId=28288&crc=84C3943C9B9AF5377EEC3166C4BF2611&SignatureValue=84C3943C9B9AF5377EEC3166C4BF2611&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=K_striga@bk.ru&Fee=2.690000&Shp_days=30&Shp_id=691241035"]

    # "out_summ=69.000000&OutSum=69.000000&inv_id=28203&InvId=28203&crc=7E2B0CF1738753B2921C292C84E0A9B1&SignatureValue=7E2B0CF1738753B2921C292C84E0A9B1&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=kvas_tonya@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=1361118358",
# "out_summ=69.000000&OutSum=69.000000&inv_id=27878&InvId=27878&crc=54EDA12891279D97F9837AAC97CDA713&SignatureValue=54EDA12891279D97F9837AAC97CDA713&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=ksouishh@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=1388473719",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28212&InvId=28212&crc=FB6DDBFABEE9AD2D2942B120852FFB3E&SignatureValue=FB6DDBFABEE9AD2D2942B120852FFB3E&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=katrin.kachalina@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=773884210",
# "out_summ=580.000000&OutSum=580.000000&inv_id=28268&InvId=28268&crc=F2CD8CC94A32215A091C8F8306DB9864&SignatureValue=F2CD8CC94A32215A091C8F8306DB9864&PaymentMethod=BankCard&IncSum=580.000000&IncCurrLabel=BankCardPSR&EMail=valeriyan90@mail.ru&Fee=22.620000&Shp_days=365&Shp_id=870022954",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28250&InvId=28250&crc=2DDDF92ED4685725C3DE275083D9B652&SignatureValue=2DDDF92ED4685725C3DE275083D9B652&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=79043875625@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=1388009784&Shp_prev=16948",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28247&InvId=28247&crc=57D5C23FB873AC3FC0858623C49100F6&SignatureValue=57D5C23FB873AC3FC0858623C49100F6&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=sysoevaolga@rambler.ru&Fee=2.690000&Shp_days=30&Shp_id=851864213&Shp_prev=16912",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28243&InvId=28243&crc=4AFF5E05601D1EDB2E881578BDC2F114&SignatureValue=4AFF5E05601D1EDB2E881578BDC2F114&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=shyrpaliza@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=410566780&Shp_prev=16791",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28223&InvId=28223&crc=DF14084A5A34961F4CE7F0E1505AF290&SignatureValue=DF14084A5A34961F4CE7F0E1505AF290&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=gr.gulnar@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=1339033602&Shp_prev=16171",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28226&InvId=28226&crc=C29FC2C573ED9F6805BB68787CED62B3&SignatureValue=C29FC2C573ED9F6805BB68787CED62B3&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=simakovaanatasia74@gmail.com&Fee=2.690000&Shp_days=30&Shp_id=1056079111&Shp_prev=16470",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28222&InvId=28222&crc=A078302493F99A70F2A3BB468083B549&SignatureValue=A078302493F99A70F2A3BB468083B549&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=Lena-19773@yandex.ru&Fee=2.690000&Shp_days=30&Shp_id=1743267397&Shp_prev=16133",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28220&InvId=28220&crc=FAA5734B5274A05741B19DB08BB615FD&SignatureValue=FAA5734B5274A05741B19DB08BB615FD&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=vadimlar2015mail.ru@gmail.com&Fee=2.690000&Shp_days=30&Shp_id=584665166&Shp_prev=16091",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28221&InvId=28221&crc=A1E322BF054A317272FCE4AB57A3DEBB&SignatureValue=A1E322BF054A317272FCE4AB57A3DEBB&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=yana6905@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=342454885&Shp_prev=16092",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28217&InvId=28217&crc=911F5B17217EB20910F845FF3672F1CF&SignatureValue=911F5B17217EB20910F845FF3672F1CF&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=terekhova.e@stlca.ru&Fee=2.690000&Shp_days=30&Shp_id=5582545767&Shp_prev=16061",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28211&InvId=28211&crc=D63A90B027FDF8A88A429A7803BB4401&SignatureValue=D63A90B027FDF8A88A429A7803BB4401&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=anna.touristic@gmail.com&Fee=2.690000&Shp_days=30&Shp_id=1023756055",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28209&InvId=28209&crc=C850BA97D2FE6DDD1406506F4E0E4965&SignatureValue=C850BA97D2FE6DDD1406506F4E0E4965&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=heezer92@gmail.com&Fee=2.690000&Shp_days=30&Shp_id=746304898",
# "out_summ=330.000000&OutSum=330.000000&inv_id=28202&InvId=28202&crc=8D70906FCA2A77FFF61A82DC4F26ADE5&SignatureValue=8D70906FCA2A77FFF61A82DC4F26ADE5&PaymentMethod=BankCard&IncSum=330.000000&IncCurrLabel=BankCardPSR&EMail=vovan_diagnost@mail.ru&Fee=12.880000&Shp_days=180&Shp_id=5335742049",
# "out_summ=69.000000&OutSum=69.000000&inv_id=27878&InvId=27878&crc=54EDA12891279D97F9837AAC97CDA713&SignatureValue=54EDA12891279D97F9837AAC97CDA713&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=ksouishh@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=1388473719",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28197&InvId=28197&crc=DF0650297F49EF409887EC85B4091668&SignatureValue=DF0650297F49EF409887EC85B4091668&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=qwnllzz@gmail.com&Fee=2.690000&Shp_days=30&Shp_id=807961823",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28192&InvId=28192&crc=F0B4DF0FD5194696FFABA795E68E39C2&SignatureValue=F0B4DF0FD5194696FFABA795E68E39C2&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=mmihalkava9@gmail.com&Fee=2.690000&Shp_days=30&Shp_id=1105694061",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28191&InvId=28191&crc=9F7A83B11D4A9B78E3834B6F9EA185DE&SignatureValue=9F7A83B11D4A9B78E3834B6F9EA185DE&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=YandexPayPSR&EMail=Annloseva@mai.ru&Fee=2.690000&Shp_days=30&Shp_id=597876205",
# "out_summ=580.000000&OutSum=580.000000&inv_id=28190&InvId=28190&crc=E69AE6B467ABD78C21ACBC2C133F1413&SignatureValue=E69AE6B467ABD78C21ACBC2C133F1413&PaymentMethod=BankCard&IncSum=580.000000&IncCurrLabel=BankCardPSR&EMail=shmyreva.m@mail.ru&Fee=22.620000&Shp_days=365&Shp_id=978575304",
# "out_summ=580.000000&OutSum=580.000000&inv_id=28184&InvId=28184&crc=F48DC8CFCF198F49F7AD2DC2DFBB0171&SignatureValue=F48DC8CFCF198F49F7AD2DC2DFBB0171&PaymentMethod=BankCard&IncSum=580.000000&IncCurrLabel=BankCardPSR&EMail=Anastasiyabass@mail.ru&Fee=22.620000&Shp_days=365&Shp_id=1431901599",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28180&InvId=28180&crc=3CCB1F20A9400A9043B6CFE5AF71998F&SignatureValue=3CCB1F20A9400A9043B6CFE5AF71998F&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=Ismagilovaalfia@yandex.ru&Fee=2.690000&Shp_days=30&Shp_id=5217820291",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28177&InvId=28177&crc=21F77F40AD31CEE77CCC69B1F6E4B86D&SignatureValue=21F77F40AD31CEE77CCC69B1F6E4B86D&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=alexandra.prutskova@yandex.ru&Fee=2.690000&Shp_days=30&Shp_id=1493857070",
# "out_summ=580.000000&OutSum=580.000000&inv_id=28178&InvId=28178&crc=1E23977D3286B4CB5A52F2BE097790D3&SignatureValue=1E23977D3286B4CB5A52F2BE097790D3&PaymentMethod=BankCard&IncSum=580.000000&IncCurrLabel=BankCardPSR&EMail=k_annikova@mail.ru&Fee=22.620000&Shp_days=365&Shp_id=232827753",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28173&InvId=28173&crc=F2EE1BAEB4D04F0D0038C3E73AFD2399&SignatureValue=F2EE1BAEB4D04F0D0038C3E73AFD2399&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=YandexPayPSR&EMail=Yulika817@yandex.ru&Fee=2.690000&Shp_days=30&Shp_id=331695818",
# "out_summ=330.000000&OutSum=330.000000&inv_id=28167&InvId=28167&crc=AFB204A841051C084B9FE7EB83EC7640&SignatureValue=AFB204A841051C084B9FE7EB83EC7640&PaymentMethod=BankCard&IncSum=330.000000&IncCurrLabel=BankCardPSR&EMail=pyshinkova04@mail.ru&Fee=12.880000&Shp_days=180&Shp_id=1983171637",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28169&InvId=28169&crc=8FF8A599F58436B27741922F4F9E4832&SignatureValue=8FF8A599F58436B27741922F4F9E4832&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=YandexPayPSR&EMail=lolittalolalo@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=1801633917",
# "out_summ=580.000000&OutSum=580.000000&inv_id=28166&InvId=28166&crc=A147C1C874B2A4ECB152F74F1DE2EB75&SignatureValue=A147C1C874B2A4ECB152F74F1DE2EB75&PaymentMethod=BankCard&IncSum=580.000000&IncCurrLabel=BankCardPSR&EMail=Sm.milla@yandex.ru&Fee=22.620000&Shp_days=365&Shp_id=1127460441",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28164&InvId=28164&crc=05CB9F075CB255697CC11ABE89A12918&SignatureValue=05CB9F075CB255697CC11ABE89A12918&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=postnikova2008@yandex.ru&Fee=2.690000&Shp_days=30&Shp_id=203118993",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28163&InvId=28163&crc=1D1B57AE38A5945D620ACD24A932F20B&SignatureValue=1D1B57AE38A5945D620ACD24A932F20B&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=ryabchenokn@bk.ru&Fee=2.690000&Shp_days=30&Shp_id=482103534",
# "out_summ=330.000000&OutSum=330.000000&inv_id=28157&InvId=28157&crc=B7F3A1E42798068F17DFC28D25AA3ADE&SignatureValue=B7F3A1E42798068F17DFC28D25AA3ADE&PaymentMethod=BankCard&IncSum=330.000000&IncCurrLabel=BankCardPSR&EMail=velyaevapolina@mail.com&Fee=12.880000&Shp_days=180&Shp_id=865999326",
# "out_summ=580.000000&OutSum=580.000000&inv_id=28159&InvId=28159&crc=4B1EEFE2599563CAAD88EDBBD9285934&SignatureValue=4B1EEFE2599563CAAD88EDBBD9285934&PaymentMethod=BankCard&IncSum=580.000000&IncCurrLabel=BankCardPSR&EMail=Vasilnatallia@yandex.ru&Fee=22.620000&Shp_days=365&Shp_id=299489693",
# "out_summ=330.000000&OutSum=330.000000&inv_id=28155&InvId=28155&crc=00FAE559A3AEE8F6AC26E8439F7AABB9&SignatureValue=00FAE559A3AEE8F6AC26E8439F7AABB9&PaymentMethod=BankCard&IncSum=330.000000&IncCurrLabel=YandexPayPSR&EMail=EOVasileva@yandex.ru&Fee=12.880000&Shp_days=180&Shp_id=1150428203",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28153&InvId=28153&crc=93BBE92DEA42EF7C34830542AC4651FC&SignatureValue=93BBE92DEA42EF7C34830542AC4651FC&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=Vera.bondarewa@icloud.com&Fee=2.690000&Shp_days=30&Shp_id=946717430",
# "out_summ=580.000000&OutSum=580.000000&inv_id=28148&InvId=28148&crc=D664DA51E28BD61A09C58827EA44A02A&SignatureValue=D664DA51E28BD61A09C58827EA44A02A&PaymentMethod=BankCard&IncSum=580.000000&IncCurrLabel=BankCardPSR&EMail=Zolotayaolya@mail.ru&Fee=22.620000&Shp_days=365&Shp_id=1294101253",
# "out_summ=330.000000&OutSum=330.000000&inv_id=28147&InvId=28147&crc=98291C8B82E524D786DC394C91D20929&SignatureValue=98291C8B82E524D786DC394C91D20929&PaymentMethod=BankCard&IncSum=330.000000&IncCurrLabel=BankCardPSR&EMail=dashamilor@gmail.com&Fee=12.880000&Shp_days=180&Shp_id=712187",
# "out_summ=330.000000&OutSum=330.000000&inv_id=28145&InvId=28145&crc=E0083E7EE399E6CEA5E840295C6D61FF&SignatureValue=E0083E7EE399E6CEA5E840295C6D61FF&PaymentMethod=BankCard&IncSum=330.000000&IncCurrLabel=BankCardPSR&EMail=rreckoner@mail.ru&Fee=12.880000&Shp_days=180&Shp_id=368560145",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28143&InvId=28143&crc=844A76D71E29B61ABF549A71F51384D4&SignatureValue=844A76D71E29B61ABF549A71F51384D4&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=e_horkova@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=463052775",
# "out_summ=580.000000&OutSum=580.000000&inv_id=28142&InvId=28142&crc=1E6C0434D69290D88F6FA5C8E7ED4774&SignatureValue=1E6C0434D69290D88F6FA5C8E7ED4774&PaymentMethod=BankCard&IncSum=580.000000&IncCurrLabel=BankCardPSR&EMail=Annesal@mail.ru&Fee=22.620000&Shp_days=365&Shp_id=406149032",
# "out_summ=330.000000&OutSum=330.000000&inv_id=28141&InvId=28141&crc=EEFA78ED12E8B44851924E34EE638BCD&SignatureValue=EEFA78ED12E8B44851924E34EE638BCD&PaymentMethod=BankCard&IncSum=330.000000&IncCurrLabel=BankCardPSR&EMail=yu.dobrina@gmail.com&Fee=12.880000&Shp_days=180&Shp_id=260616473",
# "out_summ=69.000000&OutSum=69.000000&inv_id=28138&InvId=28138&crc=E0240F997FE48CF83C563F29C2483A6B&SignatureValue=E0240F997FE48CF83C563F29C2483A6B&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=lenok_min@mail.ru&Fee=2.690000&Shp_days=30&Shp_id=1595831004",
# "out_summ=330.000000&OutSum=330.000000&inv_id=28139&InvId=28139&crc=7F229A61B019EC2F4961AD8D44AB8342&SignatureValue=7F229A61B019EC2F4961AD8D44AB8342&PaymentMethod=BankCard&IncSum=330.000000&IncCurrLabel=BankCardPSR&EMail=Aliyushka-1391@mail.ru&Fee=12.880000&Shp_days=180&Shp_id=741017171",
# "out_summ=330.000000&OutSum=330.000000&inv_id=28137&InvId=28137&crc=268757258A82572BA0155636295F5F58&SignatureValue=268757258A82572BA0155636295F5F58&PaymentMethod=BankCard&IncSum=330.000000&IncCurrLabel=BankCardPSR&EMail=Sofi.shcherbakova.1997@gmail.com&Fee=12.880000&Shp_days=180&Shp_id=909690544",
# "out_summ=330.000000&OutSum=330.000000&inv_id=27536&InvId=27536&crc=C208DD84AABFB27C873B4654154FA3C6&SignatureValue=C208DD84AABFB27C873B4654154FA3C6&PaymentMethod=BankCard&IncSum=330.000000&IncCurrLabel=BankCardPSR&EMail=menovshikova67@mail.ru&Fee=12.880000&Shp_days=180&Shp_id=893174505",
# # "out_summ=69.000000&OutSum=69.000000&inv_id=28130&InvId=28130&crc=28061D36412CE4E21DB90AFF15D777B3&SignatureValue=28061D36412CE4E21DB90AFF15D777B3&PaymentMethod=BankCard&IncSum=69.000000&IncCurrLabel=BankCardPSR&EMail=dariaturilina@gmail.com&Fee=2.690000&Shp_days=30&Shp_id=336502051"
# # ]
# data=[]
# import requests
# data_curr={}
# for elem in lists:
#     elem=elem.split("&")
#     for j in elem:
#         j=j.split("=")
#         data_curr[j[0]]=j[1]
#     data.append(data_curr)
#     data_curr={}
# print(data)


# import datetime
# date=datetime.datetime.now().date()
# # for data1 in data:
# #     request1=requests.post("http://195.2.79.3:443/get_payment",data=data1)
# #     print(request1.text)
# from databaseInteraction import *
# add_web_source(title="test",code=1111111,price=0,date=date,
#         type="канал")

# session=sessionmaker(engine)()
# today=datetime.now().date()
# payments1=session.query(SuccessPayment).filter_by(payment_date=today).all()
# lists1=[]
# for payment in payments1:
#     if not payment.type_of_payment=="TRY REC":
#         user=session.query(User).filter_by(TelegramID=payment.telegram_id).update({"IsActiveSub":1,"SubscrType_ID":3})
# session.commit()