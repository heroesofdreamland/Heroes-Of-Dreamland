from typing import MutableSequence

import pygame

from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle import Lifecycle
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.render.components.text import Text
from logic.core.render.components.vstack import VStack
from logic.environment.environment import Environment, Groups
from logic.level_design.scenes.scenes import Scenes
from logic.ui.colors import Colors
from logic.ui.fonts import Fonts
from logic.core.screen import Screen


class MainMenuController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        self.__options = [
            "Start Game",
            "Settings",
            "Exit",
            "Modes(closed)",
        ]
        super().__init__(group=group)
        self.__current_option_index = 0
        self.__space_command_activated = False

    def process_input(self, events: MutableSequence):
        for event in events:
            if event.type == pygame.KEYDOWN:
                match event.scancode:
                    case pygame.KSCAN_W | pygame.KSCAN_UP:
                        self.__move_selection_up()
                    case pygame.KSCAN_S | pygame.KSCAN_DOWN:
                        self.__move_selection_down()
                    case pygame.KSCAN_SPACE | pygame.KSCAN_RETURN:
                        self.__space_command_activated = True

    def update(self):
        if self.__space_command_activated:
            self.__select_option()
            self.__space_command_activated = False

    def render(self, queue: DrawQueue):
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
        Text(
            text="x.com/H_o_Dreamland",
            font=Fonts.blackcraft(size=24),
            color=Colors.GRAY
        ).draw(
            position=(120, screen_height - 80),
            queue=queue
        )
        Text(
            text="Version 2.0.0",
            font=Fonts.blackcraft(size=24),
            color=Colors.GRAY
        ).draw(
            position=(75, screen_height - 30),
            queue=queue
        )

    def __move_selection_up(self):
        self.__current_option_index = (self.__current_option_index - 1) % len(self.__options)

    def __move_selection_down(self):
        self.__current_option_index = (self.__current_option_index + 1) % len(self.__options)

    def __select_option(self):
        match self.__current_option_index:
            case 0:
                Groups.reset()
                Environment.reset()
                Environment.scene_manager.activate(Scenes.HERO_SELECT_MENU.value)
            case 1:
                Environment.scene_manager.activate(Scenes.SETTINGS.value)
            case 2:
                pygame.quit()
                quit()