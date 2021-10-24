from user import User
from habits import Habit, HabitsProgress, HabitCollection
from cluster_strategy import ClusterStrategy

class LifeSphereCluster():
    def __init__(self, life_sphere_name: str, habit_collection: HabitCollection):
        self.life_sphere_name_ = life_sphere_name
        self.habit_collection_ = habit_collection
        self.strategy_ = ClusterStrategy()
        self.progress_ = HabitsProgress()

    def get_progress(self):
        return self.progress_

    def get_life_sphere_name(self):
        return self.life_sphere_name_

    def add_habbits(self, habbits_count):
        assert habbits_count >= 0

        new_habits_count = 0
        cluster_habits = self.habit_collection_.get_habits()
        for i in range(len(cluster_habits)):
            is_new = not self.progress_.has_habit(cluster_habits[i])
            is_acceptable = self.strategy_.accepts_habit(cluster_habits[i])
            if not (is_acceptable and is_new):
                continue

            is_accepted_by_user = True # ask user
            if not is_accepted_by_user:
                continue

            new_habits_count += 1
            self.progress_.add_habit(Habbit(cluster_habits[i]))
            if new_habbits_count == habbits_count:
                break
            
        return new_habbits_count

    def remove_habits(self, habbits_count):
        assert habbits_count >= 0
        assert habbits_count <= self.progress_.get_habits_count()

        remove_habits_count = 0
        cluster_habits = self.progress_.get_habits()
        for habit_name in cluster_habbits:
            is_blocked_by_user = False #ask user
            if is_blocked_by_user:
                continue

            self.remove_habit(habit_name)
            remove_habits_count += 1
            if remove_habits_count == habbits_count:
                break

        return remove_habits_count
