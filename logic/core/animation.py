import pygame

from logic.core.opengl import OpenGL, Texture
from logic.core.resource_cache import cached_image
from logic.core.screen import Screen


class Animation:
    def __init__(self,
                 path: str,
                 count: int,
                 duration: float,
                 speed: float = 1,
                 repeat: bool = True):
        self.__path = path
        self.__count = count
        self.__duration = duration
        self.speed = speed
        self.repeat = repeat

    def get_frames_count(self) -> int:
        return self.__count

    def get_duration(self) -> float:
        return self.__duration / self.speed

    def get_texture(self, index: int, scale: float, mirrored: bool) -> Texture:
        scale = scale * Screen.get_screen_scale() # TODO: - Optimize performance
        return OpenGL.image_texture(path=self.__get_path(index=index), scale=scale, mirrored=mirrored)

    def get_image(self, index: int, scale: float, mirrored: bool) -> pygame.Surface:
        scale = scale * Screen.get_screen_scale()  # TODO: - Optimize performance
        return cached_image(path=self.__get_path(index=index), mirrored=mirrored, scale=scale)

    def get_base_path(self) -> str:
        return self.__path

    def __get_path(self, index: int) -> str:
        return self.__path + '/' + str(index).zfill(3) + '.png'
