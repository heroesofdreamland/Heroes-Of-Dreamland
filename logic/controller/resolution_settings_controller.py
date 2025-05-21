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


class ResolutionSettingsController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)
        self.__current_resolution_index = 0

    def process_input(self, events: MutableSequence):
        for event in events:
            if event.type == pygame.KEYDOWN:
                scancode = event.scancode

                match scancode:
                    case pygame.KSCAN_W | pygame.KSCAN_UP:
                        self.__settings_selection_up()
                    case pygame.KSCAN_S | pygame.KSCAN_DOWN:
                        self.__settings_selection_down()
                    case pygame.KSCAN_SPACE | pygame.KSCAN_RETURN:
                        self.__select_resolution()
                    case pygame.KSCAN_ESCAPE:
                        Environment.scene_manager.activate(Scenes.SETTINGS.value)

    def render(self, queue: DrawQueue):
        screen_width, screen_height = Screen.get_current_resolution()

        available_resolutions = Screen.get_available_resolutions()
        VStack(
            children=[
                Text(
                    text=f"{resolution[0]}x{resolution[1]}" if resolution != (0, 0) else "Fullscreen",
                    font=Fonts.blackcraft(36),
                    color=Colors.WHITE if index == self.__current_resolution_index else Colors.GRAY
                ) for index, resolution in enumerate(available_resolutions)
            ]
        ).draw(
            position=(screen_width / 2, screen_height / 2),
            queue=queue
        )

    def __select_resolution(self):
        selected_resolution = Screen.get_available_resolutions()[self.__current_resolution_index]
        Screen.set_resolution(selected_resolution)

    def __settings_selection_up(self):
        self.__current_resolution_index = (self.__current_resolution_index - 1) % len(Screen.get_available_resolutions())

    def __settings_selection_down(self):
        self.__current_resolution_index = (self.__current_resolution_index + 1) % len(Screen.get_available_resolutions())
