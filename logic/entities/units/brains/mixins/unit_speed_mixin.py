import math
from typing import MutableSequence

import pymunk

from logic.core.animated_object import AnimatedObject
from logic.core.draw_queue import DrawQueue
from logic.core.isometry import cartesian_to_isometric
from logic.entities.units.data.unit_life_state import UnitLifeState
from logic.entities.units.data.unit_side import UnitSide
from logic.entities.units.models.animation_type import AnimationType


class UnitSpeedMixin:
    def __init__(self, speed: float, animated_object: AnimatedObject, body: pymunk.Body):
        self.__base_speed = speed
        self.__current_speed = speed
        self.__current_animation_scale = 1
        self.__animated_object = animated_object
        self.__body = body
        self.__permanent_diff: float = 0
        self.__temporary_diff: float = 0
        self.__permanent_stun = False
        self.__temporary_stun = False
        self.__x_direction: float = 0
        self.__y_direction: float = 0
        self.__side = UnitSide.LEFT
        self.__recalculate_speed()

    @property
    def side(self) -> UnitSide:
        return self.__side

    @property
    def speed(self) -> float:
        return self.__current_speed

    @property
    def is_moving(self) -> bool:
        return self.__current_speed > 0 and (self.__x_direction != 0 or self.__y_direction != 0)

    @property
    def is_stunned(self) -> bool:
        return self.__permanent_stun or self.__temporary_stun

    def set_side(self, side: UnitSide):
        match side:
            case UnitSide.RIGHT:
                self.__side = UnitSide.RIGHT
                self.__animated_object.mirrored = False
            case UnitSide.LEFT:
                self.__side = UnitSide.LEFT
                self.__animated_object.mirrored = True

    def speed_modify(self, diff: float, permanent: bool):
        if permanent:
            # This change will be applied forever
            self.__permanent_diff += diff
        else:
            # This change will be cleaned up on the next update
            self.__temporary_diff += diff
        self.__recalculate_speed()

    def speed_set_stun(self, is_stunned: bool, permanent: bool):
        if permanent:
            # This change will be applied forever
            self.__permanent_stun = is_stunned
        else:
            # This change will be cleaned up on the next update
            self.__temporary_stun = is_stunned
        self.__recalculate_speed()

    def set_direction(self, x: float, y: float):
        length = math.hypot(x, y)
        if length > 0:
            self.__x_direction = x / length
            self.__y_direction = y / length
        else:
            self.__x_direction = 0
            self.__y_direction = 0

    def process_input(self, events: MutableSequence):
        pass

    def pre_update(self):
        self.__temporary_diff = 0
        self.__temporary_stun = False
        if AnimationType.RUN in self.__animated_object.animations:
            self.__animated_object.animations[AnimationType.RUN].speed = self.__current_animation_scale
        self.__body.velocity = [0, 0]

    def update(self):
        if self.life_state == UnitLifeState.DEATH:  # UnitLifeMixin.life_state (cast removed for performance)
            return
        if self.is_stunned:
            self.__body.velocity = [0, 0]
        else:
            speed = self.__current_speed
            self.__body.velocity = [speed * self.__x_direction, speed * self.__y_direction]
            iso_x_direction = cartesian_to_isometric(coordinate=(self.__x_direction, self.__y_direction))[0]
            if iso_x_direction > 0.1:
                self.set_side(UnitSide.RIGHT)
            elif iso_x_direction < -0.1:
                self.set_side(UnitSide.LEFT)

    def post_update(self):
        pass

    def render(self, queue: DrawQueue):
        pass

    def __recalculate_speed(self):
        if self.__permanent_stun or self.__temporary_stun:
            self.__current_speed = 0
        else:
            self.__current_speed = max(round(self.__base_speed + self.__permanent_diff + self.__temporary_diff, 2), 0)

        if self.__current_speed == 0:
            self.__current_animation_scale = 1
        else:
            self.__current_animation_scale = round(self.__current_speed / self.__base_speed, 1)

        if AnimationType.RUN in self.__animated_object.animations:
            self.__animated_object.animations[AnimationType.RUN].speed = self.__current_animation_scale
