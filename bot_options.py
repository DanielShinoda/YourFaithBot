from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token="2032324784:AAGtOWAHaLCnlQHIhwhBLQr4jDKrujOvPI8", parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
headers = {"api_token": "ca1f659914af8a0c261f0d0ff3aaa5e86a6d955b"}
