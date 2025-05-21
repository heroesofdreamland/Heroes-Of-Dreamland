from typing import Callable

from logic.core.lifecycle_group import LifecycleGroup
from logic.entities.units.models.frozen_wyverns.tier2.mini_treant.mini_treant import MiniTreant
from logic.entities.units.models.frozen_wyverns.tier2.treant.treant import Treant
from logic.environment.environment import Groups
from logic.level_design.levels.level import Level
from logic.level_design.levels.simple_level import SimpleLevel
from logic.level_design.maps.utils.map_model import MapModel
from logic.level_design.maps.utils.base_map_controller import BaseMapController


class MapController(BaseMapController):
    def __init__(self, group: LifecycleGroup, map_model: MapModel):
        super().__init__(group=group, map_model=map_model)
        self.map_model.enable_exits(False)

    def levels(self, level_end_handler: Callable) -> [Level]:
        return [
            SimpleLevel(group=Groups.level,
                        map_model=self.map_model,
                        enemy_types=[Treant, MiniTreant],
                        enemies_to_spawn=15,
                        initial_enemies=[MiniTreant],
                        level_end_handler=level_end_handler)
        ]

    def handle_levels_end(self):
        self.map_model.enable_exits(True)
