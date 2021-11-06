from dataclasses import dataclass
import life_sphere_cluster
from datetime import timedelta, date
import json
import habits
from bot_options import bot, dp, storage


NAME_ID = "name"
HABITS_ID = "habits"


@dataclass
class UserOptions:
    chat_id: int


class User:
    def __init__(self, habit_collections, chosen_life_spheres, user_options: UserOptions):
        self.life_spheres_ = dict()
        self.user_options_ = user_options

        for life_spheres_name in chosen_life_spheres:

            assert life_spheres_name in habit_collections

            self.life_spheres_[life_spheres_name] = life_sphere_cluster.LifeSphereCluster(
                life_spheres_name,
                habit_collections
            )

    def set_progress(self, life_sphere_name, progress_dict):
        assert life_sphere_name in self.life_spheres_
        assert progress_dict["name"] == life_sphere_name

        self.life_spheres_.clear()

        for habit_dict in progress_dict[HABITS_ID]:
            new_habit = habits.habit_from_dictionary(habit_dict, self)
            self.life_spheres_[life_sphere_name].add_habits(new_habit)

    def call_habits(self, time: date):
        for life_sphere_name in self.life_spheres_:
            cluster = self.life_spheres_[life_sphere_name]
            cluster.get_progress().call_habits(time)

    def add_habits(self, life_sphere_name, num_habits):
        self.life_spheres_[life_sphere_name].add_habits(num_habits)

    def notify(self, text):
        bot.send_message(self.user_options_.chat_id, text)
