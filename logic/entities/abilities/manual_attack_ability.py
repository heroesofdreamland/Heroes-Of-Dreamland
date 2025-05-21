from typing import cast, MutableSequence

import pygame

from logic.entities.abilities.ability import Ability
from logic.core.draw_queue import DrawQueue
from logic.environment.environment import Environment
from logic.ui.colors import Colors
from logic.settings.debug_settings import DebugSettings
from logic.settings.key_settings import KeySettings
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.brains.helpers.unit_distances_helper import UnitDistancesHelper
from logic.entities.units.brains.mixins.unit_attack_mixin import AttackState
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.damage_data import DamageData
from logic.entities.units.data.unit_life_state import UnitLifeState


class ManualAttackAbility(Ability):
    def __init__(self, damage_radius: float, max_attack_enemies: int | None, damage_data: DamageData, enemies_provider: EnemiesProvider):
        self.__damage_radius = damage_radius
        self.__max_attack_enemies = max_attack_enemies
        self.damage_data = damage_data
        self.__enemies_provider = enemies_provider
        self.__is_attacking = False

    def process_input(self, owner: object, events: MutableSequence):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.scancode == KeySettings.get_key('ATTACK'):
                    self.__is_attacking = True
            if event.type == pygame.KEYUP:
                if event.scancode == KeySettings.get_key('ATTACK'):
                    self.__is_attacking = False

    def update(self, owner: object):
        owner = cast(Unit, owner)
        if owner.life_state == UnitLifeState.DEATH:
            return
        enemies = self.__enemies_provider()
        should_attack = self.__is_attacking and not owner.is_stunned and not owner.is_moving
        owner.update_attack_state(should_start_attack=should_attack, should_continue_attack=should_attack)
        owner_position = owner.position
        match owner.attack_state:
            case AttackState.ATTACK:
                attacked_enemies = 0
                for enemy in UnitDistancesHelper.units_in_radius(center=owner_position, radius=self.__damage_radius, units=enemies, side=owner.side):
                    enemy_position = enemy.position
                    if Environment.map.pathfinder.is_path_clear(start=(owner_position.x, owner_position.y), end=(enemy_position.x, enemy_position.y), radius=1) and (self.__max_attack_enemies is None or self.__max_attack_enemies > attacked_enemies):
                        attacked_enemies += 1
                        enemy.get_damage(damage_data=self.damage_data, attacker=owner)

    def render(self, owner: object, queue: DrawQueue):
        if DebugSettings.debug_settings['show_unit_damage_radii']:
            owner = cast(Unit, owner)
            position = owner.position
            queue.debug_draw_circle(color=Colors.RED, radius=self.__damage_radius, position=(position.x, position.y), game_space=True)
