from notifications import Notification
from life_sphere_cluster import LifeSphereCluster
from datetime import timedelta, date
import json
import habits
from notifications import Notification

NAME_ID = "name"
HABITS_ID = "habits"

class User():
    def __init__(self, habbit_collections, chosen_life_spheres, user_options = None):
        self.life_spheres_ = dict()
        self.user_options_ = user_options

        for life_spheres_name in chosen_life_spheres:
            assert life_spheres_name in habbit_collections
            self.life_spheres_[life_spheres_name] = LifeSphereCluster(name, habbit_collections)

    def set_progress(self, life_sphere_name, progress_dict):
        assert life_sphere_name in self.life_spheres_
        assert progress_dict.name == life_sphere_name

        self.life_spheres_.clear()

        for habit_dict in progress_dict[HABITS_ID]:
            new_habit = habits.habitFromDictionary(habit_dict, self)
            self.life_spheres_.add_habbit(new_habit)

    def send_notification(self, notification: Notification):
        # use user_options to send to precise user
        pass

    def call_habits(self, time: date):
        for life_sphere_name in self.life_spheres_:
            cluster = self.life_spheres_[life_sphere_name]
            cluster.get_progress().call_habits(time)

    def add_habits(self, life_sphere_name, num_habits):
        self.life_spheres_[life_sphere_name].add_habbits(num_habits)
