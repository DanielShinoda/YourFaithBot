from aiogram.dispatcher.filters.state import State, StatesGroup


class HabitStates(StatesGroup):
    name = State()  # Название привычки
    text = State()  # Текст
    call_time = State()  # Время напоминания
    call_delay = State()  # Частота напоминаний
    call_delay_pick = State()  # Выбор


class SettingsState(StatesGroup):
    call_time = State()  # Название привычки


class DeleteState(StatesGroup):
    delete_habit = State()  # Удаление привычки
