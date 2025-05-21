import random
from collections.abc import Callable
from typing import Type
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.timer import Timer
from logic.level_design.maps.utils.map_model import MapModel
from logic.entities.units.unit_factory import generate_unit


class Level:
    def __init__(self,
                 group: LifecycleGroup,
                 map_model: MapModel,
                 level_end_handler: Callable):
        self.__level_end_handler = level_end_handler
        self.__group = group
        self.__map_model = map_model
        self._timer = Timer()
        self._last_spawn_time: float|None = None

    def start_level(self):
        self._timer.start(group=self.__group)

    def pause_level(self, is_paused: bool):
        self._timer.pause(is_paused=is_paused)

    def end_level(self):
        self._timer.stop(group=self.__group)
        self.__level_end_handler()

    def update(self):
        pass

    def _spawn_random_enemy(self, types: list):
        enemy_type = types[random.randint(0, len(types) - 1)]
        self._spawn_enemy(enemy_type)

    def _spawn_enemy(self, enemy_type: Type):
        generate_unit(unit_type=enemy_type, coordinate=self.__map_model.random_spawn_position())
        self._last_spawn_time = self._timer.get_time()
