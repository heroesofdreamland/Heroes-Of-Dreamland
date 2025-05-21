from enum import IntEnum

from logic.core.render.component import Component
from logic.core.render.surface import Surface, ContainerSurface


class HStackAlignment(IntEnum):
    TOP = 0
    CENTER = 1
    BOTTOM = 2


class HStack(Component):
    def __init__(self, children: list[Component], spacing: float = 0, alignment: HStackAlignment = HStackAlignment.CENTER):
        self.__children = children
        self.__spacing = spacing
        self.__alignment = alignment
        super().__init__()

    def update(self, children: list[Component] | None = None):
        if children is not None:
            self.__children = children

    def surface(self) -> Surface:
        total_width: float = 0
        max_height: float = 0

        child_surfaces = []
        for child in self.__children:
            child_surfaces.append(child.surface())

        for child_surface in child_surfaces:
            size = child_surface.get_size()
            max_height = max(max_height, size[1])
            total_width += size[0] + self.__spacing
        if total_width > 0:
            total_width -= self.__spacing

        current_x: float = 0
        child_positions = []
        for child_surface in child_surfaces:
            size = child_surface.get_size()
            current_y: float = 0
            match self.__alignment:
                case HStackAlignment.TOP:
                    current_y = 0
                case HStackAlignment.CENTER:
                    current_y = (max_height - size[1]) / 2
                case HStackAlignment.BOTTOM:
                    current_y = max_height - size[1]
            child_positions.append((current_x, current_y))
            current_x += size[0] + self.__spacing

        return ContainerSurface(child_surfaces=child_surfaces, child_positions=child_positions, size=(total_width, max_height))
