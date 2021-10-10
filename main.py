import json
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from random import randint
from aiogram.utils import executor
import requests


BOT_TOKEN = "2032324784:AAGtOWAHaLCnlQHIhwhBLQr4jDKrujOvPI8"

with open("configs/ui_config.json", "r", encoding='utf_8') as read_file:
    ui_config = json.load(read_file)

with open("configs/dialogue_config.json", "r", encoding='utf_8') as read_file:
    dialogue_config = json.load(read_file)

with open("configs/ml_config.json", "r", encoding='utf_8') as read_file:
    ml_config = json.load(read_file)


def get_ind(arr):
    return randint(0, len(arr) - 1)


bot = Bot(token=BOT_TOKEN)


class Form(StatesGroup):
    mood = State()  # Получение настроения


storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.add(*[ui_config['button_names']['check_in'],
                         ui_config['button_names']['statistics'],
                         ui_config['button_names']['help']])

analyse_keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
analyse_keyboard_markup.add(*['😁', '🙂', '😐', '😡'])


async def start_handler(event: types.Message):
    user_name = event.from_user.username
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

    await event.answer(
        dialogue_config['hello_phrase'][0].format(
            event.from_user.get_mention(as_html=True)),
        parse_mode=types.ParseMode.HTML, reply_markup=main_menu_keyboard
    )


# При нажатии на кнопку Помощь
@dp.message_handler(Text(equals=ui_config['button_names']['help']))
async def help_handler(message: types.Message):
    await message.reply("/start - начало бота, инициализация юзера в базе данных")


# При нажатии на кнопку Анализ
@dp.message_handler(Text(equals=ui_config['button_names']['check_in']))
async def analyse_handler(message: types.Message):
    await message.answer(
        'Опиши своё состояние смайликом или текстом',
        reply_markup=analyse_keyboard_markup
    )
    await Form.mood.set()


# Запись в базу данных настроения
@dp.message_handler(state=Form.mood)
async def process_name(event: types.Message, state: FSMContext):
    user_name = event.from_user.username
    r = requests.get('https://faithback.herokuapp.com/api/users/')
    print(r)
    user = -1
    for i in r.json():
        if i['login'] == user_name:
            user = i['id']
            break
    if user > 0:
        requests.post('https://faithback.herokuapp.com/api/mood/',
                      json={"mood": event.text, "user": user})

    await event.reply(
        dialogue_config["bye_phrase"][get_ind(dialogue_config["bye_phrase"])],
        reply_markup=main_menu_keyboard
    )
    await state.finish()


dp.register_message_handler(start_handler, commands={"start"})


if __name__ == '__main__':
    executor.start_polling(dp)
