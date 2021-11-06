import habits


class LifeSphereCluster:
    def __init__(self, life_sphere_name: str, habit_collection):
        self.life_sphere_name_ = life_sphere_name
        self.habit_collection_ = habit_collection
        self.progress_ = habits.HabitsProgress()

    def get_progress(self):
        return self.progress_

    def get_life_sphere_name(self):
        return self.life_sphere_name_

    def add_habits(self, new_habits):
        for habit in new_habits:
            self.progress_.add_habit(habit)

    def remove_habits(self, habits_names):
        for name in habits_names:
            self.progress_.remove_habit(name)
