from logic.core.lifecycle_group import LifecycleGroup
from logic.level_design.maps.utils.map_model import MapModel
from logic.level_design.maps.utils.base_map_controller import BaseMapController


class MapController(BaseMapController):
    def __init__(self, group: LifecycleGroup, map_model: MapModel):
        super().__init__(group=group, map_model=map_model)
        self.map_model.enable_exits(True)
