from queue import SimpleQueue
from typing import Callable

from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle import Lifecycle
from logic.core.lifecycle_group import LifecycleGroup
from logic.level_design.levels.level import Level
from logic.level_design.maps.utils.map_model import MapModel


class BaseMapController(Lifecycle):
    def __init__(self, group: LifecycleGroup, map_model: MapModel):
        super().__init__(group)
        self.map_model = map_model
        self.__queue = SimpleQueue()
        self.__current_level = None
        for level in self.levels(level_end_handler=self.__start_next_level):
            self.__queue.put(level)
        self.__start_next_level()

    def levels(self, level_end_handler: Callable) -> [Level]:
        return []

    def handle_levels_end(self):
        pass

    def pause_current_level(self, is_paused: bool):
        if self.__current_level is not None:
            self.__current_level.pause_level(is_paused=is_paused)

    def update(self):
        if self.__current_level is not None:
            self.__current_level.update()

    def render(self, queue: DrawQueue):
        self.map_model.renderer.render(queue=queue)

    def __start_next_level(self):
        if not self.__queue.empty():
            self.__current_level = self.__queue.get()
            self.__current_level.start_level()
        else:
            self.__current_level = None
            self.handle_levels_end()
