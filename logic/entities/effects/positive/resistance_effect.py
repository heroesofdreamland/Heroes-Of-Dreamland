from __future__ import annotations

from typing import cast, Type

from logic.core.render.component import Component
from logic.core.render.types import Size
from logic.entities.effects.effect import Effect
from logic.entities.units.brains.unit_brain import Unit


class ResistanceEffect(Effect):
    def __init__(self,
                 resistance_from: Type,
                 duration: float):
        super().__init__(duration=duration, amount=1)
        self.__resistance_from = resistance_from

    def __repr__(self):
        return "ResistanceEffect(resistance_from=" + self.__resistance_from.__name__ + ", duration=" + str(self.duration) + ")"

    def __add__(self, other) -> Effect:
        if self.is_stackable(other=other):
            return ResistanceEffect(resistance_from=self.__resistance_from, duration=max(self.remaining_duration(), other.remaining_duration()))
        else:
            return self

    def is_stackable(self, other: Effect) -> bool:
        if isinstance(other, ResistanceEffect):
            return self.__resistance_from == other.__resistance_from
        else:
            return False

    def resolve(self, unit: object):
        unit = cast(Unit, unit)
        for effect in unit.effects:
            if isinstance(effect, self.__resistance_from):
                effect._is_ended = True

    def status_bar_component(self, size: Size) -> Component | None:
        return None