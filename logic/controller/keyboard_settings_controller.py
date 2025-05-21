from copy import deepcopy
from typing import MutableSequence

import pygame

from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.lifecycle import Lifecycle
from logic.core.render.color import Color
from logic.core.render.components.text import Text
from logic.core.render.components.vstack import VStack
from logic.environment.environment import Environment
from logic.level_design.scenes.scenes import Scenes
from logic.ui.colors import Colors
from logic.ui.fonts import Fonts
from logic.settings.key_settings import KeySettings
from logic.core.screen import Screen


class KeyboardSettingsController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)
        self.__current_key_index = 0
        self.__editing_key = None
        self.__current_key_settings = deepcopy(KeySettings.get_current_settings())

    def process_input(self, events: MutableSequence):
        for event in events:
            if event.type == pygame.KEYDOWN:
                scancode = event.scancode

                if self.__editing_key is not None:
                    self.__edit_key(scancode)
                else:
                    match scancode:
                        case pygame.KSCAN_W | pygame.KSCAN_UP:
                            self.__settings_selection_up()
                        case pygame.KSCAN_S | pygame.KSCAN_DOWN:
                            self.__settings_selection_down()
                        case pygame.KSCAN_R:
                            if self.__editing_key is None:
                                self.__reset_keys()
                        case pygame.KSCAN_SPACE | pygame.KSCAN_RETURN:
                            self.__editing_key = list(self.__current_key_settings.keys())[self.__current_key_index]
                        case pygame.KSCAN_ESCAPE:
                            if self.__are_all_keys_assigned():
                                KeySettings.update(new_keys=self.__current_key_settings)
                                Environment.scene_manager.activate(Scenes.SETTINGS.value)

    def render(self, queue: DrawQueue):
        screen_width, screen_height = Screen.get_current_resolution()
        VStack(
            children=[
                Text(
                    text=f"{key}: {KeySettings.get_value_for_scancode(self.__current_key_settings[key])}",
                    font=Fonts.blackcraft(25),
                    color=self.__text_color(index=index, key=key)
                ) for index, key in enumerate(self.__current_key_settings)
            ]
        ).draw(
            position=(screen_width / 2, screen_height / 2),
            queue=queue
        )

    def __text_color(self, index: int, key: str) -> Color:
        return Colors.WHITE if index == self.__current_key_index else Colors.GRAY if self.__current_key_settings[key] is not None else Colors.RED

    def __edit_key(self, scan_code: int):
        if scan_code in KeySettings.get_possible_keys():
            for existing_key_name, assigned_key in self.__current_key_settings.items():
                if assigned_key == scan_code and existing_key_name != self.__editing_key:
                    self.__current_key_settings[existing_key_name] = None
            if self.__editing_key in self.__current_key_settings:
                self.__current_key_settings[self.__editing_key] = scan_code
        self.__editing_key = None

    def __reset_keys(self):
        KeySettings.update(KeySettings.get_defaults_keys())
        self.__current_key_settings = deepcopy(KeySettings.get_current_settings())

    def __are_all_keys_assigned(self) -> bool:
        for key, value in self.__current_key_settings.items():
            if value is None:
                return False
        return True

    def __settings_selection_up(self):
        self.__current_key_index = (self.__current_key_index - 1) % len(self.__current_key_settings)

    def __settings_selection_down(self):
        self.__current_key_index = (self.__current_key_index + 1) % len(self.__current_key_settings)
