from enum import IntEnum

from logic.core.render.component import Component
from logic.core.render.surface import ContainerSurface, Surface


class ZStackAlignment(IntEnum):
    TOP_LEFT = 0
    CENTER_LEFT = 1
    BOTTOM_LEFT = 2
    TOP_CENTER = 3
    CENTER = 4
    BOTTOM_CENTER = 5
    TOP_RIGHT = 6
    CENTER_RIGHT = 7
    BOTTOM_RIGHT = 8


class ZStack(Component):
    def __init__(self, children: list[Component], alignment: ZStackAlignment = ZStackAlignment.CENTER):
        self.__children = children
        self.__alignment = alignment
        super().__init__()

    def surface(self) -> Surface:
        max_width: float = 0
        max_height: float = 0
        child_surfaces = []
        for child in self.__children:
            child_surfaces.append(child.surface())

        for child_surface in child_surfaces:
            size = child_surface.get_size()
            max_width = max(max_width, size[0])
            max_height = max(max_height, size[1])

        child_positions = []
        for child_surface in child_surfaces:
            size = child_surface.get_size()
            current_x: float = 0
            current_y: float = 0
            match self.__alignment:
                case ZStackAlignment.TOP_LEFT:
                    current_x = 0
                    current_y = 0
                case ZStackAlignment.TOP_CENTER:
                    current_x = (max_width - size[0]) / 2
                    current_y = 0
                case ZStackAlignment.TOP_RIGHT:
                    current_x = max_width - size[0]
                    current_y = 0
                case ZStackAlignment.CENTER_LEFT:
                    current_x = 0
                    current_y = (max_height - size[1]) / 2
                case ZStackAlignment.CENTER:
                    current_x = (max_width - size[0]) / 2
                    current_y = (max_height - size[1]) / 2
                case ZStackAlignment.CENTER_RIGHT:
                    current_x = max_width - size[0]
                    current_y = (max_height - size[1]) / 2
                case ZStackAlignment.BOTTOM_LEFT:
                    current_x = 0
                    current_y = max_height - size[1]
                case ZStackAlignment.BOTTOM_CENTER:
                    current_x = (max_width - size[0]) / 2
                    current_y = max_height - size[1]
                case ZStackAlignment.BOTTOM_RIGHT:
                    current_x = max_width - size[0]
                    current_y = max_height - size[1]

            child_positions.append((current_x, current_y))

        return ContainerSurface(child_surfaces=child_surfaces, child_positions=child_positions, size=(max_width, max_height))
