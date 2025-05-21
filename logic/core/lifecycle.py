# Base controller class
from typing import MutableSequence

from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle_group import LifecycleGroup


class Lifecycle:
    def __init__(self, group: LifecycleGroup):
        self.group = group
        self.is_alive = True

    def process_input(self, events: MutableSequence):
        pass

    def pre_update(self):
        pass

    def update(self):
        pass

    def post_update(self):
        pass

    def render(self, queue: DrawQueue):
        pass
