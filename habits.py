from dataclasses import dataclass
from datetime import timedelta, date
from user import User
import json

@dataclass
class HabitOptions:
    name: str
    text: str
    next_call: date
    delay: timedelta
    user: User

class Habbit():
    def __init__(self, options: HabitOptions):
        self.options_ = options

    def needs_call(self, time: date):
        return time >= self.options_.next_call

    def get_options(self):
        return self.options_

    def call(self):
        self.options_.next_call += self.options_.delay;
        return

class HabbitCollection():
    def __init__(self, name):
        self.name_ = name
        self.habits_ = []

    def init_from_file(self, file_path):
        with open(file_path, "r", encoding='utf_8') as read_file:
            habits_config = json.load(read_file)

        # habits_config

    def __init__(self):
        pass

class LifeSphereCluster():
    def __init__(self):
        pass

class ClusterStrategy():
    def __init__(self):
        pass

    def accepts_habit(self):
        return True

class ClusterProgress():
    def __init__(self):
        self.habits_ = dict()

    def add_habit(habbit: Habbit):
        self.habits_[habbit.get_options().name] = habbit

    def remove_habbit(habbit_name: str):
        if habbit_name in self.habits_:
            del self.habits_[habbit_name]

    def call_habbits(self, time: date):
        for habit_name in self.habits_:
            if self.habits_[habit_name].needs_call(time):
                self.habits_[habit_name].call()
