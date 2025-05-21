import pygame

from logic.core.render.color import Color
from logic.core.render.component import Component
from logic.core.render.surface import Surface, NativeSurface
from logic.core.render.types import Size
from logic.core.screen import Screen


class Rect(Component):
    def __init__(self, size: Size, color: Color | None = None, border: tuple[int, Color] | None = None, border_radius: int = 0):
        self.__size = size
        self.__color = color
        self.__border = border
        self.__border_radius = border_radius
        self.__surface: Surface | None = None
        super().__init__()

    def surface(self) -> Surface:
        screen_scale = Screen.get_screen_scale()
        scaled_size = (self.__size[0] * screen_scale, self.__size[1] * screen_scale)
        surface = pygame.Surface(scaled_size, pygame.SRCALPHA)
        if self.__color is not None and not self.__color.is_clear():
            pygame.draw.rect(surface, self.__color.color(), (0, 0, scaled_size[0], scaled_size[1]),
                             border_radius=self.__border_radius)
        if self.__border is not None:
            border_width, border_color = self.__border
            if not border_color.is_clear():
                pygame.draw.rect(surface, border_color.color(), (0, 0, scaled_size[0], scaled_size[1]), border_width,
                                 border_radius=self.__border_radius)
        return NativeSurface(surface=surface, identifier=self.__class__.__name__ + "(" + str(hash(self)) + ")")

    def __hash__(self):
        unpacked_border = (0, 0)
        if self.__border is not None:
            width, color = self.__border
            unpacked_border = (width, str(color))
        return hash((
            self.__size,
            str(self.__color),
            unpacked_border,
            self.__border_radius
        ))
