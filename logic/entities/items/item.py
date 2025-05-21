from enum import Enum
from typing import MutableSequence

from logic.core.animated_object import AnimatedObject


class ItemType(Enum):
    store = 'store'
    inventory = 'inventory'
    gui = 'gui'

class Item:
    def __init__(self, price: int, description: str, is_active: bool):
        self.price = price
        self.description = description
        self.animated_object_cache: dict = {}
        self.is_active = is_active

    def process_input(self, owner: object, events: MutableSequence, slot: int | None):
        pass

    def update(self, owner: object):
        pass

    def post_update(self, owner: object):
        pass

    def get_animated_object(self, item_type: ItemType) -> AnimatedObject:
        if item_type in self.animated_object_cache:
            return self.animated_object_cache[item_type]
        self.animated_object_cache[item_type] = AnimatedObject(
            animations=self.get_animations(),
            scale=self.__get_scale(item_type=item_type),
            offset=(0, 0))
        return self.animated_object_cache[item_type]

    def get_animations(self) -> dict:
        return {}

    def can_activate(self, owner: object) -> bool:
        return True

    def cooldown(self) -> float | None:
        return None

    @staticmethod
    def __get_scale(item_type: ItemType) -> float:
        sprite_scale: float = 0
        match item_type:
            case ItemType.store:
                sprite_scale = 3
            case ItemType.gui:
                sprite_scale = 1
            case ItemType.inventory:
                sprite_scale = 1
        return sprite_scale
