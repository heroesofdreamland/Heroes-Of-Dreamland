from collections.abc import Callable

from logic.core.lifecycle_group import LifecycleGroup
from logic.environment.environment import Environment
from logic.events.trade_state_event import TradeStateEvent, TradeState
from logic.level_design.levels.level import Level
from logic.level_design.maps.utils.map_model import MapModel
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.models.neutrals.trader.trader import Trader
from logic.entities.units.unit_factory import generate_unit, UnitGroup


class TraderLevel(Level):
    def __init__(self,
                 group: LifecycleGroup,
                 map_model: MapModel,
                 level_end_handler: Callable):
        super().__init__(group=group, map_model=map_model, level_end_handler=level_end_handler)
        self.__map_model = map_model
        self._timer.set_duration(15)
        self.__trader: Unit | None = None
        self.__trade_state: TradeState | None = None

    def start_level(self):
        super().start_level()
        self.__trader = generate_unit(
            unit_type=Trader,
            coordinate=self.__map_model.random_spawn_position(),
            group=UnitGroup.NEUTRAL
        )

    def update(self):
        super().update()
        for event in Environment.event_manager.events():
            if isinstance(event, TradeStateEvent):
                self.__trade_state = event.state

        if self.__trade_state == TradeState.NONE:
            self.__end_level()
        elif self._timer.is_completed() and self.__trade_state is None:
            self.__end_level()

    def __end_level(self):
        if self.__trader is not None:
            self.__trader.is_alive = False
        self.end_level()
