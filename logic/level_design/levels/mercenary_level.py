from collections.abc import Callable

from logic.core.lifecycle_group import LifecycleGroup
from logic.level_design.levels.level import Level
from logic.level_design.maps.utils.map_model import MapModel
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.models.neutrals.guild_grandmaster.guild_grandmaster import GuildGrandmaster
from logic.entities.units.unit_factory import generate_unit, UnitGroup


class MercenaryLevel(Level):
    def __init__(self,
                 group: LifecycleGroup,
                 map_model: MapModel,
                 level_end_handler: Callable):
        super().__init__(group=group, map_model=map_model, level_end_handler=level_end_handler)
        self.__map_model = map_model
        self.__mercenary: Unit | None = None

    def start_level(self):
        super().start_level()
        self.__mercenary = generate_unit(
            unit_type=GuildGrandmaster,
            coordinate=self.__map_model.random_spawn_position(),
            group=UnitGroup.NEUTRAL
        )

    def update(self):
        super().update()