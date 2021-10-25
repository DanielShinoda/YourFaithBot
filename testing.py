import unittest
import habits
import user
from datetime import timedelta, date
import life_sphere_cluster

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        user_one = user.User()
        habit_one = habits.Habit(("", "", date.fromisoformat('2019-01-01'), timedelta(), user_one))

        self.assertEqual('foo'.upper(), 'FOO')

def habit_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestStringMethods('test_upper'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(habit_suite())
