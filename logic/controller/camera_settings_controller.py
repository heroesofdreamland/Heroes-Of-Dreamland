from typing import MutableSequence

import pygame

from logic.core.camera import Camera
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


class CameraSettingsController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)
        self.__current_preset_index = 0

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
                        self.__select_camera_preset()
                    case pygame.KSCAN_ESCAPE:
                        Environment.scene_manager.activate(Scenes.SETTINGS.value)

    def render(self, queue: DrawQueue):
        screen_width, screen_height = Screen.get_current_resolution()

        available_camera_presets = Camera.get_available_box_presets()
        VStack(
            children=[
                Text(
                    text=f"{int(preset[0] * 100)}%",
                    font=Fonts.blackcraft(36),
                    color=Colors.WHITE if index == self.__current_preset_index else Colors.GRAY
                ) for index, preset in enumerate(available_camera_presets)
            ]
        ).draw(
            position=(screen_width / 2, screen_height / 2),
            queue=queue
        )

    def __select_camera_preset(self):
        selected_preset = Camera.get_available_box_presets()[self.__current_preset_index]
        Camera.set_box_preset(selected_preset)

    def __settings_selection_up(self):
        self.__current_preset_index = (self.__current_preset_index - 1) % len(Camera.get_available_box_presets())

    def __settings_selection_down(self):
        self.__current_preset_index = (self.__current_preset_index + 1) % len(Camera.get_available_box_presets())
