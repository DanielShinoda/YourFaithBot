import json
from aiogram import types

with open("configs/ui_config.json", "r", encoding='utf_8') as read_file:
    ui_config = json.load(read_file)

with open("configs/dialogue_config.json", "r", encoding='utf_8') as read_file:
    dialogue_config = json.load(read_file)

with open("configs/ml_config.json", "r", encoding='utf_8') as read_file:
    ml_config = json.load(read_file)


def get_main_menu_keyboard():
    main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_keyboard.add(*[ui_config['button_names']['check_in'],
                             ui_config['button_names']['statistics'],
                             ui_config['button_names']['help']]
                           )
    return main_menu_keyboard


def get_analyse_keyboard_markup():
    analyse_keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    analyse_keyboard_markup.add(*['😁', '🙂', '😐', '😫', '😡'])
    return analyse_keyboard_markup


def get_empty_keyboard_markup():
    empty_keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    return empty_keyboard_markup


def get_text_keyboard_markup():
    text_keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    text_keyboard_markup.add(['Да', 'Нет'])
    return text_keyboard_markup


emojis = {
    '😁': 4,
    '🙂': 3,
    '😐': 2,
    '😫': 1,
    '😡': 0
}


def transform_emoji(emoji):
    return emojis[emoji]
