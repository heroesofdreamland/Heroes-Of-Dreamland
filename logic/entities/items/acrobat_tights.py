from typing import cast, MutableSequence

import pygame

from logic.core.animation import Animation
from logic.core.timer import Timer
from logic.environment.environment import Groups
from logic.entities.items.item import Item
from logic.settings.key_settings import KeySettings
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.models.animation_type import AnimationType


class AcrobatTights(Item):
    def __init__(self):
        self.path = 'resources/used_resources/items/chaos_incarnatech_loot/acrobat_tights/'
        self.__cooldown_duration = 2
        self.__dash_duration = 0.1
        self.__dash_distance = 100
        self.__timer = Timer(duration=self.__cooldown_duration)
        super().__init__(price=100,
                         description='Acrobat tights',
                         is_active=True)

    def process_input(self, owner: object, events: MutableSequence, slot: int | None):
        if slot is None:
            return
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.scancode == KeySettings.get_key('SLOT_' + str(slot + 1)):
                    self.__start_dash_if_needed(owner=owner)

    def update(self, owner: object):
        if self.__timer.is_running() and self.__timer.get_time() < self.__dash_duration:
            dash_speed = self.__dash_distance / self.__dash_duration
            diff_speed = dash_speed - owner.speed # UnitSpeedMixin.speed (cast removed for performance)
            if diff_speed > 0:
                owner.speed_modify(diff=diff_speed, permanent=False) # UnitSpeedMixin.speed_modify (cast removed for performance)

    def __start_dash_if_needed(self, owner: object):
        owner = cast(Unit, owner)
        if not owner.is_moving:
            return
        if not self.__timer.is_running() or self.__timer.is_completed():
            if self.__timer.is_running():
                self.__timer.stop(Groups.player)
            self.__timer.start(Groups.player)

    def get_animations(self) -> dict:
        return {
            AnimationType.USED: Animation(path=self.path + AnimationType.USED.value,
                                          count=18,
                                          duration=0.5,
                                          repeat=True),
            AnimationType.PREVIEW: Animation(path=self.path + AnimationType.PREVIEW.value,
                                             count=12,
                                             duration=0.5,
                                             repeat=True)
        }

    def can_activate(self, owner: object) -> bool:
        return owner.is_moving # UnitSpeedMixin.speed (cast removed for performance)

    def cooldown(self) -> float | None:
        if self.__timer.is_running() and not self.__timer.is_completed():
            return self.__cooldown_duration - self.__timer.get_time()
        else:
            return None
