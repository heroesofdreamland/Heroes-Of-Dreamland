from typing import MutableSequence

from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle import Lifecycle
from logic.core.lifecycle_group import LifecycleGroup
from logic.environment.environment import Environment


class ObjectsController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)

    def pre_update(self):
        self.__pre_update_array(Environment.map.enemies)
        self.__pre_update_array(Environment.map.summons)
        self.__pre_update_array(Environment.map.neutrals)
        self.__pre_update_array(Environment.map.objects)

    @staticmethod
    def __pre_update_array(array: MutableSequence[Lifecycle]):
        for obj in array:
            obj.pre_update()

    def update(self):
        self.__update_array(Environment.map.enemies)
        self.__update_array(Environment.map.summons)
        self.__update_array(Environment.map.neutrals)
        self.__update_array(Environment.map.objects)

    @staticmethod
    def __update_array(array: MutableSequence[Lifecycle]):
        for obj in array:
            obj.update()

    def post_update(self):
        self.__post_update_array(Environment.map.enemies)
        self.__post_update_array(Environment.map.summons)
        self.__post_update_array(Environment.map.neutrals)
        self.__post_update_array(Environment.map.objects)

    @staticmethod
    def __post_update_array(array: MutableSequence[Lifecycle]):
        objects_to_remove = []
        for obj in array:
            obj.post_update()
            if not obj.is_alive:
                objects_to_remove.append(obj)
        for obj in objects_to_remove:
            array.remove(obj)

    def render(self, queue: DrawQueue):
        self.__render_array(Environment.map.enemies, queue)
        self.__render_array(Environment.map.summons, queue)
        self.__render_array(Environment.map.neutrals, queue)
        self.__render_array(Environment.map.objects, queue)

    @staticmethod
    def __render_array(array: MutableSequence[Lifecycle], queue: DrawQueue):
        for obj in array:
            obj.render(queue)

    def process_input(self, events: MutableSequence):
        self.__process_input_array(Environment.map.enemies, events)
        self.__process_input_array(Environment.map.summons, events)
        self.__process_input_array(Environment.map.neutrals, events)
        self.__process_input_array(Environment.map.objects, events)

    @staticmethod
    def __process_input_array(array: MutableSequence[Lifecycle], events: MutableSequence):
        for obj in array:
            obj.process_input(events)