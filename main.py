import json
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from random import randint
from aiogram.utils import executor
import requests
import keyboards
import emotion_model
import user
import habits
from typing import NamedTuple
import life_sphere_cluster

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
    emoji = State()  # Смайлик
    description = State()  # текст
    mood = State()  # Получение настроения


storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

emoji = ''

# load habit collections
habit_collections = {
    'sport': habits.HabitCollection('sport'),
    'meditation': habits.HabitCollection('meditation'),
    'sleep': habits.HabitCollection('sleep'),
    'mood': habits.HabitCollection('mood')
    }

for name in habit_collections:
    habit_collections[name].init_from_file("./configs/" + name + "_config.json")

# load users
users = []


def read_database_users():
    r = requests.get('https://faithback.herokuapp.com/api/users/')

    assert r.status_code == 200
    return r.json()


database_list = read_database_users()
for database_user in database_list:
    # read them from datatable
    chosen_life_spheres = ["sport", "meditation", "mood"]

    # read user options
    user_options = None

    new_user = user.User(habit_collections, chosen_life_spheres, user_options)
    
    for life_sphere in chosen_life_spheres:
        new_user.add_habits(life_sphere, 1)

    # or read dict from database
    # new_user.set_progress(dict[user.NAME_ID],  dict)

# Global Timer must execute
# for called_user in users:
#    called_user.call_habits()


class NotificationResult(NamedTuple):
    example: int


class Notification:
    def __init__(self, habit: habits.Habit):
        self.options_ = habit.options_

    def draw(self, message: types.Message):
        pass


class MoodNotification(Notification):
    async def draw(self, message: types.Message):
        await analyse(message)


class BasicNotification(Notification):
    async def draw(self, message: types.Message):
        await message.reply(
            self.options_.text,
            reply_markup=keyboards.get_answer_keyboard_markup()
        )


@dp.callback_query_handler(func=lambda c: c.data == 'habitCallResult')
async def process_callback_basic_notification(callback_query: types.CallbackQuery):
    pass


@dp.callback_query_handler(func=lambda c: c.data == 'sport')
async def process_callback_basic_notification(callback_query: types.CallbackQuery):
    pass


async def start_handler(event: types.Message):
    user_name = event.from_user.username
    # Если человек уже есть в базе данных, не нужно добавлять его ещё раз
    if requests.get('https://faithback.herokuapp.com/api/users/{}/'.format(user_name)).status_code != 200:
        requests.post('https://faithback.herokuapp.com/api/users/', json={"login": user_name})

    await event.answer(
        dialogue_config['hello_phrase'][0].format(
            event.from_user.get_mention(as_html=True)),
        parse_mode=types.ParseMode.HTML, reply_markup=keyboards.get_start_keyboard()
    )


# При нажатии на кнопку Помощь
@dp.message_handler(Text(equals=ui_config['button_names']['help']))
async def help_handler(message: types.Message):
    await message.reply("/start - начало бота, инициализация юзера в базе данных")


async def analyse(message: types.Message):
    user_name = message.from_user.username
    r = requests.get('https://faithback.herokuapp.com/api/users/{}/'.format(user_name))
    if r.status_code != 200:
        await message.reply('Напишите /start для регистрации')
    else:
        await Form.emoji.set()
        await message.reply(
            'Опиши своё состояние смайликом',
            reply_markup=keyboards.get_analyse_keyboard_markup()
        )


@dp.message_handler(state=Form.emoji)
async def process_emoji(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['emoji'] = event.text
    print('emoji:', data['emoji'])
    await event.reply('Вкратце опиши своё настроение')
    await Form.next()


@dp.message_handler(state=Form.description)
async def process_text(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = event.text
    print('text:', data['description'])
    await process_mood(event, state)


# Запись в базу данных настроения
@dp.message_handler(state=Form.mood)
async def process_mood(event: types.Message, state: FSMContext):
    user_name = event.from_user.username
    r = requests.get('https://faithback.herokuapp.com/api/users/{}/'.format(user_name))

    async with state.proxy() as data:
        requests.post(
            'https://faithback.herokuapp.com/api/mood/',
            json={
                "mood": keyboards.transform_emoji(data['emoji']),
                "user": r.json()['id'],
                "description": data['description'],
                "description_tone": dict(emotion_model.get_emotion_array(data['description']))
            }
        )
    await state.finish()


dp.register_message_handler(start_handler, commands={"start"})


if __name__ == '__main__':
    executor.start_polling(dp)
