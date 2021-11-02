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
    call_delay_pick = State()  # Выбор


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

    r = requests.post(
        'https://faithback.herokuapp.com/api/users/'.format(event.from_user.username), json={
            "login": event.from_user.username,
            "chat_id": event.from_user.id,
            "time_shift": event.text
        }
    )

    print(r)

    await state.finish()

    await event.answer(
        "Запомнил!",
        reply_markup=keyboards.get_main_menu_keyboard()
    )


@dp.message_handler(Text(equals="Добавить"))
async def add_habit_handler(event: types.Message):
    user_name = event.from_user.username

    add_user_in_db(user_name, event.from_user.id)

    await HabitStates.name.set()

    await event.reply(
        "Введи название привычки",
        reply_markup=keyboards.get_temporary_keyboard()
    )


@dp.message_handler(state=HabitStates.name)
async def process_habit_name(event: types.Message, state: FSMContext):
    if event.text == "Вернуться в меню":
        await state.finish()
        await event.answer(
            "Выход в главное меню!",
            reply_markup=keyboards.get_main_menu_keyboard()
        )
        return

    async with state.proxy() as data:
        data['name'] = event.text

    await event.answer(
        "Введи, что мне прислать тебе, когда придёт время",
        reply_markup=keyboards.get_temporary_keyboard()
    )

    await HabitStates.next()


@dp.message_handler(state=HabitStates.text)
async def process_habit_text(event: types.Message, state: FSMContext):
    if event.text == "Вернуться в меню":
        await state.finish()
        await event.answer(
            "Выход в главное меню!",
            reply_markup=keyboards.get_main_menu_keyboard()
        )
        return

    async with state.proxy() as data:
        data['text'] = event.text

    await event.answer(
        "Теперь выбери дату и время, когда ты хочешь, чтобы я тебе напомнил\n"
        "Если ты хочешь, чтобы напоминалка повторялась, введи ближайшую дату, когда мне надо напомнить\n"
        "Формат: Jun 1 2005 1:33PM",
        reply_markup=keyboards.get_temporary_keyboard()
    )

    await HabitStates.next()


@dp.message_handler(state=HabitStates.call_time)
async def process_habit_call_time(event: types.Message, state: FSMContext):
    if event.text == "Вернуться в меню":
        await state.finish()
        await event.answer(
            "Выход в главное меню!",
            reply_markup=keyboards.get_main_menu_keyboard()
        )
        return

    async with state.proxy() as data:
        data['call_time'] = event.text

    await event.answer(
        "Хочешь сделать это событие регулярным?",
        reply_markup=keyboards.get_call_delay_keyboard()
    )

    await HabitStates.next()


@dp.message_handler(state=HabitStates.call_delay)
async def process_habit_name(event: types.Message, state: FSMContext):
    if event.text == "Нет":
        await state.finish()

        async with state.proxy() as data:
            pass
            # new_habit = habits.Habit(
            #     habits.HabitOptions(
            #         data['name'],
            #         data['text'],
            #         date(data['call_time']),
            #
            #     )
            # )

        async with state.proxy() as data:
            temp = "Добавил привычку:\n" + \
                   "Название привычки: {}\n".format(data['name']) + \
                   "Буду писать тебе: {}\n".format(data['text']) + \
                   "Ближайшее напоминание: {}\n".format(data['call_time'])
            await event.answer(
                temp,
                reply_markup=keyboards.get_main_menu_keyboard()
            )
        return

    await event.answer(
        "Как часто напоминать?",
        reply_markup=keyboards.get_call_delay_pick_keyboard()
    )

    await HabitStates.next()


@dp.message_handler(state=HabitStates.call_delay_pick)
async def process_habit_call_delay_pick(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # new_habit = habits.Habit(
        #     habits.HabitOptions(
        #         data['name'],
        #         data['text'],
        #         date(data['call_time']),
        #
        #     )
        # )
        temp = "Добавил привычку:\n" + \
               "Название привычки: {}\n".format(data['name']) + \
               "Буду писать тебе: {}\n".format(data['text']) + \
               "Ближайшее напоминание: {}\n".format(data['call_time']) + \
               "Частота напоминания: {}".format(event.text)
        await event.answer(
            temp,
            reply_markup=keyboards.get_main_menu_keyboard()
        )
    await state.finish()


@dp.message_handler(Text(equals="Удалить"))
async def remove_habit_handler(event: types.Message):
    pass


@dp.message_handler(Text(equals="Режим"))
async def mode_handler(event: types.Message):
    pass


if __name__ == '__main__':
    executor.start_polling(dp)
