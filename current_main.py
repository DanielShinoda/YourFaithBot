import json
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import requests
import keyboards
import habits
from datetime import date
from bot_options import bot, dp, storage
import user


class HabitStates(StatesGroup):
    name = State()  # Название привычки
    text = State()  # Текст
    call_time = State()  # Время напоминания
    call_delay = State()  # Частота напоминаний


class SettingsState(StatesGroup):
    call_time = State()  # Название привычки


def add_user_in_db(name, id_):
    if requests.get('https://faithback.herokuapp.com/api/users/{}/'.format(name)).status_code != 200:
        requests.post(
            'https://faithback.herokuapp.com/api/users/', json={
                "login": name,
                "chat_id": id_
            }
        )


# # All users in db
# users = []
#
#
# def read_database_users():
#     r = requests.get('https://faithback.herokuapp.com/api/users/')
#
#     assert r.status_code == 200
#     return r.json()
#
#
# def notify_users(time: date):
#     global users
#
#     for user_ in users:
#         user_.call_habits(time)
#
#
# database_list = read_database_users()
# for database_user in database_list:
#     # read them from datatable
#     chosen_life_spheres = ["habits"]
#
#     habit_collections = {
#         'sport': habits.HabitCollection('sport'),
#         'meditation': habits.HabitCollection('meditation'),
#         'sleep': habits.HabitCollection('sleep'),
#         'mood': habits.HabitCollection('mood'),
#         'habits': habits.HabitCollection('habits')
#     }
#
#     for name in habit_collections:
#         habit_collections[name].init_from_file("./configs/" + name + "_config.json")
#
#     # read user options
#     user_options = user.UserOptions(database_user["chat_id"])
#
#     new_user = user.User(habit_collections, chosen_life_spheres, user_options)
#
#     new_user.set_progress("habits", database_user["habit_clusters"])
#
#     users.append(new_user)


@dp.message_handler(commands="start")
async def start_handler(event: types.Message):
    user_name = event.from_user.username

    add_user_in_db(user_name, event.from_user.id)

    await event.answer(
        "Привет, я Octopus🐙, у меня много лапок и ими всеми я хочу тебе помочь!"
        "Вместе со мной ты сможешь построить режим дня"
        "и не забывать о важных событиях\nСперва настрой время, нажав Настройки",
        reply_markup=keyboards.get_main_menu_keyboard()
    )


@dp.message_handler(Text(equals="Настройки"))
async def settings_handler(event: types.Message):
    user_name = event.from_user.username

    add_user_in_db(user_name, event.from_user.id)

    await SettingsState.call_time.set()

    await event.reply(
        "Чтобы напоминать тебе о делах вовремя мне нужно"
        "знать твой часовой пояс, напиши его в формате +/-**:** UTC",
        reply_markup=keyboards.get_temporary_keyboard()
    )


@dp.message_handler(state=SettingsState.call_time)
async def process_settings_time(event: types.Message, state: FSMContext):
    if event.text == "Вернуться в меню":
        await state.finish()
        await event.answer(
            "Выход в главное меню!",
            reply_markup=keyboards.get_main_menu_keyboard()
        )
        return

    requests.post(
        'https://faithback.herokuapp.com/api/users/', json={
            "login": event.from_user.username,
            "time_shift": event.text
        }
    )

    await state.finish()

    await event.answer(
        "Запомнил!",
        reply_markup=keyboards.get_main_menu_keyboard()
    )


@dp.message_handler(Text(equals="Добавить"))
async def add_habit_handler(event: types.Message):
    pass


@dp.message_handler(Text(equals="Удалить"))
async def remove_habit_handler(event: types.Message):
    pass


@dp.message_handler(Text(equals="Режим"))
async def mode_handler(event: types.Message):
    pass


# # Прописать добавление привычки
# async def add_habit(message: types.Message):
#     user_name = message.from_user.username
#     r = requests.get('https://faithback.herokuapp.com/api/users/{}/'.format(user_name))
#     if r.status_code != 200:
#         await message.reply('Напишите /start для регистрации')
#     else:
#         await HabitForm.emoji.set()
#         await message.reply(
#             'Опиши своё состояние смайликом',
#             reply_markup=keyboards.get_analyse_keyboard_markup()
#         )
#
#
# @dp.message_handler(state=HabitForm.emoji)
# async def process_emoji(event: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['emoji'] = event.text
#     print('emoji:', data['emoji'])
#     await event.reply('Вкратце опиши своё настроение')
#     await HabitForm.next()
#
#
# @dp.message_handler(state=HabitForm.description)
# async def process_text(event: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['description'] = event.text
#     print('text:', data['description'])
#     await process_mood(event, state)
#
#
# # Запись в базу данных настроения
# @dp.message_handler(state=HabitForm.mood)
# async def process_mood(event: types.Message, state: FSMContext):
#     user_name = event.from_user.username
#     r = requests.get('https://faithback.herokuapp.com/api/users/{}/'.format(user_name))
#
#     async with state.proxy() as data:
#         requests.post(
#             'https://faithback.herokuapp.com/api/mood/',
#             json={
#                 "mood": keyboards.transform_emoji(data['emoji']),
#                 "user": r.json()['id'],
#                 "description": data['description'],
#                 "description_tone": dict(emotion_model.get_emotion_array(data['description']))
#             }
#         )
#     await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
