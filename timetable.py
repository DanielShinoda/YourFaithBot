import habits
from datetime import datetime, timedelta
from bot_options import dp, headers
from pytimeparse.timeparse import timeparse
import requests


class TimeTable:
    def __init__(self, username):
        self.username = username

    async def get_week_timetable(self):
        r = requests.get(
            'https://faithback.herokuapp.com/api/users/{}/'.format(self.username),
            cookies=headers
        )

        days_of_week = [
            'Понедельник',
            'Вторник',
            'Среда',
            'Четверг',
            'Пятница',
            'Суббота',
            'Воскресение'
        ]

        user_timetable = {
            'Понедельник': list(),
            'Вторник': list(),
            'Среда': list(),
            'Четверг': list(),
            'Пятница': list(),
            'Суббота': list(),
            'Воскресение': list()
        }

        current_time = datetime.now()
        week_time = current_time - timedelta(days=current_time.weekday())

        for habit in r.json()['habit_clusters'][0]['habits']:
            habit_start = datetime.strptime(habit['call_time'],  '%Y-%m-%d %H:%M:%S')
            habit_delta = timeparse(habit['call_delay'])

            if habit_delta == 86400:
                for day in user_timetable:
                    user_timetable[day].append(habit['name'])

            elif habit_delta == 604800:
                habit_day = habit_start.weekday()
                user_timetable[days_of_week[habit_day]].append(habit['name'])

            elif habit_delta == 0:
                if habit_start >= week_time and habit_start <= week_time + timedelta(weeks=1):
                    habit_day = habit_start.weekday()
                    user_timetable[days_of_week[habit_day]].append(habit['name'])
            else:
                user_timetable = {'WrongFormattedDeltas': 'Error'}

        return user_timetable
