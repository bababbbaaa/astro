from controller import *
import aiogram
bot.set_my_commands([


    aiogram.types.bot_command.BotCommand(command="send",description="Получить гороскоп сейчас"),
    aiogram.types.bot_command.BotCommand(command="gen_user_mes",description="Гороскоп другу"),
    aiogram.types.bot_command.BotCommand(command="subscribe",description="Подписка"),
    aiogram.types.bot_command.BotCommand(command="support",description="Поддержка"),
    aiogram.types.bot_command.BotCommand(command="change",description="Изменить данные"),



])