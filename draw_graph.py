import matplotlib.pyplot as plt
import datetime
import seaborn as sns


def draw_graph(my_json):
    sns.set(style="darkgrid")

    # Подготовим данные

    levels = [i["mood"] for i in my_json["mood"]]
    dates = [datetime.datetime.strptime(i["time"].split('.')[0], '%Y-%m-%dT%H:%M:%S') for i in my_json["mood"]]
    dates = [str(i.day) + '.' + str(i.month) + ' ' + str(i.hour) + ':' + str(i.minute) for i in dates]

    # Рисуем
    plt.figure(figsize=(20, 8))
    plt.bar(dates, levels, color="#FFC700")
    plt.ylabel('Уровень настроения от 0 до 4')
    plt.title('График настроения за последние дни')
    plt.savefig('stat.png', dpi=200)
