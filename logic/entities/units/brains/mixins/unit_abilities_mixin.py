from typing import Type, TypeVar, Optional, MutableSequence

from logic.entities.abilities.ability import Ability
from logic.core.draw_queue import DrawQueue

T = TypeVar('T')


class UnitAbilitiesMixin:
    def __init__(self, abilities: list[Ability]):
        self.__abilities = abilities

    def ability(self, ability_type: Type[T]) -> Optional[T]:
        for element in self.__abilities:
            if isinstance(element, ability_type):
                return element
        return None

    def process_input(self, events: MutableSequence):
        for ability in self.__abilities:
            ability.process_input(owner=self, events=events)

    def pre_update(self):
        for ability in self.__abilities:
            ability.pre_update(owner=self)

    def update(self):
        for ability in self.__abilities:
            ability.update(owner=self)

    def post_update(self):
        for ability in self.__abilities:
            ability.post_update(owner=self)

    def render(self, queue: DrawQueue):
        for ability in self.__abilities:
            ability.render(owner=self, queue=queue)
