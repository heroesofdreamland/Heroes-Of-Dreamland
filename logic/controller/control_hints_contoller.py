from logic.core.draw_queue import DrawQueue, DrawAnchor
from logic.core.lifecycle import Lifecycle
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.render.components.hstack import HStack
from logic.core.render.components.margin import Margin
from logic.core.render.components.static_image import StaticImage
from logic.core.render.components.text import Text
from logic.core.render.components.vstack import VStack, VStackAlignment
from logic.environment.environment import Environment
from logic.events.inventory_state_event import InventoryStateEvent
from logic.events.trade_state_event import TradeState, TradeStateEvent
from logic.ui.colors import Colors
from logic.ui.fonts import Fonts
from logic.core.screen import Screen
from logic.settings.key_settings import KeySettings
from logic.entities.units.brains.helpers.unit_distances_helper import UnitDistancesHelper
from logic.entities.units.data.unit_life_state import UnitLifeState
from logic.entities.units.models.neutrals.guild_grandmaster.guild_grandmaster import GuildGrandmaster
from logic.entities.units.models.neutrals.trader.trader import Trader


class ControlHintsController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)
        self.__controls_list: list[tuple[list[str], str]] = []
        self.__last_trade_event: TradeStateEvent | None = None
        self.__last_inventory_event: InventoryStateEvent | None = None

    def update(self):
        for event in Environment.event_manager.events():
            if isinstance(event, TradeStateEvent):
                self.__last_trade_event = event
            if isinstance(event, InventoryStateEvent):
                self.__last_inventory_event = event
        self.__reload_controls_list()

    def render(self, queue: DrawQueue):
        self.__render_controls(screen_height=Screen.get_current_resolution()[1], queue=queue)

    def __reload_controls_list(self):
        new_controls = []
        if Environment.scene_manager.current_activated_scene().name == 'keyboard_settings':
            new_controls.append([['R'], 'Reset keys'])
        else:
            if Environment.player.life_state == UnitLifeState.DEATH:
                self.__controls_list = []
                return
            if self.__last_trade_event is not None and self.__last_trade_event.state != TradeState.NONE:
                new_controls.append([['ESC'], 'Quit'])
                if self.__last_trade_event.state == TradeState.BUY:
                    if Environment.player.all_items:
                        new_controls.append([[KeySettings.get_value_for_scancode(KeySettings.get_key('STORE_SWITCH_MODE'))], 'Selling'])
                    new_controls.append([['A', 'D'], 'Navigate'])
                    if self.__last_trade_event.can_trade_now:
                        new_controls.append([['SPACE'], 'Buy item'])
                if self.__last_trade_event.state == TradeState.SELL:
                    new_controls.append([[KeySettings.get_value_for_scancode(KeySettings.get_key('STORE_SWITCH_MODE'))], 'Buying'])
                    new_controls.append([['W', 'A', 'S', 'D'], 'Navigate'])
                    if self.__last_trade_event.can_trade_now:
                        new_controls.append([['SPACE'], 'Sell item'])
            elif self.__last_inventory_event is not None and self.__last_inventory_event.is_opened:
                new_controls.append([['ESC'], 'Quit'])
            elif not Environment.player.is_stunned:
                new_controls.append([[KeySettings.get_value_for_scancode(KeySettings.get_key('ATTACK'))], 'Attack'])
                for neutral in Environment.map.neutrals:
                    if UnitDistancesHelper.are_units_colliding(neutral, Environment.player):
                        if isinstance(neutral, Trader):
                            new_controls.append([[KeySettings.get_value_for_scancode(KeySettings.get_key('ACTION'))], 'Trade'])
                        elif isinstance(neutral, GuildGrandmaster):
                            new_controls.append([[KeySettings.get_value_for_scancode(KeySettings.get_key('ACTION'))], 'Get order'])
        self.__controls_list = new_controls

    def __render_controls(self, screen_height: float, queue: DrawQueue):
        Margin(
            child=VStack(
                children=[
                    HStack(
                        children=[
                            HStack(
                                children=[
                                    StaticImage(
                                        path='resources/used_resources/controls/' + element + '.png'
                                    ) for element in pair[0]
                                ],
                                spacing=4
                            ),
                            Text(
                                text=pair[1],
                                font=Fonts.blackcraft(size=20),
                                color=Colors.WHITE
                            )
                        ],
                        spacing=8
                    ) for pair in reversed(self.__controls_list)
                ],
                spacing=8,
                alignment=VStackAlignment.START
            ),
            left=20,
            bottom=20
        ).draw(
            position=(0, screen_height),
            anchor=DrawAnchor.BOTTOM_LEFT,
            queue=queue
        )
