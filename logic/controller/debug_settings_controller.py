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
from logic.settings.debug_settings import DebugSettings
from logic.ui.fonts import Fonts
from logic.core.screen import Screen


class DebugSettingsController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)
        self.__current_debug_option_index = 0
        self.debug_option_names = list(DebugSettings.debug_settings.keys())

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
                        self.__toggle_debug_setting()
                    case pygame.KSCAN_ESCAPE:
                        Environment.scene_manager.activate(Scenes.SETTINGS.value)

    def render(self, queue: DrawQueue):
        screen_width, screen_height = Screen.get_current_resolution()
        VStack(
            children=[
                Text(
                    text=f"{key}: {DebugSettings.debug_settings[key]}",
                    font=Fonts.blackcraft(36),
                    color=Colors.WHITE if index == self.__current_debug_option_index else Colors.GRAY
                ) for index, key in enumerate(DebugSettings.debug_settings.keys())
            ]
        ).draw(
            position=(screen_width / 2, screen_height / 2),
            queue=queue
        )

    def __toggle_debug_setting(self):
        for debug_option_key in DebugSettings.debug_settings.keys():
            if debug_option_key == self.debug_option_names[self.__current_debug_option_index]:
                DebugSettings.debug_settings[debug_option_key] = not DebugSettings.debug_settings[debug_option_key]


    def __settings_selection_up(self):
        self.__current_debug_option_index = (self.__current_debug_option_index - 1) % len(self.debug_option_names)

    def __settings_selection_down(self):
        self.__current_debug_option_index = (self.__current_debug_option_index + 1) % len(self.debug_option_names)
