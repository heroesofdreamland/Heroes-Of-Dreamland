from typing import MutableSequence

import pygame

from logic.core.animated_object import AnimatedObject
from logic.core.animation import Animation
from logic.core.draw_queue import DrawQueue, DrawAnchor
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.lifecycle import Lifecycle
from logic.core.render.components.animated_image import AnimatedImage
from logic.core.render.components.grid import Grid
from logic.core.render.components.hstack import HStack, HStackAlignment
from logic.core.render.components.rect import Rect
from logic.core.render.components.text import Text
from logic.core.render.components.vstack import VStack
from logic.core.render.components.zstack import ZStack
from logic.environment.environment import Environment, Groups
from logic.events.trade_state_event import TradeState, TradeStateEvent
from logic.entities.items.boots_of_speed import BootsOfSpeed
from logic.entities.items.item import ItemType
from logic.entities.items.ogre_cudgel import OgreCudgel
from logic.ui.colors import Colors
from logic.ui.fonts import Fonts
from logic.settings.key_settings import KeySettings
from logic.core.screen import Screen
from logic.entities.units.models.neutrals.trader.trader import Trader
from logic.utils.screen_dimmer import ScreenDimmer
from logic.entities.units.brains.helpers.unit_distances_helper import UnitDistancesHelper
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.models.animation_type import AnimationType


