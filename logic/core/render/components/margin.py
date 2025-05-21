from logic.core.render.component import Component
from logic.core.render.surface import Surface, ContainerSurface


class Margin(Component):
    def __init__(self, child: Component, left: float = 0, right: float = 0, top: float = 0, bottom: float = 0):
        self.__child = child
        self.__left = left
        self.__right = right
        self.__top = top
        self.__bottom = bottom
        super().__init__()

    def surface(self) -> Surface:
        child_surface = self.__child.surface()
        child_width, child_height = child_surface.get_size()
        size = (child_width + self.__left + self.__right, child_height + self.__top + self.__bottom)
        return ContainerSurface(child_surfaces=[child_surface], child_positions=[(self.__left, self.__top)], size=size)