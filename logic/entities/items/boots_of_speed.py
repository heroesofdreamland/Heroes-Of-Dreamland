from typing import cast

from logic.core.animation import Animation
from logic.entities.items.item import Item
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.models.animation_type import AnimationType


class BootsOfSpeed(Item):
    def __init__(self):
        self.path = 'resources/used_resources/items/chaos_incarnatech_loot/eggsoul/'
        self.__increase_speed = 0.1
        super().__init__(price=100,
                         description='+0.1 speed',
                         is_active=False)

    def update(self, owner: object):
        unit = cast(Unit, owner)
        unit.speed_modify(diff=self.__increase_speed, permanent=False)

    def get_animations(self) -> dict:
        return {
            AnimationType.USED: Animation(path=self.path + AnimationType.USED.value,
                                          count=18,
                                          duration=0.5,
                                          repeat=True),
            AnimationType.PREVIEW: Animation(path=self.path + AnimationType.PREVIEW.value,
                                             count=12,
                                             duration=0.5,
                                             repeat=True)
        }
