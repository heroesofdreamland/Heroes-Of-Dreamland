from typing import cast

import pygame

from logic.core.db_service import DBService
from logic.core.opengl import OpenGL


class Screen:
    __available_resolutions = [
        (1280, 720),
        (1280, 800),
        (1440, 900),
        (1600, 900),
        (1680, 1050),
        (1920, 1080),
        (1920, 1200),
        (2048, 1152),
        (2560, 1440),
        (0, 0)
    ]

    __default_resolution = (1920, 1080)
    __cached_resolution: tuple[int, int] | None = None
    __cached_scale = 1
    __resolution_data_path = 'resources/game_data/resolution_data'

    @staticmethod
    def __update_screen(resolution: tuple[int, int], is_fullscreen: bool):
        flags = pygame.DOUBLEBUF | pygame.OPENGL
        if is_fullscreen:
            flags |= pygame.FULLSCREEN
        pygame.display.quit()
        new_screen = pygame.display.set_mode(size=resolution, flags=flags)
        OpenGL.configure(screen_size=new_screen.get_size())
        screen_width, screen_height = OpenGL.get_viewport_size()
        reference_width, reference_height = (800, 600)
        Screen.__cached_scale = int(min(screen_width / reference_width, screen_height / reference_height))
        Screen.__cached_resolution = None

    @staticmethod
    def __is_fullscreen(resolution: tuple[int, int]) -> bool:
        return resolution == (0, 0)

    @staticmethod
    def initialize():
        try:
            resolution = cast(tuple[int, int], DBService.select_data("resolution", Screen.__resolution_data_path))
            Screen.__update_screen(resolution, Screen.__is_fullscreen(resolution=resolution))
        except KeyError:
            Screen.__update_screen(Screen.__default_resolution, Screen.__is_fullscreen(resolution=Screen.__default_resolution))
        pygame.display.set_caption("Heroes of Dreamland")

    @staticmethod
    def set_resolution(resolution: tuple[int, int]):
        if resolution in Screen.__available_resolutions:
            DBService.insert_data("resolution", resolution, Screen.__resolution_data_path)
            Screen.__update_screen(resolution, Screen.__is_fullscreen(resolution=resolution))
        else:
            raise ValueError(f"Resolution {resolution} is not available in the predefined list.")

    @staticmethod
    def get_current_resolution() -> tuple[int, int]:
        if Screen.__cached_resolution is None:
            Screen.__cached_resolution = OpenGL.get_viewport_size()
        return Screen.__cached_resolution

    @staticmethod
    def get_available_resolutions() -> list:
        return Screen.__available_resolutions

    @staticmethod
    def get_screen_scale() -> int:
        return Screen.__cached_scale

