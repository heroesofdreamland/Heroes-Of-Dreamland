from copy import deepcopy
from typing import MutableSequence

from logic.core.draw_queue import DrawQueue
from logic.entities.items.item import Item


class UnitItemsMixin:
    def __init__(self):
        self.__passive_items = []
        self.__active_items = []

    @property
    def active_items(self) -> list[Item]:
        return self.__active_items

    @property
    def passive_items(self) -> list[Item]:
        return self.__passive_items

    @property
    def all_items(self) -> list[Item]:
        return self.__active_items + self.__passive_items

    def add_item(self, item: Item):
        if item.is_active:
            self.__active_items.append(deepcopy(item))
        else:
            self.__passive_items.append(deepcopy(item))

    def remove_item(self, item: Item):
        if item.is_active:
            self.__active_items.remove(item)
        else:
            self.__passive_items.remove(item)

    def process_input(self, events: MutableSequence):
        for index, item in enumerate(self.__active_items):
            item.process_input(owner=self, events=events, slot=index)

    def pre_update(self):
        pass

    def update(self):
        for item in self.__passive_items:
            item.update(owner=self)
        for item in self.__active_items:
            item.update(owner=self)

    def post_update(self):
        for item in self.__passive_items:
            item.post_update(owner=self)
        for item in self.__active_items:
            item.post_update(owner=self)

    def render(self, queue: DrawQueue):
        pass