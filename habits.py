from dataclasses import dataclass
from datetime import timedelta, date
from user import User
from typing import NamedTuple
import json
import copy
from notifications import MoodNotifiaction, BasicNotifiaction, Notification

@dataclass
class HabitOptions:
    name: str
    text: str
    call_time: date
    call_delay: timedelta
    user: User

def habitFromDictionary(dictionary, user_object):
    habit = Habit((
        dictionary["name"],
        dictionary["text"],
        dictionary["call_time"],
        dictionary["call_delay"],
        user_object
        ))
    return habit

class HabitCallResult(NamedTuple):
    validated: bool

class Habit():
    def __init__(self, habit_object):
        self.options_ = copy.copy(habit_object.options_)

    def __init__(self, options: HabitOptions):
        self.options_ = copy.copy(options)

    def needs_call(self, time: date):
        return time >= self.options_.call_time

    def update_call_time(self, current_time: date, update_to_past: bool):
        pass

    def get_options(self):
        return self.options_

    def call(self):
        self.options_.call_time += self.options_.delay;
        return notify_user_()

    def notify_user_(self):
        new_notification = BasicNotifiaction()

        # temporary fix
        if self.options_.name == "mood_check":
            new_notification = MoodNotifiaction()

        self.options_.user.send_notification(new_notification)
        return HabitCallResult(True)

class HabitCollection():
    def __init__(self, name):
        self.name_ = name
        self.habits_ = []

    def init_from_file(self, file_path):
        with open(file_path, "r", encoding='utf_8') as read_file:
            habits_config = json.load(read_file)
        # read habits_config

    def get_habits():
        return self.habits_

    def __init__(self):
        pass

class HabitsProgress():
    def __init__(self):
        self.habits_ = dict()
        self.validations = dict()

    def add_habit(habit: Habit):
        habit_name = habbit.get_options().name
        self.habits_[habit_name] = habit
        self.validations_[habit_name] = 0

        assert len(self.habits_) == len(self.validations_)

    def remove_habit(habit_name: str):
        self.habits_.pop(habit_name)
        self.validations_.pop(habit_name)

        assert len(self.habits_) == len(self.validations_)

    def has_habit(habit_name: str):
        return habit_name in self.habits_ 

    def call_habits(self, time: date):
        for habit_name in self.habits_:
            habit = self.habits_[habit_name]
            if habit.needs_call(time):
                call_result = habit.call()
                if (call_result.validated):
                    self.validations[habit_name] += 1

    def get_habits_count():
        return len(self.habits_)

    def get_habits():
        return self.habits_

    def clear():
        self.habits_.clear()
        self.validations.clear()
        assert len(self.habits_) == len(self.validations_)
