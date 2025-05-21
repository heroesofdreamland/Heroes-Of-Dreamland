from typing import cast

from logic.entities.abilities.ability import Ability
from logic.environment.environment import Environment, Groups
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.models.animated_objects.enemy.death_object import DeathObject


class DeathObjectAbility(Ability):
    def post_update(self, owner: object):
        if not owner.is_alive:  # Lifecycle.is_alive (cast removed for performance)
            owner = cast(Unit, owner)
            Environment.map.objects.append(
                DeathObject(
                    position=owner.position,
                    offset=owner.animated_object.offset,
                    group=Groups.objects
                )
            )
