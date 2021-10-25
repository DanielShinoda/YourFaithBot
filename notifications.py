from typing import NamedTuple


class NotificationResult(NamedTuple):
    example: int


class Notification:
    def __init__(self):
        pass

    def draw(self):
        pass


class MoodNotification(Notification):
    def draw(self):
        pass


class BasicNotification(Notification):
    def draw(self):
        pass
