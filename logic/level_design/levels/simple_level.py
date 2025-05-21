from collections.abc import Callable
from typing import Type

from logic.core.lifecycle_group import LifecycleGroup
from logic.environment.environment import Environment
from logic.events.enemy_death_event import EnemyDeathEvent
from logic.events.enemy_summon_event import EnemySummonEvent
from logic.level_design.levels.level import Level
from logic.level_design.maps.utils.map_model import MapModel


class SimpleLevel(Level):
    def __init__(self,
                 group: LifecycleGroup,
                 map_model: MapModel,
                 enemy_types: list[Type],
                 enemies_to_spawn: int,
                 initial_enemies: list[Type],
                 level_end_handler: Callable):
        self.__enemy_types = enemy_types
        self.__spawn_time_interval = 0.2
        self.__enemies_to_spawn = enemies_to_spawn
        self.__initial_enemies = initial_enemies
        self.__enemies_to_die = self.__enemies_to_spawn
        super().__init__(group=group, map_model=map_model, level_end_handler=level_end_handler)

    def start_level(self):
        super().start_level()
        for enemy_type in self.__initial_enemies:
            self._spawn_enemy(enemy_type)
            self.__enemies_to_spawn -= 1

    def update(self):
        super().update()
        for event in Environment.event_manager.events():
            if isinstance(event, EnemySummonEvent):
                self.__handle_enemy_summon()
            if isinstance(event, EnemyDeathEvent):
                self.__handle_enemy_death()
        if self._timer.is_running():
            if self._last_spawn_time is None:
                self._spawn_random_enemy(types=self.__enemy_types)
                self.__enemies_to_spawn -= 1
            elif self._timer.get_time() - self._last_spawn_time > self.__spawn_time_interval and self.__enemies_to_spawn > 0:
                self._spawn_random_enemy(types=self.__enemy_types)
                self.__enemies_to_spawn -= 1

    def __handle_enemy_death(self):
        self.__enemies_to_die -= 1
        if self.__enemies_to_spawn > 0:
            self._spawn_random_enemy(types=self.__enemy_types)
            self.__enemies_to_spawn -= 1
        if self.__enemies_to_die == 0:
            self.end_level()

    def __handle_enemy_summon(self):
        self.__enemies_to_die += 1