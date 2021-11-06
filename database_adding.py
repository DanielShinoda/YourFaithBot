import requests
import habits
import user
from bot_options import headers


# All users in db
users = dict()


def add_new_user_to_users(database_user):
    print(database_user)
    chosen_life_spheres = ["habits"]

    habit_collections = {
        'sport': habits.HabitCollection('sport'),
        'meditation': habits.HabitCollection('meditation'),
        'sleep': habits.HabitCollection('sleep'),
        'mood': habits.HabitCollection('mood'),
        'habits': habits.HabitCollection('habits')
    }

    for name in habit_collections:
        habit_collections[name].init_from_file("./configs/" + name + "_config.json")

    # read user options
    user_options = user.UserOptions(database_user["chat_id"])

    new_user = user.User(habit_collections, chosen_life_spheres, user_options)

    r = requests.post(
        'https://faithback.herokuapp.com/api/users/{}/clusters/'.format(database_user["login"]), json={
            "name": "habits"
        },
        cookies=headers
    )

    new_user.set_progress("habits", database_user["habit_clusters"][0])

    users[new_user.user_options_.chat_id] = new_user


def add_user_in_db(name_, id_):
    r = requests.get('https://faithback.herokuapp.com/api/users/{}/'.format(name_), cookies=headers)

    if r.status_code != 200:

        requests.post(
            'https://faithback.herokuapp.com/api/users/', json={
                "login": name_,
                "chat_id": id_
            },
            cookies=headers)

        requests.post(
            'https://faithback.herokuapp.com/api/users/{}/clusters/'.format(name_), json={
                "name": "habits"
            },
            cookies=headers
        )

        r = requests.get('https://faithback.herokuapp.com/api/users/{}/'.format(name_), cookies=headers)

        add_new_user_to_users(r.json())


