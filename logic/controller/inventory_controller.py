from typing import MutableSequence

import pygame

from logic.core.animated_object import AnimatedObject
from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle import Lifecycle
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.render.component import Component
from logic.core.render.components.animated_image import AnimatedImage
from logic.core.render.components.grid import Grid
from logic.core.render.components.hstack import HStack
from logic.core.render.components.rect import Rect
from logic.core.render.components.text import Text
from logic.core.render.components.vstack import VStack, VStackAlignment
from logic.core.render.components.zstack import ZStack, ZStackAlignment
from logic.core.screen import Screen
from logic.environment.environment import Groups, Environment
from logic.events.inventory_state_event import InventoryStateEvent
from logic.entities.items.item import ItemType, Item
from logic.ui.colors import Colors
from logic.ui.fonts import Fonts
from logic.settings.key_settings import KeySettings
from logic.utils.screen_dimmer import ScreenDimmer
from logic.entities.units.models.animation_type import AnimationType


class InventoryController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)
        self.__is_inventory_opened = False
        self.__main_grid_width = 10
        self.__main_grid_height = 5
        self.__active_grid_height = 5
        self.__hero_slot_width = 3
        self.__selected_x = 0
        self.__selected_y = 0
        self.__cell_size = 48
        self.__screen_dimmer = ScreenDimmer()
        self.__player_animated_object: AnimatedObject | None = None

    def process_input(self, events: MutableSequence):
        for event in events:
            if event.type == pygame.KEYDOWN:
                match event.scancode:
                    case pygame.KSCAN_ESCAPE:
                        if self.__is_inventory_opened:
                            self.__set_inventory_opened(is_inventory_opened=False)
                            events.remove(event)
                    case pygame.KSCAN_I:
                        if not self.__is_inventory_opened:
                            self.__set_inventory_opened(is_inventory_opened=True)
                    case pygame.KSCAN_W | pygame.KSCAN_UP:
                        if self.__is_inventory_opened:
                            if self.__selected_x == 0 or self.__selected_x == self.__hero_slot_width + 1:
                                self.__selected_y = (self.__selected_y + self.__main_grid_height + self.__active_grid_height - 1) % (self.__main_grid_height + self.__active_grid_height)
                            else:
                                if self.__selected_y == self.__active_grid_height:
                                    self.__selected_y = self.__active_grid_height + self.__main_grid_height - 1
                                else:
                                    self.__selected_y -= 1
                    case pygame.KSCAN_S | pygame.KSCAN_DOWN:
                        if self.__is_inventory_opened:
                            if self.__selected_x == 0 or self.__selected_x == self.__hero_slot_width + 1:
                                self.__selected_y = (self.__selected_y + 1) % (self.__main_grid_height + self.__active_grid_height)
                            else:
                                if self.__selected_y == self.__active_grid_height + self.__main_grid_height - 1:
                                    self.__selected_y = self.__active_grid_height
                                else:
                                    self.__selected_y += 1
                    case pygame.KSCAN_D | pygame.KSCAN_RIGHT:
                        if self.__is_inventory_opened:
                            if self.__selected_y < self.__active_grid_height:
                                if self.__selected_x == 0:
                                    self.__selected_x = self.__hero_slot_width + 1
                                else:
                                    self.__selected_x = 0
                            else:
                                self.__selected_x = (self.__selected_x + 1) % self.__main_grid_width # Переключаемся горизонтально между главным Grid
                    case pygame.KSCAN_A | pygame.KSCAN_LEFT:
                        if self.__is_inventory_opened:
                            if self.__selected_y < self.__active_grid_height:
                                if self.__selected_x == 0:
                                    self.__selected_x = self.__hero_slot_width + 1
                                else:
                                    self.__selected_x = 0
                            else:
                                self.__selected_x = (self.__selected_x + self.__main_grid_width - 1) % self.__main_grid_width # Переключаемся горизонтально между главным Grid

    def render(self, queue: DrawQueue):
        if self.__is_inventory_opened:
            self.__screen_dimmer.render(queue=queue)
            screen_width, screen_height = Screen.get_current_resolution()
            active_items = Environment.player.active_items
            passive_items = Environment.player.passive_items
            VStack(
                children=[
                    HStack(
                        children=[
                            Grid(
                                children=[
                                    self.__item_component(item=item, index=index) for index, item in enumerate(active_items[:5])
                                ],
                                cell_size=self.__cell_size,
                                width=1,
                                height=self.__active_grid_height,
                                border_color=Colors.WHITE,
                                selected_cell=self.__left_active_grid_selected_cell()
                            ),
                            ZStack(
                                children=[
                                    Rect(
                                        size=(self.__hero_slot_width * self.__cell_size, self.__active_grid_height * self.__cell_size)
                                    ),
                                    AnimatedImage(
                                        animated_object=self.__player_animated_object,
                                        animation_type=AnimationType.IDLE
                                    )
                                ]
                            ),
                            Grid(
                                children=[
                                    self.__item_component(item=item, index=index + 5) for index, item in enumerate(active_items[5:10])
                                ],
                                cell_size=self.__cell_size,
                                width=1,
                                height=self.__active_grid_height,
                                border_color=Colors.WHITE,
                                selected_cell=self.__right_active_grid_selected_cell()
                            )
                        ]
                    ),
                    Grid(
                        children=[
                            AnimatedImage(
                                animated_object=item.get_animated_object(ItemType.inventory),
                                animation_type=AnimationType.PREVIEW
                            ) for item in passive_items
                        ],
                        cell_size=self.__cell_size,
                        width=self.__main_grid_width,
                        height=self.__main_grid_height,
                        border_color=Colors.WHITE,
                        selected_cell=self.__main_grid_selected_cell()
                    )
                ],
                alignment=VStackAlignment.START
            ).draw(
                position=(screen_width / 2, screen_height / 2),
                queue=queue
            )

    @staticmethod
    def __item_component(item: Item, index: int) -> Component:
        return ZStack(
            children=[
                AnimatedImage(
                    animated_object=item.get_animated_object(ItemType.inventory),
                    animation_type=AnimationType.PREVIEW
                ),
                ZStack(
                    children=[
                        Rect(
                            size=(18, 18),
                            color=Colors.WHITE,
                            border=(1, Colors.BLACK),
                            border_radius=4
                        ),
                        Text(
                            text=KeySettings.get_value_for_scancode(KeySettings.get_key('SLOT_' + str(index + 1))),
                            font=Fonts.blackcraft(14),
                            color=Colors.BLACK
                        )
                    ]
                )
            ],
            alignment=ZStackAlignment.TOP_RIGHT
        )

    def __set_inventory_opened(self, is_inventory_opened: bool):
        self.__is_inventory_opened = is_inventory_opened
        Environment.event_manager.send(InventoryStateEvent(is_opened=is_inventory_opened))
        for group in [Groups.objects, Groups.player]:
            group.set_input_enabled(is_enabled=not self.__is_inventory_opened, reason='inventory_opened')
            group.set_update_enabled(is_enabled=not self.__is_inventory_opened, reason='inventory_opened')
            group.set_animation_enabled(is_enabled=not self.__is_inventory_opened, reason='inventory_opened')
        Groups.level.set_update_enabled(is_enabled=not self.__is_inventory_opened, reason='inventory_opened')
        if is_inventory_opened:
            self.__player_animated_object = Environment.player.model.build_animated_object(scale=1.4)
        else:
            self.__player_animated_object = None

    def __left_active_grid_selected_cell(self) -> tuple[int, int] | None:
        if self.__selected_y < self.__active_grid_height and self.__selected_x == 0:
            return 0, self.__selected_y
        else:
            return None

    def __right_active_grid_selected_cell(self) -> tuple[int, int] | None:
        if self.__selected_y < self.__active_grid_height and self.__selected_x == self.__hero_slot_width + 1:
            return 0, self.__selected_y
        else:
            return None

    def __main_grid_selected_cell(self) -> tuple[int, int] | None:
        if self.__selected_y >= self.__active_grid_height:
            return self.__selected_x, self.__selected_y - self.__active_grid_height
        else:
            return None
