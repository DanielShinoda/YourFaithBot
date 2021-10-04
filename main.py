import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from random import randint
from aiogram.utils import executor
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = "2032324784:AAGtOWAHaLCnlQHIhwhBLQr4jDKrujOvPI8"
with open("config.json", "r", encoding='utf_8') as read_file:
    data = json.load(read_file)


def get_ind(arr):
    return randint(0, len(arr) - 1)


bot = Bot(token=BOT_TOKEN)


class Form(StatesGroup):
    mood = State()  # Получение настроения


storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


async def start_handler(event: types.Message):
    soup = BeautifulSoup(event.from_user.get_mention(as_html=True), 'html.parser')
    user_name = soup.find_all('a')[0].text
    # Если человек уже есть в базе данных, не нужно добавлять его ещё раз
    flag = False
    r = requests.get('https://faithback.herokuapp.com/api/users/')
    for i in r.json():
        if i['login'] == user_name:
            flag = True
            break
    # Если человек не найден в базе данных: добавляем его
    if not flag:
        requests.post('https://faithback.herokuapp.com/api/users/', json={"login": user_name})
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*data['buttons'])
    await event.answer(
        data['hello_phrase'][0].format(
            event.from_user.get_mention(as_html=True)),
        parse_mode=types.ParseMode.HTML, reply_markup=keyboard
    )


# При нажатии на кнопку Помощь
@dp.message_handler(Text(equals=data["buttons"][2]))
async def help_handler(message: types.Message):
    await message.reply("/start - начало бота, инициализация юзера в базе данных")


# При нажатии на кнопку Анализ
@dp.message_handler(Text(equals=data["buttons"][0]))
async def analyse_handler(message: types.Message):
    await Form.mood.set()
    await message.reply(data["analyse"][get_ind(data["analyse"])])


# Запись в базу данных настроения
@dp.message_handler(state=Form.mood)
async def process_name(event: types.Message, state: FSMContext):
    soup = BeautifulSoup(event.from_user.get_mention(as_html=True), 'html.parser')
    user_name = soup.find_all('a')[0].text
    r = requests.get('https://faithback.herokuapp.com/api/users/')
    user = -1
    for i in r.json():
        if i['login'] == user_name:
            user = i['id']
            break
    if user > 0:
        requests.post('https://faithback.herokuapp.com/api/mood/',
                      json={"mood": event.text, "user": user})

    await state.finish()
    await event.reply(data["bye_phrase"][get_ind(data["analyse"])])

dp.register_message_handler(start_handler, commands={"start"})


if __name__ == '__main__':
    executor.start_polling(dp)
