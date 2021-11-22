import logging

from datetime import datetime, date, time

from aiogram import Bot, Dispatcher, executor, types

import sqlite3
from sqlite3 import Error

from db import init_db
from db import add_message
from db import fetchall

API_TOKEN = 'API_TOKEN'

logging.basicConfig(level = logging.INFO)
bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)

sumator = 0
total_list = [] 

def auth(func):
    async def wrapper(message):
        if message['from']['id'] != 483528710:
            return await message.reply ('Accsess Denied', reply = False)
        return await func(message)
    return wrapper

init_db()

def execute_keys():
    '''
    Эта функция вытаскивает ключи price и description для последующего выкидывания в /expenses
    '''
    temporary_bd = fetchall('user_message', ['id', 'user_id', 'price', 'description', 'datee'])
    result_pr = [item['price'] for item in temporary_bd]
    result_de = [value['description'] for value in temporary_bd]
    result_da = [el['datee'] for el in temporary_bd]
    c = []
    c.append(result_pr)
    c.append(result_de)
    c.append(result_da)
    final_res = list(map(" ".join, zip(*c)))
    return final_res

def total_sum():
    today_date = str(datetime.now().strftime('%d %b %Y'))
    today_datee = today_date[::-1]
    new_spisok = execute_keys()
    for elem in new_spisok:
        if str(elem[:-12:-1]) == today_datee:
            sumator += int(elem[:4])
        else:
            if str(elem[:-12:-1]) != today_date:
                sumator = 0
    return sumator

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm Money Keeper Bot! I will help you with controling your money spendings  🙌 😊")
    
@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await message.reply('Availible commands: \n/expenses - Show all of your expenses 💲 \n/start - Short tutorial 🛠 \n/total - Show the total sum of your expenses 💸')

@dp.message_handler(commands=['expenses'])
async def expenses_list(message: types.Message):
    a = execute_keys()
    b = "\n".join(map(str, a))
    await message.reply('Your expenses:' + '\n'+ b)

@dp.message_handler(commands=['total'])
async def total_expenses(message: types.Message):
    total_output = total_sum()
    await message.reply((message.date.strftime('%d %b %Y')) +  '\n' + 'Your total expenses today:' '\n' + str(total_output) + ' RUB.')

@dp.message_handler(content_types = ['text'])
async def is_digit(message: types.Message):
    date_t = message.date
    temp_data = tuple(str(message.text).split())        
    if str(temp_data[0]).isdigit() == True and len(temp_data) == 2:
        add_message(
            user_id = int(message.from_user.id),
            price = int(temp_data[0]),
            description = temp_data[1],
            datee = date_t.strftime("%d %b %Y")
        )
        return await message.reply ('Expense was saved!')
    elif str(temp_data[0]).isdigit() == False or len(temp_data) != 2:
        return await message.reply ('if you want to write down your expense please make the same input like in example.\nExample: 250 "something"')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
