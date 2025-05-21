from typing import Callable, cast

from logic.entities.abilities.ability import Ability
from logic.environment.environment import Environment
from logic.events.enemy_death_event import EnemyDeathEvent
from logic.entities.units.brains.helpers.unit_distances_helper import UnitDistancesHelper
from logic.entities.units.brains.unit_brain import Unit


class DetectDeathsAbility(Ability):
    def __init__(self, radius: float | None, action: Callable[[Unit, Unit], None]):
        self.__radius = radius
        self.__action = action

    def update(self, owner: object):
        for event in Environment.event_manager.events():
            if isinstance(event, EnemyDeathEvent):
                unit = cast(Unit, event.enemy)
                owner = cast(Unit, owner)
                if self.__radius is None or UnitDistancesHelper.is_unit_in_radius(center=owner.position, radius=self.__radius, unit=unit, should_be_alive=False):
                    self.__action(owner, unit)