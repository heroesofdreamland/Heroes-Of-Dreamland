from logic.events.event import Event


class EventManager:
    def __init__(self):
        self.__preparing_events: list[Event] = []
        self.__ready_events: list[Event] = []

    def send(self, event: Event):
        self.__preparing_events.append(event)

    def events(self) -> list[Event]:
        return self.__ready_events

    def publish(self):
        self.__ready_events = self.__preparing_events
        self.__preparing_events = []
