import telebot
import config
import functions
from horoscopeusr import ChUserInfo
TOKEN=config.TOKEN
bot = telebot.TeleBot(TOKEN, parse_mode=None)
def send_horo(txt,photo,id,is_file_exists):
    try: 
        
        if is_file_exists==True: 
            bot.send_photo(id,photo=photo)
            bot.send_message(id,txt,parse_mode="html")
        else:
            bot.send_message(id,txt,parse_mode="html")
    except Exception as err:
        if 'error_code' not in vars(err).keys():
            return 0

        if err.error_code==429:

            send_horo(txt,photo,id,is_file_exists)
        else:
            users=functions.GetUsers(inpTelegramID=str(id),)
            name=users[0]["name"]
            ChUserInfo(inpValue=0,inpTelegramID=str(id),inpFieldName="IsActiveBot" )