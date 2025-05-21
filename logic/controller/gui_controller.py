from typing import cast, MutableSequence

import pygame
from pymunk import Vec2d

from logic.entities.abilities.manual_attack_ability import ManualAttackAbility
from logic.core.draw_queue import DrawQueue, DrawAnchor
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.lifecycle import Lifecycle
from logic.core.render.component import Component
from logic.core.render.components.animated_image import AnimatedImage
from logic.core.render.components.grid import Grid
from logic.core.render.components.hstack import HStack
from logic.core.render.components.margin import Margin
from logic.core.render.components.rect import Rect
from logic.core.render.components.text import Text
from logic.core.render.components.vstack import VStack, VStackAlignment
from logic.core.render.components.zstack import ZStack, ZStackAlignment
from logic.environment.environment import Environment, Groups
from logic.entities.items.item import ItemType, Item
from logic.level_design.scenes.scenes import Scenes
from logic.ui.colors import Colors
from logic.ui.fonts import Fonts
from logic.core.screen import Screen
from logic.settings.key_settings import KeySettings
from logic.entities.units.data.unit_life_state import UnitLifeState
from logic.entities.units.models.animation_type import AnimationType
from logic.entities.units.unit_factory import generate_unit, UnitGroup


# GuiController responsibilities:
# - Rendering the user interface (health, buttons and others)
class GuiController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)
        self.__player_animated_object = Environment.player.animation_model.build_animated_object()
        self.__should_restart_game = False

    def process_input(self, events: MutableSequence):
        if Environment.player.life_state == UnitLifeState.DEATH:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    match event.scancode:
                        case pygame.KSCAN_SPACE | pygame.KSCAN_RETURN:
                            self.__should_restart_game = True

    def update(self):
        if self.__should_restart_game:
            Groups.reset()
            hero_type = type(Environment.player)
            Environment.reset()
            generate_unit(unit_type=hero_type, coordinate=Vec2d(x=0, y=0), group=UnitGroup.PLAYER)
            Environment.scene_manager.activate(Scenes.MAIN_GAMEPLAY.value)

    def render(self, queue: DrawQueue):
        screen_width, screen_height = Screen.get_current_resolution()
        match Environment.player.life_state:
            case UnitLifeState.DEATH:
                self.__render_game_over_text(queue=queue)
            case UnitLifeState.ALIVE:
                self.__render_player_panel(screen_width=screen_width,
                                           screen_height=screen_height,
                                           queue=queue)
                self.__render_orders(queue=queue)

    def __render_player_panel(self,
                              screen_width: float,
                              screen_height: float,
                              queue: DrawQueue):
        center_panel_width = 100 * Screen.get_screen_scale()
        full_panels_width = 600 * Screen.get_screen_scale()
        panels_height = 120 * Screen.get_screen_scale()
        side_width = (full_panels_width - center_panel_width) // 2

        HStack(
            children=[
                ZStack(
                    children=[
                        Rect(
                            size=(side_width, panels_height),
                            color=Colors.BLACK
                        ),
                        Margin(
                            child=VStack(
                                children=[
                                    Text(
                                        text="Souls: " + str(Environment.player.souls),
                                        font=Fonts.blackcraft(size=20),
                                        color=Colors.WHITE
                                    ),
                                    Text(
                                        text="Speed: " + str(Environment.player.speed),
                                        font=Fonts.blackcraft(size=20),
                                        color=Colors.WHITE
                                    ),
                                    Text(
                                        text="Damage: " + str(cast(ManualAttackAbility, Environment.player.ability(ManualAttackAbility)).damage_data.damage),
                                        font=Fonts.blackcraft(size=20),
                                        color=Colors.WHITE
                                    ),
                                    Text(
                                        text="Armor: " + str(Environment.player.armor),
                                        font=Fonts.blackcraft(size=20),
                                        color=Colors.WHITE
                                    )
                                ],
                                spacing=0,
                                alignment=VStackAlignment.START
                            ),
                            left=8,
                            right=8,
                            top=8,
                            bottom=8
                        )
                    ],
                    alignment=ZStackAlignment.TOP_LEFT
                ),
                ZStack(
                    children=[
                        Rect(
                            size=(center_panel_width, panels_height),
                            color=Colors.GREEN
                        ),
                        AnimatedImage(
                            animated_object=self.__player_animated_object,
                            animation_type=AnimationType.IDLE
                        )
                    ]
                ),
                ZStack(
                    children=[
                        Rect(
                            size=(side_width, panels_height),
                            color=Colors.BLACK
                        ),
                        Margin(
                            child=Grid(
                                children=[
                                    self.__item_component(item=item, index=index, size=40) for index, item in enumerate(Environment.player.active_items)
                                ],
                                cell_size=40,
                                width=5,
                                height=2,
                                border_color=Colors.CLEAR
                            ),
                            left=8,
                            right=8,
                            top=8,
                            bottom=8
                        )
                    ],
                    alignment=ZStackAlignment.TOP_LEFT
                )
            ]
        ).draw(
            position=(screen_width / 2, screen_height),
            queue=queue,
            anchor=DrawAnchor.BOTTOM_CENTER,
            game_space=False
        )

    @staticmethod
    def __item_component(item: Item, index: int, size: float) -> Component:
        cooldown = item.cooldown()
        can_activate = item.can_activate(owner=Environment.player) and cooldown is None
        return ZStack(
            children=[
                AnimatedImage(
                    animated_object=item.get_animated_object(ItemType.gui),
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
                ),
                ZStack(
                    children=[
                        Rect(
                            size=(size, size),
                            color=Colors.SEMITRANSPARENT if not can_activate else None
                        )
                    ] + ([
                        Text(
                            text="%.1f" % cooldown,
                            font=Fonts.blackcraft(size=20),
                            color=Colors.WHITE
                        )
                    ] if cooldown is not None else []),
                )
            ],
            alignment=ZStackAlignment.TOP_RIGHT
        )

    @staticmethod
    def __render_game_over_text(queue: DrawQueue):
        screen_width, screen_height = Screen.get_current_resolution()
        Text(
            text="You died",
            font=Fonts.blackcraft(size=50),
            color=Colors.WHITE
        ).draw(
            position=(screen_width / 2, screen_height / 2),
            queue=queue,
            anchor=DrawAnchor.CENTER,
            game_space=False
        )

    @staticmethod
    def __render_orders(queue: DrawQueue):
        if Environment.orders:
            screen_width, screen_height = Screen.get_current_resolution()
            Margin(
                child=VStack(
                    children=[
                        Text(
                            text=f'{order.name}\n{order.description}\n{order.progress}',
                            font=Fonts.blackcraft(20),
                            color=Colors.WHITE
                        ) for order in Environment.orders
                    ],
                    spacing=20
                ),
                left=20
            ).draw(
                position=(0, screen_height / 2),
                queue=queue,
                anchor=DrawAnchor.CENTER_LEFT
            )
