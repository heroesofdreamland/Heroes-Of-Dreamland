from typing import Type, cast

from logic.entities.abilities.ability import Ability
from logic.environment.environment import Environment
from logic.events.enemy_summon_event import EnemySummonEvent
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.enemy_config import EnemyConfigKey
from logic.entities.units.unit_factory import generate_unit


class TrojanAbility(Ability):
    def __init__(self, summon_type: Type, count_of_summons: int, depth: int = 1):
        self.__summon_type = summon_type
        self.__count_of_summons = count_of_summons
        self.__depth = depth

    def post_update(self, owner: object):
        owner = cast(Unit, owner)
        if not owner.is_alive and self.__depth > 0:
            owner_position = owner.position
            for i in range(self.__count_of_summons):
                new_enemy = generate_unit(
                    unit_type=self.__summon_type,
                    coordinate=owner_position,
                    config={
                        EnemyConfigKey.IS_SUMMONED: True,
                        EnemyConfigKey.TROJAN_DEPTH: self.__depth - 1
                    }
                )
                Environment.event_manager.send(EnemySummonEvent(enemy=new_enemy))