class StoreController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        self.__animated_object = AnimatedObject(
            animations={
                AnimationType.PREVIEW_STORE: Animation(
                    path='resources/used_resources/store/store_activation/',
                    count=27,
                    duration=0.8,
                    repeat=False
                )
            },
            scale=5,
            offset=(0, 0)
        )
        self.__active_trader: Unit | None = None
        self.__is_selling = False
        self.__buying_selection = 0
        self.__buying_items = [BootsOfSpeed(), OgreCudgel(), BootsOfSpeed()]
        self.__buying_item_size = 100 * Screen.get_screen_scale()
        self.__selling_grid_cell_size = 48
        self.__selling_grid_width = 6
        self.__selling_grid_height = 10
        self.__selling_selection_x = 0
        self.__selling_selection_y = 0
        self.__screen_dimmer = ScreenDimmer()
        super().__init__(group=group)

    def process_input(self, events: MutableSequence):
        for event in events:
            if event.type == pygame.KEYDOWN:
                scancode = event.scancode
                if self.__active_trader is None:
                    if scancode == KeySettings.get_key('ACTION'):
                        for neutral in Environment.map.neutrals:
                            if isinstance(neutral, Trader) and UnitDistancesHelper.are_units_colliding(neutral, Environment.player):
                                self.__set_trading(trader=neutral)
                                break
                else:
                    if scancode == pygame.KSCAN_SPACE or scancode == pygame.KSCAN_RETURN:
                        if self.__is_selling:
                            index = self.__selling_selection_x + self.__selling_selection_y * self.__selling_grid_width
                            all_items = Environment.player.all_items
                            if index < len(all_items):
                                item = all_items[index]
                                Environment.player.add_souls(souls=item.price / 2)
                                Environment.player.remove_item(item)
                                self.__selling_send_event()
                                if not Environment.player.all_items:
                                    self.__switch_mode(is_selling=False)
                        else:
                            selected_item = self.__buying_selected_item()
                            if Environment.player.souls > selected_item.price:
                                Environment.player.remove_souls(souls=selected_item.price)
                                Environment.player.add_item(selected_item)
                                self.__buying_send_event()
                                selected_item.get_animated_object(ItemType.store).configure_animation(AnimationType.USED)

                    elif scancode == pygame.KSCAN_A or scancode == pygame.KSCAN_LEFT:
                        if self.__is_selling:
                            self.__selling_selection_x = (self.__selling_selection_x + self.__selling_grid_width * 2 - 1) % (self.__selling_grid_width * 2)
                            self.__selling_send_event()
                        else:
                            self.__buying_selection = (self.__buying_selection - 1) % len(self.__buying_items)
                            self.__buying_send_event()

                    elif scancode == pygame.KSCAN_D or scancode == pygame.KSCAN_RIGHT:
                        if self.__is_selling:
                            self.__selling_selection_x = (self.__selling_selection_x + 1) % (self.__selling_grid_width * 2)
                            self.__selling_send_event()
                        else:
                            self.__buying_selection = (self.__buying_selection + 1) % len(self.__buying_items)
                            self.__buying_send_event()

                    elif scancode == pygame.KSCAN_W or scancode == pygame.KSCAN_UP:
                        if self.__is_selling:
                            self.__selling_selection_y = (self.__selling_selection_y + self.__selling_grid_height - 1) % self.__selling_grid_height
                            self.__selling_send_event()

                    elif scancode == pygame.KSCAN_S or scancode == pygame.KSCAN_DOWN:
                        if self.__is_selling:
                            self.__selling_selection_y = (self.__selling_selection_y + 1) % self.__selling_grid_height
                            self.__selling_send_event()

                    elif scancode == pygame.KSCAN_ESCAPE:
                        self.__set_trading(trader=None)
                        self.__animated_object.destroy_animation()
                        events.remove(event)

                    elif scancode == KeySettings.get_key('STORE_SWITCH_MODE'):
                        self.__switch_mode(is_selling=not self.__is_selling)

    def render(self, queue: DrawQueue):
        if self.__active_trader is not None:
            screen_width, screen_height = Screen.get_current_resolution()
            self.__screen_dimmer.render(queue=queue)
            AnimatedImage(
                animated_object=self.__animated_object,
                animation_type=AnimationType.PREVIEW_STORE
            ).draw(
                position=(screen_width / 2, screen_height / 2),
                queue=queue,
                anchor=DrawAnchor.CENTER,
                game_space=False
            )
            if self.__is_selling:
                self.__selling_render(queue)
            else:
                self.__buying_render(queue)

    def __set_trading(self, trader: Unit | None):
        is_trading = trader is not None
        self.__active_trader = trader
        if is_trading:
            self.__buying_send_event()
        else:
            Environment.event_manager.send(TradeStateEvent(state=TradeState.NONE))
        for group in [Groups.objects, Groups.player]:
            group.set_input_enabled(is_enabled=not is_trading, reason='trading_mode')
            group.set_update_enabled(is_enabled=not is_trading, reason='trading_mode')
            group.set_animation_enabled(is_enabled=not is_trading, reason='trading_mode')
        Groups.level.set_update_enabled(is_enabled=not is_trading, reason='trading_mode')

    def __switch_mode(self, is_selling: bool):
        if is_selling and not Environment.player.all_items:
            return
        self.__is_selling = is_selling
        if is_selling:
            self.__selling_send_event()
        else:
            self.__buying_send_event()

    def __selling_render(self, queue: DrawQueue):
        screen_width, screen_height = Screen.get_current_resolution()
        all_items = Environment.player.all_items
        HStack(
            children=[
                Grid(
                    children=[
                        AnimatedImage(
                            animated_object=item.get_animated_object(ItemType.inventory),
                            animation_type=AnimationType.PREVIEW
                        ) for index, item in enumerate(all_items)
                    ],
                    cell_size=self.__selling_grid_cell_size,
                    width=self.__selling_grid_width,
                    height=self.__selling_grid_height,
                    border_color=Colors.WHITE,
                    selected_cell=self.__selling_player_grid_selection()
                ),
                Rect(
                    size=(100, 100), # TODO: - Replace with something better
                ),
                Grid(
                    children=[
                        AnimatedImage(
                            animated_object=item.get_animated_object(ItemType.inventory),
                            animation_type=AnimationType.PREVIEW
                        ) for index, item in enumerate([])
                    ],
                    cell_size=self.__selling_grid_cell_size,
                    width=self.__selling_grid_width,
                    height=self.__selling_grid_height,
                    border_color=Colors.WHITE,
                    selected_cell=self.__selling_trader_grid_selection()
                )
            ],
            alignment=HStackAlignment.CENTER
        ).draw(
            position=(screen_width / 2, screen_height / 2),
            queue=queue,
            anchor=DrawAnchor.CENTER,
            game_space=False
        )

    def __selling_player_grid_selection(self) -> tuple[int, int] | None:
        if self.__selling_selection_x < self.__selling_grid_width:
            return self.__selling_selection_x, self.__selling_selection_y
        else:
            return None

    def __selling_trader_grid_selection(self) -> tuple[int, int] | None:
        if self.__selling_selection_x >= self.__selling_grid_width:
            return self.__selling_selection_x - self.__selling_grid_width, self.__selling_selection_y
        else:
            return None

    def __selling_send_event(self):
        index = self.__selling_selection_x + self.__selling_selection_y * self.__selling_grid_width
        all_items = Environment.player.all_items
        can_sell_item = index < len(all_items)
        Environment.event_manager.send(TradeStateEvent(state=TradeState.SELL, can_trade_now=can_sell_item))

    def __buying_render(self, queue: DrawQueue):
        for index, item in enumerate(self.__buying_items):
            coordinate = self.__buying_item_coordinate(index)
            VStack(
                children=[
                    ZStack(
                        children=[
                            AnimatedImage(
                                animated_object=item.get_animated_object(ItemType.store),
                                animation_type=AnimationType.PREVIEW
                            ),
                            Rect(
                                size=(self.__buying_item_size, self.__buying_item_size),
                                border=(4, Colors.YELLOW) if index == self.__buying_selection else None
                            )
                        ]
                    ),
                    Text(
                        text=item.description,
                        font=Fonts.blackcraft(size=36),
                        color=Colors.WHITE
                    )
                ]
            ).draw(
                position=coordinate,
                queue=queue,
                anchor=DrawAnchor.CENTER,
                game_space=False
            )

    @staticmethod
    def __buying_item_coordinate(index: int) -> tuple[float, float]:
        screen_width, screen_height = Screen.get_current_resolution()
        # Now works only for 3 items
        match index:
            case 0:
                return screen_width * 0.23125, screen_height * 0.85
            case 1:
                return screen_width * 0.78, screen_height * 0.85
            case 2:
                return screen_width * 0.5025, screen_height * 0.11667

    def __buying_selected_item(self):
        return self.__buying_items[self.__buying_selection]

    def __buying_send_event(self):
        selected_item = self.__buying_selected_item()
        can_buy_item = Environment.player.souls > selected_item.price
        Environment.event_manager.send(TradeStateEvent(state=TradeState.BUY, can_trade_now=can_buy_item))
