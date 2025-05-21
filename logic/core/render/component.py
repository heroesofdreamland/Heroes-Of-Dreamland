from logic.core.draw_queue import DrawQueue, DrawAnchor
from logic.core.render.surface import Surface
from logic.core.render.types import Position


class Component:
    def __init__(self):
        pass

    def surface(self) -> Surface:
        pass

    def draw(self, position: Position, queue: DrawQueue, anchor: int = DrawAnchor.CENTER, game_space: bool = False, priority: int = 0):
        self.surface().render(queue=queue, position=position, anchor=anchor, game_space=game_space, priority=priority)
