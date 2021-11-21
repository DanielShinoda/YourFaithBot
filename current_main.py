from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import requests
import keyboards
import habits
import threading
from datetime import datetime, timedelta
from bot_options import bot, dp, headers
import aiogram.utils.markdown as md
from database_adding import add_new_user_to_users, add_user_in_db, users
from states import HabitStates, SettingsState, DeleteState
import timetable
from notificator import Notificator
import asyncio


def read_database_users():
    #  Log: check code from database
    r = requests.get('https://faithback.herokuapp.com/api/users/', cookies=headers)
    assert r.status_code == 200
    return r.json()


database_list = read_database_users()
for db_user in database_list:
    add_new_user_to_users(db_user)


ntf = Notificator()
#  Log: smth to check threading
threading.Thread(target=ntf.start, daemon=True).start()


@dp.message_handler(commands="start")
async def start_handler(event: types.Message):
    #  Log: function entry
    user_name = event.from_user.username
    #  Log: Check if user in database
    add_user_in_db(user_name, event.from_user.id)

    await event.answer(
        "Привет, я Octopus🐙, у меня много лапок и ими всеми я хочу тебе помочь!\n"
        "Вместе со мной ты сможешь построить режим дня "
        "и не забывать о важных событиях\nСперва настрой время, нажав Настройки",
        reply_markup=keyboards.get_main_menu_keyboard()
    )


@dp.message_handler(Text(equals="Настройки"))
async def settings_handler(event: types.Message):
    #  Log: function entry
    user_name = event.from_user.username
    #  Log: Check if user in database
    add_user_in_db(user_name, event.from_user.id)

    await SettingsState.call_time.set()

    await event.reply(
        "Чтобы напоминать тебе о делах вовремя мне нужно "
        "знать твой часовой пояс, напиши его в формате +/-**:** UTC",
        reply_markup=keyboards.get_temporary_keyboard()
    )


@dp.message_handler(state=SettingsState.call_time)
async def process_settings_time(event: types.Message, state: FSMContext):
    #  Log: function entry
    if event.text == "Вернуться в меню":
        await state.finish()
        #  Log: bot sends message
        await event.answer(
            "Выход в главное меню!",
            reply_markup=keyboards.get_main_menu_keyboard()
        )
        return
    #  Log: check code from database
    requests.post(
        'https://faithback.herokuapp.com/api/users/{}/'.format(event.from_user.username), json={
            "time_shift": event.text,
        },
        cookies=headers
    )

    await state.finish()
    #  Log: bot sends message
    await event.answer(
        "Запомнил!",
        reply_markup=keyboards.get_main_menu_keyboard()
    )


@dp.message_handler(Text(equals="Добавить"))
async def add_habit_handler(event: types.Message):
    #  Log: function entry
    user_name = event.from_user.username

    add_user_in_db(user_name, event.from_user.id)

    await HabitStates.name.set()
    #  Log: bot sends message
    await event.reply(
        "Введи название привычки",
        reply_markup=keyboards.get_temporary_keyboard()
    )


@dp.message_handler(state=HabitStates.name)
async def process_habit_name(event: types.Message, state: FSMContext):
    #  Log: function entry
    if event.text == "Вернуться в меню":
        await state.finish()
        #  Log: bot sends message
        await event.answer(
            "Выход в главное меню!",
            reply_markup=keyboards.get_main_menu_keyboard()
        )
        return

    async with state.proxy() as data:
        data['name'] = event.text
    #  Log: bot sends message
    await event.answer(
        "Введи, что мне прислать тебе, когда придёт время",
        reply_markup=keyboards.get_temporary_keyboard()
    )

    await HabitStates.next()


