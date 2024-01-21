import datetime

"""Класс статистики"""


class Statistics:
    def __init__(self):
        self.health_refilled = 0
        self.launch_time = datetime.datetime.now()
