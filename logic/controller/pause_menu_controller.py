from typing import MutableSequence

import pygame

from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.lifecycle import Lifecycle
from logic.core.render.components.text import Text
from logic.core.render.components.vstack import VStack
from logic.environment.environment import Environment, Groups
from logic.level_design.scenes.scenes import Scenes
from logic.ui.colors import Colors
from logic.ui.fonts import Fonts
from logic.core.screen import Screen
from logic.utils.screen_dimmer import ScreenDimmer


class PauseMenuController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)
        self.__options = ["Restart", "Exit to Main Menu"]
        self.__current_option_index = 0
        self.__game_is_paused = False
        self.__space_command_activated = False
        self.__screen_dimmer = ScreenDimmer()

    def process_input(self, events: MutableSequence):
        for event in events:
            if event.type == pygame.KEYDOWN:
                match event.scancode:
                    case pygame.KSCAN_ESCAPE:
                        self.__set_game_paused(is_paused=not self.__game_is_paused)
                    case pygame.KSCAN_W | pygame.KSCAN_UP:
                        if self.__game_is_paused:
                            self.__move_selection_up()
                    case pygame.KSCAN_S | pygame.KSCAN_DOWN:
                        if self.__game_is_paused:
                            self.__move_selection_down()
                    case pygame.KSCAN_SPACE | pygame.KSCAN_RETURN:
                        if self.__game_is_paused:
                            self.__space_command_activated = True

    def update(self):
        if self.__space_command_activated:
            self.__select_option()
            self.__space_command_activated = False

    def render(self, queue: DrawQueue):
        if self.__game_is_paused:
            self.__screen_dimmer.render(queue=queue)
            screen_width, screen_height = Screen.get_current_resolution()
            VStack(
                children=[
                    Text(
                        text=option,
                        font=Fonts.blackcraft(size=36),
                        color=Colors.WHITE if self.__current_option_index == index else Colors.GRAY
                    ) for index, option in enumerate(self.__options)
                ],
                spacing=20
            ).draw(
                position=(screen_width / 2, screen_height / 2),
                queue=queue
            )

    def __move_selection_up(self):
        self.__current_option_index = (self.__current_option_index - 1) % len(self.__options)

    def __move_selection_down(self):
        self.__current_option_index = (self.__current_option_index + 1) % len(self.__options)

    def __select_option(self):
        Groups.reset()
        Environment.reset()
        match self.__current_option_index:
            case 0:
                Environment.scene_manager.activate(Scenes.HERO_SELECT_MENU.value)
            case 1:
                Environment.scene_manager.activate(Scenes.MAIN_MENU.value)

    def __set_game_paused(self, is_paused: bool):
        self.__game_is_paused = is_paused
        for group in [Groups.objects, Groups.player]:
            group.set_input_enabled(is_enabled=not self.__game_is_paused, reason='game_paused')
            group.set_update_enabled(is_enabled=not self.__game_is_paused, reason='game_paused')
            group.set_animation_enabled(is_enabled=not self.__game_is_paused, reason='game_paused')
        Groups.level.set_update_enabled(is_enabled=not self.__game_is_paused, reason='game_paused')