@dp.message_handler(state=HabitStates.text)
async def process_habit_text(event: types.Message, state: FSMContext):
    #  Log: function entry
    if event.text == "Вернуться в меню":
        await state.finish()
        #  Log: bot sends message
        await event.answer(
            "Выход в главное меню!",
            reply_markup=keyboards.get_main_menu_keyboard()
        )
        return

    async with state.proxy() as data:
        data['text'] = event.text
    #  Log: bot sends message
    await event.answer(
        "Теперь выбери дату и время, когда ты хочешь, чтобы я тебе напомнил\n"
        "Если ты хочешь, чтобы напоминалка повторялась, введи ближайшую дату, когда мне надо напомнить\n"
        "Формат: Jun 1 2005 1:33PM",
        reply_markup=keyboards.get_temporary_keyboard()
    )

    await HabitStates.next()


@dp.message_handler(state=HabitStates.call_time)
async def process_habit_call_time(event: types.Message, state: FSMContext):
    #  Log: function entry
    if event.text == "Вернуться в меню":
        await state.finish()
        #  Log: bot sends message
        await event.answer(
            "Выход в главное меню!",
            reply_markup=keyboards.get_main_menu_keyboard()
        )
        return

    try:
        datetime.strptime(event.text, '%b %d %Y %I:%M%p')
    except ValueError:
        #  Log: bot sends message
        await bot.send_message(chat_id=event.from_user.id, text="Пожалуйста, введи дату в корректном формате.")
        return

    async with state.proxy() as data:
        data['call_time'] = event.text
    #  Log: bot sends message
    await event.answer(
        "Хочешь сделать это событие регулярным?",
        reply_markup=keyboards.get_call_delay_keyboard()
    )

    await HabitStates.next()


@dp.message_handler(state=HabitStates.call_delay)
async def process_habit_name(event: types.Message, state: FSMContext):
    #  Log: function entry
    if event.text == "Нет":
        # Нам не нужна регулярность, один раз повторяется.
        async with state.proxy() as data:
            new_habit = habits.Habit(
                habits.HabitOptions(
                    name=data['name'],
                    text=data['text'],
                    call_time=datetime.strptime(data['call_time'], '%b %d %Y %I:%M%p'),
                    call_delay=timedelta(),
                    user=users[event.from_user.id]
                )
            )

            users[event.from_user.id].add_habits("habits", [new_habit])
            #  Log: check code from database
            requests.post(
                'https://faithback.herokuapp.com/api/users/{}/clusters/habits/'.format(event.from_user.username), json={
                    "name": new_habit.options_.name,
                    "text": new_habit.options_.text,
                    "call_time": str(new_habit.options_.call_time),
                    "call_delay": str(new_habit.options_.call_delay),
                },
                cookies=headers
            )

            temp = "Добавил привычку:\n" + \
                   "Название привычки: {}\n".format(md.bold(data['name'])) + \
                   "Буду писать тебе: {}\n".format(data['text']) + \
                   "Ближайшее напоминание: {}\n".format(data['call_time'])

            await state.finish()
            #  Log: bot sends message
            await event.answer(
                temp,
                reply_markup=keyboards.get_main_menu_keyboard()
            )
        return
    #  Log: bot sends message
    await event.answer(
        "Как часто напоминать?",
        reply_markup=keyboards.get_call_delay_pick_keyboard()
    )

    await HabitStates.next()


