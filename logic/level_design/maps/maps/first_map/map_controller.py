from typing import Callable

from logic.core.lifecycle_group import LifecycleGroup
from logic.entities.units.models.frozen_wyverns.tier1.bomb.bomb import Bomb
from logic.entities.units.models.frozen_wyverns.tier1.warrior.warrior import Warrior
from logic.entities.units.models.frozen_wyverns.tier1.wyverns_mage.wyverns_mage import WyvernsMage
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
                        enemy_types=[WyvernsMage, Warrior, Bomb],
                        enemies_to_spawn=40,
                        initial_enemies=[Warrior],
                        level_end_handler=level_end_handler)
        ]

    def handle_levels_end(self):
        self.map_model.enable_exits(True)
