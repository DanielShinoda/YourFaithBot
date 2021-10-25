import json
from aiogram import types

with open("configs/ui_config.json", "r", encoding='utf_8') as read_file:
    ui_config = json.load(read_file)

with open("configs/dialogue_config.json", "r", encoding='utf_8') as read_file:
    dialogue_config = json.load(read_file)

with open("configs/ml_config.json", "r", encoding='utf_8') as read_file:
    ml_config = json.load(read_file)


def get_start_keyboard():
    start_kb = types.InlineKeyboardMarkup()
    start_kb.add(
        types.InlineKeyboardButton('sport', callback_data='sport'),
        types.InlineKeyboardButton('meditation', callback_data='meditation'),
        types.InlineKeyboardButton('sleep', callback_data='sleep'),
    )
    return start_kb


def get_analyse_keyboard_markup():
    analyse_kb = types.InlineKeyboardMarkup()
    analyse_kb.add(
        types.InlineKeyboardButton('😁', callback_data='😁'),
        types.InlineKeyboardButton('🙂', callback_data='🙂'),
        types.InlineKeyboardButton('😐', callback_data='😐'),
        types.InlineKeyboardButton('😫', callback_data='😫'),
        types.InlineKeyboardButton('😡', callback_data='😡')
    )
    return analyse_kb


def get_answer_keyboard_markup():
    inline_btn_1 = types.InlineKeyboardButton('Да', callback_data='habitCallResult')
    inline_btn_2 = types.InlineKeyboardButton('Нет', callback_data='habitCallResult')
    inline_kb1 = types.InlineKeyboardMarkup().add(inline_btn_1)
    inline_kb1.add(inline_btn_2)
    return inline_kb1


def get_empty_keyboard_markup():
    empty_keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    return empty_keyboard_markup


emojis = {
    '😁': 4,
    '🙂': 3,
    '😐': 2,
    '😫': 1,
    '😡': 0
}


def transform_emoji(emoji):
    return emojis[emoji]
