from __future__ import annotations

from typing import cast
from logic.core.render.component import Component
from logic.core.render.components.rect import Rect
from logic.core.render.components.text import Text
from logic.core.render.components.zstack import ZStack
from logic.core.render.types import Size
from logic.entities.effects.effect import Effect
from logic.ui.colors import Colors
from logic.ui.fonts import Fonts
from logic.entities.units.brains.unit_brain import Unit


class PoisonEffect(Effect):
    max_amount = 3

    def __repr__(self):
        return "PoisonEffect(amount=" + str(self.amount) + ", duration=" + str(self.duration) + ")"

    def __add__(self, other) -> Effect:
        if self.is_stackable(other=other):
            return PoisonEffect(duration=max(self.remaining_duration(), other.remaining_duration()), amount=round(self.amount + other.amount, 1))
        else:
            return self

    def is_stackable(self, other: Effect) -> bool:
        return isinstance(other, PoisonEffect)

    def resolve(self, unit: object):
        unit = cast(Unit, unit)
        amount = min(self.amount, PoisonEffect.max_amount)
        if amount >= PoisonEffect.max_amount:
            unit.kill()
            self._is_ended = True

    def status_bar_component(self, size: Size) -> Component | None:
        return ZStack(
            children=[
                Rect(
                    size=size,
                    border=(2, Colors.GREEN)
                ),
                Text(
                    text=str(self.amount),
                    font=Fonts.blackcraft(size=14),
                    color=Colors.WHITE
                )
            ]
        )
