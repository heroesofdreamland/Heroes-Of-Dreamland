from typing import Type

from logic.entities.rewards.order_reward import OrderReward
from logic.environment.environment import Environment
from logic.events.enemy_death_event import EnemyDeathEvent
from logic.entities.orders.order import Order


class AssassinationOrder(Order):
    def __init__(self, enemy_type: Type, kills_count: int):
        self.enemy_type = enemy_type
        self.reward = OrderReward(fame=1)
        super().__init__(name='Assassination order',
                         description=f'Kill {kills_count} {self.enemy_type.__name__}',
                         progress=kills_count,
                         cost=100)

    def update(self):
        if self.is_completed:
            return 
        if self.progress <= 0:
            self.complete()
            return
        for event in Environment.event_manager.events():
            if isinstance(event, EnemyDeathEvent) and isinstance(event.enemy, self.enemy_type):
                self.progress -= 1

    def complete(self):
        self.reward.apply(Environment.player)
        self.is_completed = True

