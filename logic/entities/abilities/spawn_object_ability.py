from typing import cast

from logic.entities.abilities.ability import Ability
from logic.environment.environment import Environment, Groups
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.models.animated_objects.enemy.spawn_object import SpawnObject


class SpawnObjectAbility(Ability):
    def __init__(self):
        self.__is_spawned = False

    def update(self, owner: object):
        owner = cast(Unit, owner)
        if not self.__is_spawned:
            Environment.map.objects.append(
                SpawnObject(
                    position=owner.position,
                    offset=owner.animated_object.offset,
                    group=Groups.objects
                )
            )
            self.__is_spawned = True
