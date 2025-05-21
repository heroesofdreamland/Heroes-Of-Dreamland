from typing import cast

from logic.entities.abilities.ability import Ability
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.brains.helpers.unit_distances_helper import UnitDistancesHelper
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.damage_data import DamageData
from logic.entities.units.data.unit_life_state import UnitLifeState


class ExplosionAbility(Ability):
    def __init__(self, trigger_radius: float, damage_radius: float, damage_data: DamageData, enemies_provider: EnemiesProvider):
        self.__trigger_radius = trigger_radius
        self.__damage_radius = damage_radius
        self.__damage_data = damage_data
        self.__enemies_provider = enemies_provider

    def update(self, owner: object):
        super().update(owner=owner)
        owner = cast(Unit, owner)
        if owner.life_state == UnitLifeState.ALIVE and UnitDistancesHelper.units_in_radius(center=owner.position, radius=self.__trigger_radius, units=self.__enemies_provider()):
            owner.kill()

    def post_update(self, owner: object):
        super().post_update(owner=owner)
        owner = cast(Unit, owner)
        if not owner.is_alive:
            for enemy in UnitDistancesHelper.units_in_radius(center=owner.position, radius=self.__damage_radius, units=self.__enemies_provider()):
                enemy.get_damage(damage_data=self.__damage_data, attacker=owner)
