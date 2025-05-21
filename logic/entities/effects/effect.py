from __future__ import annotations

from logic.core.lifecycle_group import LifecycleGroup
from logic.core.render.component import Component
from logic.core.render.types import Size
from logic.core.timer import Timer

class Effect:
    def __init__(self,
                 duration: float,
                 amount: float = 1):
        self.amount = amount
        self.duration = duration
        self._is_ended = False
        self.__timer: Timer|None = None

    def __add__(self, other) -> Effect:
        # To be implemented in subclasses.
        pass

    def start(self, group: LifecycleGroup):
        self.__timer = Timer(duration=self.duration)
        self.__timer.start(group=group)

    def stop(self, group: LifecycleGroup):
        if self.__timer is not None:
            self.__timer.stop(group=group)
            self.__timer = None

    def is_started(self):
        return self.__timer is not None

    def is_ended(self):
        if self._is_ended:
            return True
        if self.__timer is None:
            return False
        return self.__timer.is_completed()

    def remaining_duration(self):
        if self.__timer is not None:
            return max(self.duration - self.__timer.get_time(), 0)
        else:
            return self.duration

    def is_stackable(self, other: Effect) -> bool:
        return False

    def resolve(self, unit: object):
        # To be implemented in subclasses.
        pass

    def status_bar_component(self, size: Size) -> Component | None:
        # To be implemented in subclasses.
        pass
