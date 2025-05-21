from typing import MutableSequence

import pymunk
from pymunk import Vec2d

from logic.core.draw_queue import DrawQueue
from logic.environment.environment import Spaces
from logic.ui.colors import Colors
from logic.settings.debug_settings import DebugSettings


class UnitPhysicsMixin:
    def __init__(self, shape: pymunk.Shape, position: Vec2d):
        self.__shape = shape
        self.__is_in_space = False
        self.__cached_shape_radius: float | None = None
        self.__cached_body_position = position
        shape.body.position = position

    @property
    def shape_radius(self) -> float:
        if self.__cached_shape_radius is not None:
            return self.__cached_shape_radius
        else:
            radius = self.__shape.radius
            self.__cached_shape_radius = radius
            return radius

    @property
    def position(self) -> Vec2d:
        return self.__cached_body_position

    def set_position(self, position: Vec2d):
        self.__shape.body.position = position
        self.__cached_body_position = position

    @property
    def shape(self) -> pymunk.Shape:
        return self.__shape

    def enable_physics(self, enable: bool):
        if enable and not self.__is_in_space:
            Spaces.SHARED.add(self.__shape.body, self.__shape)
            self.__is_in_space = True
        elif not enable and self.__is_in_space:
            Spaces.SHARED.remove(self.__shape.body, self.__shape)
            self.__is_in_space = False

    def process_input(self, events: MutableSequence):
        pass

    def pre_update(self):
        pass

    def update(self):
        pass

    def post_update(self):
        self.__cached_body_position = self.__shape.body.position
        if not self.is_alive:  # Lifecycle.is_alive (cast removed for performance)
            self.enable_physics(False)

    def render(self, queue: DrawQueue):
        if DebugSettings.debug_settings['show_unit_shapes']:
            position = self.position
            queue.debug_draw_circle(color=Colors.GREEN, radius=self.__shape.radius, position=(position.x, position.y), game_space=True)
