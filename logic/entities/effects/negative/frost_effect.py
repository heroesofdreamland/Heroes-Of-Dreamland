from __future__ import annotations

from typing import cast
from logic.core.render.component import Component
from logic.core.render.components.rect import Rect
from logic.core.render.components.text import Text
from logic.core.render.components.zstack import ZStack
from logic.core.render.types import Size
from logic.entities.effects.effect import Effect
from logic.entities.effects.positive.resistance_effect import ResistanceEffect
from logic.entities.effects.negative.stun_effect import StunEffect
from logic.ui.colors import Colors
from logic.ui.fonts import Fonts
from logic.entities.units.brains.unit_brain import Unit


class FrostEffect(Effect):
    max_amount = 6
    speed_diff = -5

    def __repr__(self):
        return "FrostEffect(amount=" + str(self.amount) + ", duration=" + str(self.duration) + ")"

    def __add__(self, other) -> Effect:
        if self.is_stackable(other=other):
            return FrostEffect(duration=max(self.remaining_duration(), other.remaining_duration()), amount=round(self.amount + other.amount, 1))
        else:
            return self

    def is_stackable(self, other: Effect) -> bool:
        return isinstance(other, FrostEffect)

    def resolve(self, unit: object):
        unit = cast(Unit, unit)
        amount = min(self.amount, FrostEffect.max_amount)
        if amount >= FrostEffect.max_amount:
            self._is_ended = True
            unit.effect_apply(effect=StunEffect(duration=self.duration))
            unit.effect_apply(effect=ResistanceEffect(resistance_from=FrostEffect, duration=self.duration + 2)) # TODO: - Мб вынести в переменную
        elif amount > 0:
            unit.speed_modify(diff=amount * FrostEffect.speed_diff, permanent=False)

    def status_bar_component(self, size: Size) -> Component | None:
        return ZStack(
            children=[
                Rect(
                    size=size,
                    border=(2, Colors.BLACK)
                ),
                Text(
                    text=str(self.amount),
                    font=Fonts.blackcraft(size=14),
                    color=Colors.WHITE
                )
            ]
        )
