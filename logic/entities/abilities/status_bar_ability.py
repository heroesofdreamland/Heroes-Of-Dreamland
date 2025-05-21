from typing import cast

from logic.entities.abilities.ability import Ability
from logic.core.draw_queue import DrawQueue
from logic.environment.environment import Groups
from logic.ui.unit_status_bar import UnitStatusBar
from logic.entities.units.brains.unit_brain import Unit


class StatusBarAbility(Ability):
    def __init__(self, offset: tuple[float, float]):
        self.__status_bar: UnitStatusBar | None = None
        self.__offset = offset

    def update(self, owner: object):
        if self.__status_bar is None:
            self.__status_bar = UnitStatusBar(group=Groups.objects, unit=cast(Unit, owner), offset=self.__offset)
        else:
            self.__status_bar.update()

    def render(self, owner: object, queue: DrawQueue):
        if self.__status_bar is not None:
            self.__status_bar.render(queue=queue)
