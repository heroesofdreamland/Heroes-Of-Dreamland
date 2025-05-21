from typing import cast, MutableSequence

from logic.core.draw_queue import DrawQueue
from logic.environment.environment import Environment, Groups
from logic.entities.units.models.animated_objects.general.armor.field_object import FieldObject


class UnitArmorMixin:
    def __init__(self, armor: float):
        self.__armor = armor
        self.__armor_object: FieldObject | None = None

    @property
    def armor(self) -> float:
        return self.__armor

    def process_input(self, events: MutableSequence):
        pass

    def pre_update(self):
        pass

    def update(self):
        from logic.entities.units.brains.unit_brain import Unit
        unit = cast(Unit, self)
        if self.__armor_object is not None:
            if self.__armor_is_active:
                self.__armor_object.position = unit.position
            else:
                self.__armor_object.is_alive = False
                self.__armor_object = None
        elif self.__armor_is_active:
            x_offset, y_offset = unit.animated_object.offset
            new_armor_object = FieldObject(position=unit.position,
                                           offset=(x_offset + 10, y_offset + 10),
                                           group=Groups.objects)
            Environment.map.objects.append(new_armor_object)
            self.__armor_object = new_armor_object

    def post_update(self):
        pass

    def render(self, queue: DrawQueue):
        pass

    def armor_consume_damage(self, damage: float) -> float:
        remaining_damage = damage
        if self.__armor_is_active:
            if remaining_damage >= self.__armor:
                remaining_damage -= self.__armor
                self.__armor = 0
            else:
                self.__armor -= remaining_damage
                remaining_damage = 0
        return remaining_damage

    @property
    def __armor_is_active(self) -> bool:
        return self.__armor > 0