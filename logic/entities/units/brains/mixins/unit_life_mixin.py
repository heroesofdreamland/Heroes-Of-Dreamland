from copy import deepcopy
from typing import cast, MutableSequence

from logic.entities.abilities.resurrection_ability import ResurrectionAbility
from logic.core.draw_queue import DrawQueue
from logic.entities.rewards.kill_reward import KillReward
from logic.environment.environment import Environment
from logic.events.enemy_death_event import EnemyDeathEvent
from logic.entities.units.data.damage_data import DamageData
from logic.entities.units.data.unit_life_state import UnitLifeState
from logic.entities.units.data.unit_metadata import UnitMetadataKey
from logic.entities.units.models.animation_type import AnimationType


class UnitLifeMixin:
    def __init__(self, souls: float, reward: KillReward | None):
        self.__souls = souls
        self.__life_state = UnitLifeState.ALIVE
        self.__last_attacker: object | None = None
        self.__reward = reward

    @property
    def souls(self) -> float:
        return self.__souls

    @property
    def life_state(self) -> UnitLifeState:
        return self.__life_state

    @property
    def reward(self) -> KillReward:
        return self.__reward

    def add_souls(self, souls: float):
        self.__souls += souls

    def remove_souls(self, souls: float):
        self.__souls -= souls

    def kill(self):
        self.__life_state = UnitLifeState.DEATH
        self.__souls = 0

    def resurrect(self):
        self.__life_state = UnitLifeState.ALIVE
        self.__souls = 1

    def get_damage(self, damage_data: DamageData, attacker: object | None):
        self.__last_attacker = attacker
        from logic.entities.units.brains.unit_brain import Unit
        unit = cast(Unit, self)
        unit.metadata[UnitMetadataKey.DAMAGE_TAKEN] = True
        for effect in damage_data.effects:
            unit.effect_apply(effect=deepcopy(effect))

        remaining_damage = damage_data.damage
        if remaining_damage <= 0:
            return

        remaining_damage = unit.armor_consume_damage(damage=remaining_damage)

        if remaining_damage >= self.__souls:
            self.__souls = 0
            self.__life_state = UnitLifeState.DEATH
        else:
            self.__souls -= remaining_damage

    def process_input(self, events: MutableSequence):
        pass

    def pre_update(self):
        pass

    def update(self):
        match self.__life_state:
            case UnitLifeState.DEATH:
                from logic.entities.units.brains.unit_brain import Unit
                unit = cast(Unit, self)
                resurrection_ability = unit.ability(ability_type=ResurrectionAbility)
                animation_type = unit.animated_object.get_current_animation_type()
                if animation_type == AnimationType.DEATH and unit.animated_object.is_animation_completed():
                    unit.is_alive = False
                    if self.__last_attacker is not None and self.__reward is not None:
                        self.__reward.apply(self.__last_attacker)
                if animation_type == AnimationType.DEATH_WITH_RESURRECTION and unit.animated_object.is_animation_completed():
                    if resurrection_ability is not None:
                        resurrection_ability.start_resurrection_or_die(owner=unit)

    def post_update(self):
        if not self.is_alive:  # Lifecycle.is_alive (cast removed for performance)
            Environment.event_manager.send(EnemyDeathEvent(enemy=self))

    def render(self, queue: DrawQueue):
        pass
