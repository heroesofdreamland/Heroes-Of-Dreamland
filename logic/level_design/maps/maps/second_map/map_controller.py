from typing import Callable

from logic.core.lifecycle_group import LifecycleGroup
from logic.environment.environment import Groups
from logic.level_design.levels.level import Level
from logic.level_design.levels.trader_level import TraderLevel
from logic.level_design.maps.utils.map_model import MapModel
from logic.level_design.maps.utils.base_map_controller import BaseMapController


class MapController(BaseMapController):
    def __init__(self, group: LifecycleGroup, map_model: MapModel):
        super().__init__(group=group, map_model=map_model)
        self.map_model.enable_exits(True)

    def levels(self, level_end_handler: Callable) -> [Level]:
        return [
            TraderLevel(group=Groups.level,
                        map_model=self.map_model,
                        level_end_handler=level_end_handler)
        ]
