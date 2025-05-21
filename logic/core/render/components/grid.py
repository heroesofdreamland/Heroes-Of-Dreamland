import pygame

from logic.core.render.color import Color
from logic.core.render.component import Component
from logic.core.render.surface import Surface, ContainerSurface, NativeSurface
from logic.core.render.types import Position, Size
from logic.core.screen import Screen


class Grid(Component):
    __grid_cache: dict[tuple[float, int, int, str], pygame.Surface] = {}

    def __init__(self, children: list[Component], cell_size: float, width: int, height: int, border_color: Color, selected_cell: tuple[int, int] | None = None):
        self.__children = children
        self.__cell_size = cell_size
        self.__width = width
        self.__height = height
        self.__border_color = border_color
        self.__selected_cell = selected_cell
        self.__border_width = 2
        self.__selected_border_width = 5
        super().__init__()

    def update(self, children: list[Component] | None = None):
        if children is not None:
            self.__children = children

    def surface(self) -> Surface:
        child_surfaces: list[Surface] = []
        child_positions: list[Position] = []
        if not self.__border_color.is_clear():
            base_grid = self.__prepare_grid()
            child_surfaces.append(NativeSurface(surface=base_grid, identifier=self.__class__.__name__ + "/Base(" + str(hash((self.__cell_size, self.__width, self.__height, str(self.__border_color)))) + ")"))
            child_positions.append((0, 0))
        screen_scale = Screen.get_screen_scale()
        scaled_cell_size = self.__cell_size * screen_scale
        children_length = len(self.__children)
        for i in range(0, self.__width):
            for j in range(0, self.__height):
                child_index = j * self.__width + i
                if child_index < children_length:
                    child_surface = self.__children[child_index].surface()
                    child_surfaces.append(child_surface)
                    child_size = child_surface.get_size()
                    x_offset = (scaled_cell_size - child_size[0]) / 2
                    y_offset = (scaled_cell_size - child_size[1]) / 2
                    child_positions.append((i * scaled_cell_size + x_offset, j * scaled_cell_size + y_offset))
        if self.__selected_cell is not None and not self.__border_color.is_clear():
            i, j = self.__selected_cell
            selected_rect_surface = pygame.Surface((scaled_cell_size, scaled_cell_size), pygame.SRCALPHA)
            pygame.draw.rect(selected_rect_surface,
                             self.__border_color.color(),
                             (0, 0, scaled_cell_size, scaled_cell_size),
                             self.__selected_border_width)
            child_surfaces.append(NativeSurface(surface=selected_rect_surface, identifier=self.__class__.__name__ + "/SelectedCell(" + str(hash((self.__cell_size, self.__width, self.__height, str(self.__border_color), self.__selected_cell))) + ")"))
            child_positions.append((i * scaled_cell_size, j * scaled_cell_size))
        return ContainerSurface(child_surfaces=child_surfaces, child_positions=child_positions, size=self.__grid_size())

    def __hash__(self):
        return hash((
            tuple(self.__children),
            self.__cell_size,
            self.__width,
            self.__height,
            self.__border_color.__hash__
        ))

    def __grid_size(self) -> Size:
        scaled_cell_size = self.__cell_size * Screen.get_screen_scale()
        surface_width = scaled_cell_size * self.__width
        surface_height = scaled_cell_size * self.__height
        return surface_width, surface_height

    def __prepare_grid(self) -> pygame.Surface:
        scaled_cell_size = self.__cell_size * Screen.get_screen_scale()
        key = scaled_cell_size, self.__width, self.__height, str(self.__border_color)
        if key in Grid.__grid_cache:
            return Grid.__grid_cache[key]
        grid_size = self.__grid_size()
        surface = pygame.Surface(grid_size, pygame.SRCALPHA)
        rect_surface = pygame.Surface((scaled_cell_size, scaled_cell_size), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface,
                         self.__border_color.color(),
                         (0, 0, scaled_cell_size, scaled_cell_size),
                         self.__border_width)
        for i in range(0, self.__width):
            for j in range(0, self.__height):
                surface.blit(source=rect_surface, dest=(i * scaled_cell_size, j * scaled_cell_size))
        Grid.__grid_cache[key] = surface
        return surface
