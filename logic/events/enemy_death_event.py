from logic.events.event import Event


class EnemyDeathEvent(Event):
    def __init__(self, enemy):
        self.enemy = enemy
