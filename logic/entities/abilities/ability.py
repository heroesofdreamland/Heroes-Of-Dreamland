from typing import MutableSequence

from logic.core.draw_queue import DrawQueue


class Ability:
    def process_input(self, owner: object, events: MutableSequence):
        pass

    def pre_update(self, owner: object):
        pass

    def update(self, owner):
        pass

    def post_update(self, owner: object):
        pass

    def render(self, owner: object, queue: DrawQueue):
        pass
