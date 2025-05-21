import time
from enum import Enum
from typing import Optional

import pygame

from logic.core.animation import Animation
from logic.core.opengl import Texture


class AnimatedObject:
    def __init__(self,
                 animations: dict[Enum, Animation],
                 scale: float,
                 offset: tuple[float, float]):
        self.mirrored = False
        self.angle: float = 0
        self.scale = scale
        self.__animation_start_time: float | None = None
        self.__animation_pause_time: float | None = None
        self.position = None
        self.offset = offset
        self.animations = animations
        self.__current_animation_type: Enum | None = None
        self.__current_animation_duration = None
        self.__current_animation_percent = None

    def is_animation_configured(self):
        return self.__current_animation_type is not None and self.__animation_start_time != 0

    def configure_animation(self, animation_type: Enum):
        if animation_type != self.__current_animation_type:
            self.__animation_start_time = time.time()
            self.__current_animation_type = animation_type
            self.__current_animation_duration = self.animations[self.__current_animation_type].get_duration()
            self.__current_animation_percent = self.__completion_percent()

    def destroy_animation(self):
        self.__animation_start_time = None
        self.__current_animation_type = None
        self.__current_animation_duration = None
        self.__current_animation_percent = None

    def get_current_animation_type(self):
        return self.__current_animation_type

    def is_animation_completed(self):
        return self.__completion_percent() == 1

    def get_texture(self) -> Texture | None:
        if not self.is_animation_configured():
            return None
        current_animation = self.animations[self.__current_animation_type]
        return current_animation.get_texture(index=self.__current_animation_index(), scale=self.scale, mirrored=self.mirrored)

    def get_image(self) -> Optional[tuple[pygame.Surface, str, int]]:
        if not self.is_animation_configured():
            return None
        current_animation = self.animations[self.__current_animation_type]
        index = self.__current_animation_index()
        return current_animation.get_image(index=index, scale=self.scale, mirrored=self.mirrored), current_animation.get_base_path(), index

    def pause_animation(self, is_paused: bool):
        if is_paused and self.__animation_pause_time is None:
            self.__animation_pause_time = time.time()
        if not is_paused and self.__animation_pause_time is not None:
            pause_diff = time.time() - self.__animation_pause_time
            self.__animation_pause_time = None
            self.__animation_start_time += pause_diff

    def __current_animation_index(self) -> int:
        current_animation = self.animations[self.__current_animation_type]
        current_animation_frames_count = current_animation.get_frames_count()
        current_animation_index = current_animation_frames_count - 1
        completion_percent = self.__completion_percent()
        if completion_percent < 1:
            current_animation_index = int(completion_percent * current_animation_frames_count)
        return current_animation_index

    def __completion_percent(self):
        if not self.is_animation_configured():
            return 0
        if self.__current_animation_duration <= 0:
            return self.__current_animation_percent
        current_time = time.time()
        if self.__animation_pause_time is not None:
            current_time = self.__animation_pause_time
        time_diff = current_time - self.__animation_start_time
        current_animation = self.animations[self.__current_animation_type]

        completion_percent = time_diff / self.__current_animation_duration
        self.__update_start_time_if_animation_speed_changed(completion_percent,
                                                            current_time,
                                                            current_animation)

        if completion_percent > 1:
            if current_animation.repeat:
                completion_percent = completion_percent % 1
            else:
                completion_percent = 1
        if completion_percent < 0:
            completion_percent = 0
        self.__current_animation_percent = completion_percent
        return completion_percent

    def __update_start_time_if_animation_speed_changed(self,
                                                       completion_percent: float,
                                                       current_time: float,
                                                       current_animation: Animation):
        if self.__current_animation_duration != current_animation.get_duration():
            new_time_diff = completion_percent * current_animation.get_duration()
            self.__current_animation_duration = current_animation.get_duration()
            self.__animation_start_time = current_time - new_time_diff