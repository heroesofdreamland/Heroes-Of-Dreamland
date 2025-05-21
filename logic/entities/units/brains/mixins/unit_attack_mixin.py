from enum import Enum
from typing import cast, MutableSequence

from logic.core.draw_queue import DrawQueue
from logic.core.timer import Timer
from logic.environment.environment import Groups
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.data.unit_life_state import UnitLifeState


class AttackState(Enum):
    NONE = 'none'
    BEFORE_ATTACK = 'before_attack'
    ATTACK = 'attack'
    AFTER_ATTACK = 'after_attack'
    COOLDOWN = 'cooldown'


class UnitAttackConfig:
    def __init__(self, duration: float, attack_moment: float, cooldown: float):
        self.duration = duration
        self.attack_moment = attack_moment
        self.cooldown = cooldown


class UnitAttackMixin:
    def __init__(self, config: UnitAttackConfig | None, enemies_provider: EnemiesProvider):
        self.__config = config
        self.__enemies_provider = enemies_provider
        self.__timer: Timer | None = None
        self.__is_charging = False
        self.__attack_state = AttackState.NONE

    @property
    def enemies_provider(self) -> EnemiesProvider:
        return self.__enemies_provider

    @property
    def attack_state(self) -> AttackState:
        return self.__attack_state

    def update_attack_state(self, should_start_attack: bool, should_continue_attack: bool):
        from logic.entities.units.brains.unit_brain import Unit
        if cast(Unit, self).life_state == UnitLifeState.DEATH:
            self.__attack_state = AttackState.NONE
            return
        if self.__config is None:
            self.__attack_state = AttackState.NONE
            return
        is_attack_already_started = self.__timer is not None
        if should_start_attack or (is_attack_already_started and should_continue_attack):
            if self.__timer is None:
                self.__timer = Timer(duration=self.__config.duration + self.__config.cooldown)
                self.__timer.start(group=Groups.objects)
                self.__is_charging = True
            current_time = self.__timer.get_time()
            if current_time < self.__config.attack_moment * self.__config.duration:
                self.__attack_state = AttackState.BEFORE_ATTACK
            elif current_time < self.__config.duration and self.__is_charging:
                self.__is_charging = False
                self.__attack_state = AttackState.ATTACK
            elif current_time < self.__config.duration:
                self.__attack_state = AttackState.AFTER_ATTACK
            elif current_time < self.__config.duration + self.__config.cooldown:
                self.__attack_state = AttackState.COOLDOWN
            else:
                self.__stop_timer()
                self.__attack_state = AttackState.NONE
        else:
            self.__stop_timer()
            self.__attack_state = AttackState.NONE

    def process_input(self, events: MutableSequence):
        pass

    def pre_update(self):
        pass

    def update(self):
        pass

    def post_update(self):
        pass

    def render(self, queue: DrawQueue):
        pass

    def __stop_timer(self):
        if self.__timer is not None and self.__timer.is_running():
            self.__timer.stop(group=Groups.objects)
        self.__timer = None
