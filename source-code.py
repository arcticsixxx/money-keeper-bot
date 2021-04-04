import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'BOT TOKEN HERE'

logging.basicConfig(level = logging.INFO)

bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)

def auth(func):

    async def wrapper(message):
        if message['from']['id'] != 483528710:
            return await message.reply ('Accsess Denied', reply = False)
        return await func(message)

    return wrapper

