from user import User
from habits import Habit, HabitsProgress, HabitCollection
from cluster_strategy import ClusterStrategy, ClusterStrategyOptions


class LifeSphereCluster:
    def __init__(self, life_sphere_name: str, habit_collection: HabitCollection):
        self.life_sphere_name_ = life_sphere_name
        self.habit_collection_ = habit_collection
        self.strategy_ = ClusterStrategy(ClusterStrategyOptions(0))
        self.progress_ = HabitsProgress()

    def get_progress(self):
        return self.progress_

    def get_life_sphere_name(self):
        return self.life_sphere_name_

    def add_habits(self, habits_count):
        assert habits_count >= 0

        new_habits_count = 0
        cluster_habits = self.habit_collection_.get_habits()
        for i in range(len(cluster_habits)):
            is_new = not self.progress_.has_habit(cluster_habits[i])
            is_acceptable = self.strategy_.accepts_habit(cluster_habits[i])
            if not (is_acceptable and is_new):
                continue

            is_accepted_by_user = True  # ask user
            if not is_accepted_by_user:
                continue

            new_habits_count += 1
            self.progress_.add_habit(Habit(cluster_habits[i]))
            if new_habits_count == habits_count:
                break
            
        return new_habits_count

    def remove_habits(self, habits_count):
        assert habits_count >= 0
        assert habits_count <= self.progress_.get_habits_count()

        remove_habits_count = 0
        cluster_habits = self.progress_.get_habits()
        for habit_name in cluster_habits:
            is_blocked_by_user = False  # ask user
            if is_blocked_by_user:
                continue

            self.remove_habits(habit_name)
            remove_habits_count += 1
            if remove_habits_count == habits_count:
                break

        return remove_habits_count
