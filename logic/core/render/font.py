import pygame

from logic.core.render.color import Color
from logic.core.resource_cache import cached_font


class Font:
    def __init__(self, name: str, size: int):
        self.__name = name
        self.__size = size
        self.__font = cached_font(path='resources/used_resources/fonts/' + name + '.ttf', size=size)

    def __hash__(self):
        return hash((self.__name, self.__size))

    def __repr__(self):
        return self.__name + "(" + str(self.__size) + ")"

    def render(self, text: str, color: Color) -> pygame.Surface:
        return self.__font.render(text, True, color.color())
