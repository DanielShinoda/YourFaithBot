import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from random import randint
import requests

BOT_TOKEN = "2032324784:AAGtOWAHaLCnlQHIhwhBLQr4jDKrujOvPI8"
with open("config.json", "r", encoding='utf_8') as read_file:
    data = json.load(read_file)


def get_ind(arr):
    return randint(0, len(arr) - 1)


async def main():
    bot = Bot(token=BOT_TOKEN)

    try:
        dp = Dispatcher(bot=bot)

        async def start_handler(event: types.Message):

            requests.post('https://faithback.herokuapp.com/api/users/',
                          json={"login": event.from_user.get_mention()})
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*data['buttons'])
            await event.answer(
                data['hello_phrase'][0].format(
                    event.from_user.get_mention(as_html=True)),
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard
            )

        async def continue_handler(event: types.Message):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*data['buttons'])
            await event.answer(
                data['hello_phrase'][get_ind(data['hello_phrase'])].format(
                    event.from_user.get_mention(as_html=True)),
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard
            )

        async def get_mood_handler(event: types.Message):
            await event.answer(
                data['fun_advice'],
                parse_mode=types.ParseMode.HTML, disable_web_page_preview=True
            )

        @dp.message_handler(Text(equals=data["buttons"][2]))
        async def help_handler(message: types.Message):
            await message.reply("/advice - получить совет\n/start - начало бота, инициализация юзера в базе данных\n"
                                "\n/continue - воскрешение бота после отключения сервера")

        @dp.message_handler(Text(equals=data["buttons"][0]))
        async def analyse_handler(message: types.Message):
            await message.reply(data["analyse"][get_ind(data["analyse"])])

        dp.register_message_handler(start_handler, commands={"start"})
        dp.register_message_handler(continue_handler, commands={"continue"})
        dp.register_message_handler(get_mood_handler, commands={"advice"})
        await dp.start_polling()
    finally:
        await bot.close()

asyncio.run(main())
