from typing import cast

from logic.entities.abilities.ability import Ability
from logic.core.lifecycle import Lifecycle
from logic.core.timer import Timer
from logic.environment.environment import Groups
from logic.entities.units.models.animation_type import AnimationType


class ResurrectionAbility(Ability):
    def __init__(self, wait_duration: float, is_enabled: bool = True):
        self.__wait_duration = wait_duration
        self.__is_enabled = is_enabled
        self.__wait_timer: Timer | None = None

    @property
    def is_resurrecting(self) -> bool:
        return self.__wait_timer is not None

    @property
    def is_enabled(self) -> bool:
        return self.__is_enabled

    def update(self, owner: object):
        if not self.__is_enabled or not self.is_resurrecting:
            return
        from logic.entities.units.brains.unit_brain import Unit
        owner = cast(Unit, owner)
        if self.__wait_timer.is_completed():
            owner.animated_object.configure_animation(AnimationType.RESURRECTION)
            if owner.animated_object.is_animation_completed():
                self.__is_enabled = False
                self.__wait_timer.stop(group=Groups.objects)
                self.__wait_timer = None
                owner.resurrect()

    def start_resurrection_or_die(self, owner: Lifecycle):
        if not self.__is_enabled:
            owner.is_alive = False
            return
        if self.is_resurrecting:
            return
        self.__wait_timer = Timer(duration=self.__wait_duration)
        self.__wait_timer.start(group=Groups.objects)
