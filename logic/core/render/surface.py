import pygame

from logic.core.draw_queue import DrawQueue, DrawAnchor, modify_top_left_coordinate
from logic.core.opengl import SurfaceIdentifier
from logic.core.render.types import Position, Size


class SurfaceModifier:
    def apply(self, surface: pygame.Surface) -> pygame.Surface | None:
        pass


class Surface:
    def get_size(self) -> Size:
        pass

    def render(self, position: Position, queue: DrawQueue, anchor: int = DrawAnchor.CENTER, game_space: bool = False, priority: int = 0):
        pass

    def add_modifier(self, modifier: SurfaceModifier):
        pass


class EmptySurface(Surface):
    def get_size(self) -> Size:
        return 0, 0


class NativeSurface(Surface):
    def __init__(self, surface: pygame.Surface, identifier: str):
        self.__surface = surface
        self.__identifier = identifier

    def get_size(self) -> Size:
        return self.__surface.get_size()

    def render(self, position: Position, queue: DrawQueue, anchor: int = DrawAnchor.CENTER, game_space: bool = False, priority: int = 0):
        queue.draw_surface(surface=self.__surface,
                           identifier=SurfaceIdentifier(identifier=self.__identifier),
                           position=position,
                           anchor=anchor,
                           game_space=game_space,
                           priority=priority)

    def add_modifier(self, modifier: SurfaceModifier):
        surface = modifier.apply(surface=self.__surface)
        if surface:
            self.__surface = surface
            self.__identifier += ", " + str(modifier)


class ContainerSurface(Surface):
    def __init__(self, child_surfaces: list[Surface], child_positions: list[Position], size: Size):
        self.__child_surfaces = child_surfaces
        self.__child_positions = child_positions
        self.__size = size

    def get_size(self) -> Size:
        return self.__size

    def render(self, position: Position, queue: DrawQueue, anchor: int = DrawAnchor.CENTER, game_space: bool = False, priority: int = 0):
        x, y = modify_top_left_coordinate(anchor=anchor, position=position, size=self.__size)
        for child_surface, child_position in zip(self.__child_surfaces, self.__child_positions):
            s_x, s_y = child_position
            child_surface.render(position=(s_x + x, s_y + y), queue=queue, anchor=DrawAnchor.TOP_LEFT, game_space=game_space, priority=priority)

    def add_modifier(self, modifier: SurfaceModifier):
        for child_surface in self.__child_surfaces:
            child_surface.add_modifier(modifier=modifier)
