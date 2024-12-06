class EventManager:
    """Observer pattern to notify about password-related events."""
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def notify(self, event):
        for observer in self._observers:
            observer.update(event)


class UserNotification:
    def update(self, event):
        print(f"Notification: {event}")
