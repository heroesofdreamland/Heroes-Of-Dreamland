from enum import IntEnum

from logic.core.render.component import Component
from logic.core.render.surface import Surface, ContainerSurface


class VStackAlignment(IntEnum):
    START = 0
    CENTER = 1
    END = 2


class VStack(Component):
    def __init__(self, children: list[Component], spacing: float = 0, alignment: VStackAlignment = VStackAlignment.CENTER):
        self.__children = children
        self.__spacing = spacing
        self.__alignment = alignment
        super().__init__()

    def surface(self) -> Surface:
        total_height: float = 0
        max_width: float = 0

        child_surfaces = []
        for child in self.__children:
            child_surfaces.append(child.surface())

        for child_surface in child_surfaces:
            size = child_surface.get_size()
            max_width = max(max_width, size[0])
            total_height += size[1] + self.__spacing
        if total_height > 0:
            total_height -= self.__spacing

        current_y: float = 0
        child_positions = []
        for child_surface in child_surfaces:
            size = child_surface.get_size()
            current_x: float = 0
            match self.__alignment:
                case VStackAlignment.START:
                    current_x = 0
                case VStackAlignment.CENTER:
                    current_x = (max_width - size[0]) / 2
                case VStackAlignment.END:
                    current_x = max_width - size[0]
            child_positions.append((current_x, current_y))
            current_y += size[1] + self.__spacing
        return ContainerSurface(child_surfaces=child_surfaces, child_positions=child_positions, size=(max_width, total_height))
