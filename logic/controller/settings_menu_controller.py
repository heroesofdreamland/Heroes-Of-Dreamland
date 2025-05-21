from typing import MutableSequence

import pygame

from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.lifecycle import Lifecycle
from logic.core.render.components.text import Text
from logic.core.render.components.vstack import VStack
from logic.environment.environment import Environment
from logic.level_design.scenes.scenes import Scenes
from logic.ui.colors import Colors
from logic.ui.fonts import Fonts
from logic.core.screen import Screen


class SettingsMenuController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)
        self.__options = ['Keyboard', 'Screen', 'Camera', 'Debug']
        self.__current_option_index = 0

    def process_input(self, events: MutableSequence):
        for event in events:
            if event.type == pygame.KEYDOWN:
                scancode = event.scancode

                match scancode:
                    case pygame.KSCAN_W | pygame.KSCAN_UP:
                        self.__move_option_up()
                    case pygame.KSCAN_S | pygame.KSCAN_DOWN:
                        self.__move_option_down()
                    case pygame.KSCAN_SPACE | pygame.KSCAN_RETURN:
                        self.__select_option()
                    case pygame.KSCAN_ESCAPE:
                        Environment.scene_manager.activate(Scenes.MAIN_MENU.value)

    def render(self, queue: DrawQueue):
        screen_width, screen_height = Screen.get_current_resolution()

        VStack(
            children=[
                Text(
                    text=option,
                    font=Fonts.blackcraft(36),
                    color=Colors.WHITE if index == self.__current_option_index else Colors.GRAY
                ) for index, option in enumerate(self.__options)
            ],
            spacing=20
        ).draw(
            position=(screen_width / 2, screen_height / 2),
            queue=queue
        )

    def __select_option(self):
        match self.__current_option_index:
            case 0:
                Environment.scene_manager.activate(Scenes.KEYBOARD_SETTINGS.value)
            case 1:
                Environment.scene_manager.activate(Scenes.RESOLUTION_SETTINGS.value)
            case 2:
                Environment.scene_manager.activate(Scenes.CAMERA_SETTINGS.value)
            case 3:
                Environment.scene_manager.activate(Scenes.DEBUG_SETTINGS.value)

    def __move_option_up(self):
        self.__current_option_index = (self.__current_option_index - 1) % len(self.__options)

    def __move_option_down(self):
        self.__current_option_index = (self.__current_option_index + 1) % len(self.__options)
