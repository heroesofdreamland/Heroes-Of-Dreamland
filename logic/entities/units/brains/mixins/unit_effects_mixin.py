from typing import MutableSequence

from logic.core.draw_queue import DrawQueue
from logic.entities.effects.effect import Effect
from logic.environment.environment import Groups


class UnitEffectsMixin:
    def __init__(self):
        self.__effects = []

    @property
    def effects(self) -> list[Effect]:
        return self.__effects

    def effects_clean(self):
        self.__effects = []

    def effect_apply(self, effect: Effect):
        new_effects = []
        effect_added = False
        for ef in self.effects:
            if ef.is_stackable(other=effect) and not effect_added:
                new_effects.append(ef + effect)
                effect_added = True
            else:
                new_effects.append(ef)
        if not effect_added:
            new_effects.append(effect)
        self.__effects = new_effects

    def process_input(self, events: MutableSequence):
        pass

    def pre_update(self):
        pass

    def update(self):
        for ef in self.__effects:
            if not ef.is_started():
                ef.start(group=Groups.objects)
        for ef in reversed(self.__effects):
            if ef.is_ended():
                ef.stop(group=Groups.objects)
                self.__effects.remove(ef)
        for ef in self.__effects:
            ef.resolve(unit=self)
        for ef in reversed(self.__effects):
            if ef.is_ended():
                ef.stop(group=Groups.objects)
                self.__effects.remove(ef)

    def post_update(self):
        pass

    def render(self, queue: DrawQueue):
        pass