import habits
from datetime import datetime, timedelta
from bot_options import dp, headers
from pytimeparse.timeparse import timeparse

class TimeTable:
    def __init__(self, username):
        self.username = username
    async def getWeekTimetable(self):
        r = requests.get(
            'https://faithback.herokuapp.com/api/users/{}/'.format(username),
            cookies=headers
        )

        daysOfWeek = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресение']
        userTimetable = {'Понедельник':[], 'Вторник':[], 'Среда':[], 'Четверг':[], 'Пятница':[], 'Суббота':[], 'Воскресение':[]}
        currentTime = datetime.now()
        weekTime = currentTime - timedelta(days=currentTime.weekday())

        for habit in r.json()['habit_clusters'][0]['habits']:
            habit_start = datetime.strptime(habit['call_time'], '%b %d %Y %I:%M%p')
            habit_delta = timeparse(habit['call_delay'])

            if habit_delta == timedelta(days=1):
                for day in userTimetable:
                    userTimetable[day].append(habit['name'])
            elif habit_delta == timedelta(weeks=1):
                habit_day = habit_start.weekday()
                userTimetable[daysOfWeek[habit_day]].append(habit['name'])
            elif habit_delta == timedelta():
                if habit_start >= weekTime and habit_start <= weekTime + timedelta(weeks=1):
                    habit_day = habit_start.weekday()
                    userTimetable[daysOfWeek[habit_day]].append(habit['name'])
            else:
                userTimetable = {'WrongFormattedDeltas': 'Error'}
        return userTimetable



        
        


