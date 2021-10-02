import asyncio
import json
from aiogram import Bot, Dispatcher, types
from random import randint

BOT_TOKEN = "2032324784:AAGtOWAHaLCnlQHIhwhBLQr4jDKrujOvPI8"
with open("config.json", "r", encoding='utf_8') as read_file:
    data = json.load(read_file)


async def start_handler(event: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [data["analyse"], data["check"], data["help"], data["error"]]
    keyboard.add(*buttons)
    await event.answer(
        data['hello_phrase'][randint(0, len(data['hello_phrase']) - 1)].format(event.from_user.get_mention(as_html=True)),
        parse_mode=types.ParseMode.HTML, reply_markup=keyboard
    )


async def get_mood_handler(event: types.Message):
    await event.answer(
        data['fun_advice'],
        parse_mode=types.ParseMode.HTML, disable_web_page_preview=True
    )


async def help_handler(event: types.Message):
    await event.answer(
        f"/advice - получить совет\n"
        f"/start, /restart - начало/перезапуск бота\n",
        parse_mode=types.ParseMode.HTML
    )


async def main():
    bot = Bot(token=BOT_TOKEN)

    try:
        dispatcher = Dispatcher(bot=bot)
        dispatcher.register_message_handler(start_handler, commands={"start", "restart"})
        dispatcher.register_message_handler(get_mood_handler, commands={"advice"})
        await dispatcher.start_polling()
    finally:
        await bot.close()

asyncio.run(main())
