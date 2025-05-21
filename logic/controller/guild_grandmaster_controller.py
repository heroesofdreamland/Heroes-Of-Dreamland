from typing import MutableSequence

import pygame

from logic.core.lifecycle import Lifecycle
from logic.core.lifecycle_group import LifecycleGroup
from logic.environment.environment import Environment
from logic.entities.orders.order_generator import generate_order
from logic.settings.key_settings import KeySettings
from logic.entities.units.brains.helpers.unit_distances_helper import UnitDistancesHelper
from logic.entities.units.models.neutrals.guild_grandmaster.guild_grandmaster import GuildGrandmaster


class GuildGrandmasterController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)

    def process_input(self, events: MutableSequence):
        for event in events:
            if event.type == pygame.KEYDOWN:
                scancode = event.scancode
                if scancode == KeySettings.get_key('ACTION'):
                    for neutral in Environment.map.neutrals:
                        if isinstance(neutral, GuildGrandmaster) and UnitDistancesHelper.are_units_colliding(neutral, Environment.player):
                            if Environment.player.guild_coins > 0:
                                Environment.orders.append(generate_order())
                                Environment.player.remove_guild_coins(1)
