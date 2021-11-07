import habits
from datetime import datetime, timedelta
import time
from bot_options import dp, headers
from pytimeparse.timeparse import timeparse
import requests
import copy

class Notificator:
    def __init__(self):
        pass

    def start(self):
        while True:
            r = requests.get('https://faithback.herokuapp.com/api/users/', cookies=headers)
            for user in r.json():
                name = user['login']
                user_id = user['id']
                removed_ids = []
                added_obj = []
                for habit in user['habit_clusters'][0]['habits']:
                    obj_time =  datetime.strptime(habit['call_time'],  '%Y-%m-%d %H:%M:%S')
                    habit_delta = timeparse(habit['call_delay'])
                    if obj_time < datetime.now():
                        removed_ids.append(habit['id'])
                        if habit_delta == timedelta(weeks=1) or habit_delta == timedelta(days=1):
                            new_obj = copy.deepcopy(habit)
                            new_obj['call_time'] = str(obj_time + habit_delta)
                            added_obj.append(new_obj)
                            #send message here

                url = 'https://faithback.herokuapp.com/api/habbit/{}'
                for user_id in removed_ids:
                    requests.delete(
                        url.format(user_id),
                        cookies=headers
                    )
                for obj in added_obj:
                    requests.post(
                        'https://faithback.herokuapp.com/api/users/{}/clusters/habits/'.format(name), json={
                            "name": added_obj.name,
                            "text": added_obj.text,
                            "call_time": added_obj.call_time,
                            "call_delay": added_obj.call_delay,
                        },
                        cookies=headers
                    )
            time.sleep(100)
                    