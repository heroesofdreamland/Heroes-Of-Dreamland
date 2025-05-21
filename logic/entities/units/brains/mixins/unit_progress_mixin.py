from typing import MutableSequence

from logic.entities.rewards.threshold_rewards import threshold_rewards, max_level_threshold_reward
from logic.core.draw_queue import DrawQueue
from logic.entities.units.models.animated_objects.player.level_up import LevelUpObject
from logic.environment.environment import Environment, Groups


class UnitProgressMixin:
    def __init__(self):
        self.__level = 0
        self.__experience = 0
        self.__guild_coins = 1
        self.__fame = 0

    @property
    def level(self) -> int:
        return self.__level

    @property
    def experience(self) -> int:
        return self.__experience

    @property
    def guild_coins(self) -> int:
        return self.__guild_coins

    @property
    def fame(self) -> int:
        return self.__fame

    def process_input(self, events: MutableSequence):
        pass

    def pre_update(self):
        pass

    def update(self):
        if self.__experience >= threshold_rewards[min(self.__level, max_level_threshold_reward)][0]:
            self.__level_up_player()

    def post_update(self):
        pass

    def render(self, queue: DrawQueue):
        pass

    def add_level(self, level: int):
        self.__level += level

    def add_experience(self, experience: int):
        self.__experience += experience

    def reset_experience(self):
        self.__experience = 0

    def add_guild_coins(self, guild_coins: int):
        self.__guild_coins += guild_coins

    def remove_guild_coins(self, guild_coins: int):
        self.__guild_coins -= guild_coins

    def add_fame(self, fame: int):
        self.__fame += fame

    def __level_up_player(self):
        current_reward = threshold_rewards[min(self.__level, max_level_threshold_reward)]
        current_reward[1].apply(self)
        Environment.map.objects.append(
            LevelUpObject(
                position=Environment.player.position,
                offset=Environment.player.animated_object.offset,
                group=Groups.objects)
        )