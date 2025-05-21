from typing import cast, MutableSequence

import pygame

from logic.entities.abilities.ability import Ability
from logic.settings.key_settings import KeySettings
from logic.entities.units.brains.mixins.unit_attack_mixin import AttackState
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.unit_life_state import UnitLifeState


class MoveWithKeyboardAbility(Ability):
    def __init__(self):
        self.__direction_x: float = 0
        self.__direction_y: float = 0
        self.__key_states = {
            KeySettings.get_key('LEFT'): False,
            KeySettings.get_key('RIGHT'): False,
            KeySettings.get_key('UP'): False,
            KeySettings.get_key('DOWN'): False,
        }

    def pre_update(self, owner: object):
        owner = cast(Unit, owner)
        if not owner.group.is_input_enabled:
            for key in self.__key_states:
                self.__key_states[key] = False

    def process_input(self, owner: object, events: MutableSequence):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.scancode in self.__key_states:
                    self.__key_states[event.scancode] = True
            elif event.type == pygame.KEYUP:
                if event.scancode in self.__key_states:
                    self.__key_states[event.scancode] = False

        direction_x = 0
        direction_y = 0
        if self.__key_states[KeySettings.get_key('LEFT')]:
            direction_x -= 1
            direction_y += 1
        if self.__key_states[KeySettings.get_key('RIGHT')]:
            direction_x += 1
            direction_y -= 1
        if self.__key_states[KeySettings.get_key('UP')]:
            direction_x -= 1
            direction_y -= 1
        if self.__key_states[KeySettings.get_key('DOWN')]:
            direction_x += 1
            direction_y += 1

        self.__direction_x = direction_x
        self.__direction_y = direction_y

    def update(self, owner: object):
        owner = cast(Unit, owner)
        if owner.life_state == UnitLifeState.DEATH:
            return
        if owner.attack_state != AttackState.NONE:
            return
        owner.set_direction(x=self.__direction_x, y=self.__direction_y)
