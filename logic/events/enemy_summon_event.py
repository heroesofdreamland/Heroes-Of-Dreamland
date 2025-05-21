from logic.events.event import Event


class EnemySummonEvent(Event):
    def __init__(self, enemy):
        self.enemy = enemy