@dp.message_handler(state=HabitStates.call_delay_pick)
async def process_habit_call_delay_pick(event: types.Message, state: FSMContext):
    #  Log: function entry
    async with state.proxy() as data:
        if event.text == "Каждый день":
            new_habit = habits.Habit(
                habits.HabitOptions(
                    name=data['name'],
                    text=data['text'],
                    call_time=datetime.strptime(data['call_time'], '%b %d %Y %I:%M%p'),
                    call_delay=timedelta(days=1),
                    user=users[event.from_user.id]
                )
            )

        if event.text == "Каждую неделю":
            new_habit = habits.Habit(
                habits.HabitOptions(
                    name=data['name'],
                    text=data['text'],
                    call_time=datetime.strptime(data['call_time'], '%b %d %Y %I:%M%p'),
                    call_delay=timedelta(weeks=1),
                    user=users[event.from_user.id]
                )
            )

        users[event.from_user.id].add_habits("habits", [new_habit])
        #  Log: check code from database
        requests.post(
            'https://faithback.herokuapp.com/api/users/{}/clusters/habits/'.format(event.from_user.username), json={
                "name": new_habit.options_.name,
                "text": new_habit.options_.text,
                "call_time": str(new_habit.options_.call_time),
                "call_delay": str(new_habit.options_.call_delay),
            },
            cookies=headers
        )

        temp = "Добавил привычку:\n" + \
               "Название привычки: {}\n".format(md.bold(data['name'])) + \
               "Буду писать тебе: {}\n".format(data['text']) + \
               "Ближайшее напоминание: {}\n".format(data['call_time']) + \
               "Частота напоминания: {}".format(event.text)
        #  Log: bot sends message
        await event.answer(
            temp,
            reply_markup=keyboards.get_main_menu_keyboard()
        )
    await state.finish()


@dp.message_handler(Text(equals="Удалить"))
async def remove_habit_handler(event: types.Message):
    #  Log: function entry
    #  Log: check code from database
    r = requests.get(
        'https://faithback.herokuapp.com/api/users/{}/'.format(event.from_user.username),
        cookies=headers
    )

    if len(r.json()['habit_clusters'][0]['habits']) == 0:
        #  Log: bot sends message
        await bot.send_message(chat_id=event.from_user.id, text="Для начала добавь привычку. Список привычек пуст!")
        return

    cnt = 1
    send_habits = ""

    for habit in r.json()['habit_clusters'][0]['habits']:
        send_habits += str(cnt) + ") " + habit['name'] + "\n"
        cnt += 1

    await DeleteState.delete_habit.set()
    #  Log: bot sends message
    await event.reply(
        "Я пронумеровал список всех твоих событий, отправь номер того, которое надо удалить:\n" + send_habits,
        reply_markup=keyboards.get_temporary_keyboard()
    )
    #  Log: check code from database
    r = requests.get(
        'https://faithback.herokuapp.com/api/users/{}/'.format(event.from_user.username),
        cookies=headers
    )


@dp.message_handler(state=DeleteState.delete_habit)
async def delete_habit(event: types.Message, state: FSMContext):
    #  Log: function entry

    if event.text == "Вернуться в меню":
        await state.finish()
        #  Log: bot sends message
        await event.answer(
            "Выход в главное меню!",
            reply_markup=keyboards.get_main_menu_keyboard()
        )
        return
    #  Log: check code from database
    r = requests.get(
        'https://faithback.herokuapp.com/api/users/{}/'.format(event.from_user.username),
        cookies=headers
    )

    allowed = {str(i + 1) for i in range(len(r.json()['habit_clusters'][0]['habits']))}

    if event.text not in allowed:
        #  Log: bot sends message
        await bot.send_message(chat_id=event.from_user.id, text="Пожалуйста, введи корректное число!")
        return

    url = 'https://faithback.herokuapp.com/api/habbit/{}'
    #  Log: check code from database
    requests.delete(
        url.format(r.json()['habit_clusters'][0]['habits'][int(event.text) - 1]['id']),
        cookies=headers
    )
    #  Log: bot sends message
    await event.answer(
        "Готово!",
        reply_markup=keyboards.get_main_menu_keyboard()
    )

    await state.finish()


@dp.message_handler(Text(equals="Режим"))
async def mode_handler(event: types.Message):
    #  Log: function entry
    new_tt = timetable.TimeTable(event.from_user.username)
    tt = await new_tt.get_week_timetable()

    text_to_send = ""

    for day, names in tt.items():
        text_to_send += day + ": " + "".join((e + ", ") for e in names)
        text_to_send = text_to_send[:-2] + "\n"
    #  Log: bot sends message
    await bot.send_message(chat_id=event.from_user.id, text=text_to_send)


if __name__ == '__main__':
    executor.start_polling(dp)
