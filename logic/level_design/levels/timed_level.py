from collections.abc import Callable

from logic.core.lifecycle_group import LifecycleGroup
from logic.entities.units.models.frozen_wyverns.tier2.treant.treant import Treant
from logic.environment.environment import Environment
from logic.level_design.levels.level import Level
from logic.level_design.maps.utils.map_model import MapModel
from logic.entities.units.data.unit_life_state import UnitLifeState
from logic.entities.units.models.frozen_wyverns.tier1.warrior.warrior import Warrior
from logic.entities.units.models.frozen_wyverns.tier2.skeleton_thrasher.skeleton_thrasher import SkeletonThrasher


class TimedLevel(Level):
    def __init__(self,
                 group: LifecycleGroup,
                 map_model: MapModel,
                 level_end_handler: Callable):
        self.enemy_names = [Warrior, SkeletonThrasher, Treant]
        self.__spawn_time_interval = 0.5
        super().__init__(group=group, map_model=map_model, level_end_handler=level_end_handler)
        self._timer.set_duration(5)

    def update(self):
        super().start_level()
        self.__timed_spawn_random_enemy()
        if self._timer.is_completed():
            self.__kill_all_enemies()
            self.end_level()

    @staticmethod
    def __kill_all_enemies():
        for enemy in Environment.map.enemies:
            enemy.life_state = UnitLifeState.DEATH

    def __timed_spawn_random_enemy(self):
        if self._last_spawn_time is None:
            self._spawn_random_enemy(types=self.enemy_names)
        elif self._timer.get_time() - self._last_spawn_time > self.__spawn_time_interval:
            self._spawn_random_enemy(types=self.enemy_names)
