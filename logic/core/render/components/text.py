import pygame

from logic.core.render.color import Color
from logic.core.render.component import Component
from logic.core.render.font import Font
from logic.core.render.surface import Surface, NativeSurface, ContainerSurface


class Text(Component):
    __text_cache: dict[tuple[str, str, str], Surface] = {}

    def __init__(self, text: str, font: Font, color: Color):
        self.__text = text
        self.__font = font
        self.__color = color
        self.__surface = self.__prepare_text()
        super().__init__()

    def surface(self) -> Surface:
        return self.__surface

    def __prepare_text(self) -> Surface:
        key = self.__text, str(self.__font), str(self.__color)
        if key in Text.__text_cache:
            return Text.__text_cache[key]
        lines = self.__text.splitlines()
        if len(lines) <= 1:
            surface = NativeSurface(surface=self.__font.render(self.__text, self.__color), identifier=str(self))
        else:
            child_surfaces = []
            child_positions = []
            current_y: float = 0
            max_width: float = 0
            for line in lines:
                surface = self.__font.render(line, self.__color)
                child_surfaces.append(NativeSurface(surface=surface, identifier=self.__identifier(text=line)))
                child_positions.append((0, current_y))
                current_y += surface.get_height()
                max_width = max(max_width, surface.get_width())
            surface = ContainerSurface(
                child_surfaces=child_surfaces,
                child_positions=child_positions,
                size=(max_width, current_y)
            )
        Text.__text_cache[key] = surface
        return surface

    def __hash__(self):
        return hash((self.__text, self.__font, self.__color))

    def __repr__(self):
        return self.__identifier(text=self.__text)

    def __identifier(self, text: str) -> str:
        return self.__class__.__name__ + "(text=" + str(text) + ", font=" + str(self.__font) + ", color=" + str(self.__color) + ")"
