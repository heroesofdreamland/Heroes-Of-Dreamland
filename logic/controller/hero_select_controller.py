from typing import MutableSequence

import pygame
from pymunk import Vec2d

from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.lifecycle import Lifecycle
from logic.core.render.components.animated_image import AnimatedImage
from logic.core.render.components.hstack import HStack, HStackAlignment
from logic.core.render.components.opacity import Opacity
from logic.core.render.components.text import Text
from logic.core.render.components.vstack import VStack, VStackAlignment
from logic.core.screen import Screen
from logic.entities.units.models.player_characters.kron.kron import Kron
from logic.entities.units.models.player_characters.kron.kron_animation_model import KronAnimationModel
from logic.environment.environment import Environment
from logic.level_design.scenes.scenes import Scenes
from logic.ui.colors import Colors
from logic.ui.fonts import Fonts
from logic.entities.units.unit_factory import generate_unit, UnitGroup
from logic.entities.units.models.animation_type import AnimationType
from logic.entities.units.models.player_characters.master_of_the_seven.mots_animation_model import MasterOfTheSevenAnimationModel
from logic.entities.units.models.player_characters.master_of_the_seven.mots import MasterOfTheSeven
from logic.entities.units.models.player_characters.soboro.soboro import Soboro
from logic.entities.units.models.player_characters.soboro.soboro_animation_model import SoboroAnimationModel


class HeroSelectionController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        self.heroes = [
            (Soboro, 'Soboro', SoboroAnimationModel().build_animated_object(scale=3)),
            (MasterOfTheSeven, 'Master of the seven', MasterOfTheSevenAnimationModel().build_animated_object(scale=3)),
            (Kron, 'Kron', KronAnimationModel().build_animated_object(scale=3))
        ]
        self.current_hero_index = 0
        super().__init__(group=group)
        self.__space_command_activated = False

    def process_input(self, events: MutableSequence):
        for event in events:
            if event.type == pygame.KEYDOWN:
                match event.scancode:
                    case pygame.KSCAN_A | pygame.KSCAN_LEFT:
                        self.__move_selection_left()
                    case pygame.KSCAN_D | pygame.KSCAN_RIGHT:
                        self.__move_selection_right()
                    case pygame.KSCAN_SPACE | pygame.KSCAN_RETURN:
                        self.__space_command_activated = True
                    case pygame.KSCAN_ESCAPE:
                        Environment.scene_manager.activate(Scenes.MAIN_MENU.value)

    def update(self):
        if self.__space_command_activated:
            self.__select_current_hero()
            self.__space_command_activated = False

    def render(self, queue: DrawQueue):
        screen_width, screen_height = Screen.get_current_resolution()
        visible_heroes = self.__get_visible_heroes()

        hero_avatars = [Opacity(
            child=VStack(
                children=[
                    AnimatedImage(
                        animated_object=hero[2],
                        animation_type=AnimationType.IDLE
                    ),
                    Text(
                        text=hero[1],
                        font=Fonts.blackcraft(36),
                        color=Colors.WHITE if index == 1 else Colors.CLEAR
                    )
                ],
                alignment=VStackAlignment.CENTER
            ),
            opacity=1 if index == 1 else 0.3
        ) for index, hero in enumerate(visible_heroes)]

        offset = (hero_avatars[0].surface().get_size()[0] - hero_avatars[2].surface().get_size()[0]) / 2

        HStack(
            children=hero_avatars,
            spacing=24,
            alignment=HStackAlignment.BOTTOM
        ).draw(
            position=(screen_width / 2 - offset, screen_height / 2),
            queue=queue,
        )

    def __move_selection_left(self):
        self.current_hero_index = (self.current_hero_index - 1) % len(self.heroes)

    def __move_selection_right(self):
        self.current_hero_index = (self.current_hero_index + 1) % len(self.heroes)

    def __select_current_hero(self):
        generate_unit(unit_type=self.heroes[self.current_hero_index][0], coordinate=Vec2d(x=0, y=0), group=UnitGroup.PLAYER)
        Environment.scene_manager.activate(Scenes.MAIN_GAMEPLAY.value)

    def __get_visible_heroes(self):
        total_heroes = len(self.heroes)
        left_index = (self.current_hero_index - 1) % total_heroes
        right_index = (self.current_hero_index + 1) % total_heroes

        left_hero = (self.heroes[left_index])
        center_hero = (self.heroes[self.current_hero_index])
        right_hero = (self.heroes[right_index])

        return [left_hero, center_hero, right_hero]
