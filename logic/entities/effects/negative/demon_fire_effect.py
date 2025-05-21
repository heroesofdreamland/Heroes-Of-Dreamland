from __future__ import annotations

import random
from logic.core.render.component import Component
from logic.core.render.components.rect import Rect
from logic.core.render.components.text import Text
from logic.core.render.components.zstack import ZStack
from logic.core.render.types import Size
from logic.entities.effects.effect import Effect
from logic.environment.environment import Environment
from logic.ui.colors import Colors
from logic.ui.fonts import Fonts


class DemonFireEffect(Effect):
    max_amount = 7

    def __repr__(self):
        return "DemonFireEffect(amount=" + str(self.amount) + ", duration=" + str(self.duration) + ")"

    def __add__(self, other) -> Effect:
        if self.is_stackable(other=other):
            return DemonFireEffect(duration=max(self.remaining_duration(), other.remaining_duration()),
                                   amount=round(self.amount + other.amount, 1))
        else:
            return self

    def is_stackable(self, other: Effect) -> bool:
        return isinstance(other, DemonFireEffect)

    def resolve(self, unit: object):
        amount = min(self.amount, DemonFireEffect.max_amount)
        if amount >= DemonFireEffect.max_amount:
            if len(Environment.player.items) > 0:
                random_item = random.choice(Environment.player.items)
                Environment.player.remove_item(random_item)
            self._is_ended = True

    def status_bar_component(self, size: Size) -> Component | None:
        return ZStack(
            children=[
                Rect(
                    size=size,
                    border=(2, Colors.YELLOW)
                ),
                Text(
                    text=str(self.amount),
                    font=Fonts.blackcraft(size=14),
                    color=Colors.WHITE
                )
            ]
        )
