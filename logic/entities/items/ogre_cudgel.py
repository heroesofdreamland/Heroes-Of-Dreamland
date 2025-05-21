from typing import cast, MutableSequence

import pygame
from pymunk import Vec2d

from logic.core.animation import Animation
from logic.core.timer import Timer
from logic.entities.effects.negative.stun_effect import StunEffect
from logic.environment.environment import Environment, Groups
from logic.entities.items.item import Item
from logic.settings.key_settings import KeySettings
from logic.entities.units.brains.helpers.unit_distances_helper import UnitDistancesHelper
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.models.animated_objects.items.ogre_cudgel_object import OgreCudgelObject
from logic.entities.units.models.animation_type import AnimationType


class OgreCudgel(Item):
    def __init__(self):
        self.path = 'resources/used_resources/items/chaos_incarnatech_loot/ogre_cudgel/'
        self.__radius = 90
        self.__attack_delay = 0.3
        self.__cooldown_duration = 3
        self.__stun_duration = 2.5
        self.__timer = Timer(duration=self.__cooldown_duration)
        self.__attack_position: Vec2d | None = None
        super().__init__(price=100,
                         description='OgreCudgel',
                         is_active=True)

    def process_input(self, owner: object, events: MutableSequence, slot: int | None):
        if slot is None:
            return
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.scancode == KeySettings.get_key('SLOT_' + str(slot + 1)):
                    self.__start_attack_if_needed(owner=owner)

    def update(self, owner: object):
        if self.__timer.is_running() and self.__timer.get_time() >= self.__attack_delay and self.__attack_position is not None:
            owner = cast(Unit, owner)
            for enemy in UnitDistancesHelper.units_in_radius(center=self.__attack_position,
                                                             radius=self.__radius,
                                                             units=owner.enemies_provider(),
                                                             side=None):
                enemy.effects.append(StunEffect(self.__stun_duration))
            self.__attack_position = None

    def __start_attack_if_needed(self, owner: object):
        if not self.__timer.is_running() or self.__timer.is_completed():
            if self.__timer.is_running():
                self.__timer.stop(Groups.player)
            self.__timer.start(Groups.player)
            owner = cast(Unit, owner)
            attack_position = owner.position
            Environment.map.objects.append(
                OgreCudgelObject(
                    position=attack_position,
                    offset=owner.animated_object.offset,
                    side=owner.side,
                    group=Groups.objects
                )
            )
            self.__attack_position = attack_position

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

    def cooldown(self) -> float | None:
        if self.__timer.is_running() and not self.__timer.is_completed():
            return self.__cooldown_duration - self.__timer.get_time()
        else:
            return None
