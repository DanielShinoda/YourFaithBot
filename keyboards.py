import json
from aiogram import types

with open("configs/ui_config.json", "r", encoding='utf_8') as read_file:
    ui_config = json.load(read_file)

with open("configs/dialogue_config.json", "r", encoding='utf_8') as read_file:
    dialogue_config = json.load(read_file)

with open("configs/ml_config.json", "r", encoding='utf_8') as read_file:
    ml_config = json.load(read_file)


def get_main_menu_keyboard():
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton("Настройки"),
            types.KeyboardButton("Добавить"),
            types.KeyboardButton("Удалить"),
            types.KeyboardButton("Режим")
    )


def get_temporary_keyboard():
    return types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        types.KeyboardButton("Вернуться в меню")
    )
