import habits
from datetime import datetime, timedelta
import time
from bot_options import dp, bot, headers
from pytimeparse.timeparse import timeparse
import requests
import copy
import asyncio
import logging


def log(message, level):
    logging.basicConfig(filename='output.csv',
                        filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG)

    if level.upper() == "DEBUG":
        logging.debug(message)
    if level.upper() == "INFO":
        logging.info(message)
    if level.upper() == "WARNING":
        logging.warning(message)
    if level.upper() == "ERROR":
        logging.error(message)
    if level.upper() == "CRITICAL":
        logging.critical(message)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


class Notificator:
    def __init__(self):
        pass

    def start(self):
        while True:
            log("Function start entry", "INFO")
            log("Check code from database", "INFO")
            r = requests.get('https://faithback.herokuapp.com/api/users/', cookies=headers)
            for user in r.json():
                name = user['login']
                user_chat_id = user["chat_id"]
                removed_ids = []
                added_obj = []
                for habit in user['habit_clusters'][0]['habits']:

                    obj_time = datetime.strptime(habit['call_time'],  '%Y-%m-%d %H:%M:%S')
                    habit_delta = timeparse(habit['call_delay'])
                    print(user_chat_id, name, habit["name"])

                    if obj_time < datetime.now():
                        removed_ids.append(habit['id'])

                        print("Нужно отправить:", user_chat_id, name, habit["name"], obj_time)
                        log("Сложный момент, в многопоточной программе запускается асинхронная функция", "INFO")
                        sf = asyncio.run_coroutine_threadsafe(self.notify(user_chat_id, habit["text"]), loop)
                        sf.result()

                        print("Отправил:", user_chat_id, name, habit["name"], obj_time)
                        if habit_delta == 604800 or habit_delta == 86400:
                            new_obj = copy.deepcopy(habit)
                            new_obj['call_time'] = str(obj_time + habit_delta)
                            added_obj.append(new_obj)

                url = 'https://faithback.herokuapp.com/api/habbit/{}'
                for user_id in removed_ids:
                    log("Check code from database", "INFO")
                    requests.delete(
                        url.format(user_id),
                        cookies=headers
                    )

                for obj in added_obj:
                    log("Check code from database", "INFO")
                    requests.post(
                        'https://faithback.herokuapp.com/api/users/{}/clusters/habits/'.format(name), json={
                            "name": obj.name,
                            "text": obj.text,
                            "call_time": obj.call_time,
                            "call_delay": obj.call_delay,
                        },
                        cookies=headers
                    )
            time.sleep(100)

    async def notify(self, uid, name):
        log("Function notify entry", "INFO")
        log("Bot sends message", "INFO")
        await bot.send_message(
            chat_id=uid,
            text=f"Напоминаю: {name}"
        )
