import pygame

from logic.core.render.component import Component
from logic.core.render.surface import SurfaceModifier, Surface


class OpacityModifier(SurfaceModifier):
    def __init__(self, opacity: float):
        self.__opacity = opacity

    def apply(self, surface: pygame.Surface) -> pygame.Surface | None:
        if self.__opacity != 1:
            new_surface = pygame.Surface(size=surface.get_size(), flags=pygame.SRCALPHA)
            surface.set_alpha(int(self.__opacity * 255))
            new_surface.blit(surface, (0, 0))
            return new_surface
        return None

    def __hash__(self):
        return hash(self.__opacity)

    def __repr__(self):
        return self.__class__.__name__ + "(opacity=" + str(self.__opacity) + ")"


class Opacity(Component):
    def __init__(self, child: Component, opacity: float):
        self.__child = child
        self.__opacity = opacity
        super().__init__()

    def surface(self) -> Surface:
        child_surface = self.__child.surface()
        child_surface.add_modifier(OpacityModifier(opacity=self.__opacity))
        return child_surface

    def __hash__(self):
        return hash(self.__opacity)

    def __repr__(self):
        return self.__class__.__name__ + "(opacity=" + str(self.__opacity) + ")"