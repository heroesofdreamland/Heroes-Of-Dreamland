from logic.core.lifecycle import Lifecycle
from logic.core.lifecycle_group import LifecycleGroup
from logic.environment.environment import Environment


class OrdersController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        self.__orders = Environment.orders
        super().__init__(group=group)

    def update(self):
        for quest in self.__orders:
            quest.update()
            if quest.is_completed:
                #play_sound and animation
                self.__orders.remove(quest)