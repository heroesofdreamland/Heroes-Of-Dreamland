from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.lifecycle import Lifecycle


# BackgroundController responsibilities:
# - Rendering the background
class BackgroundController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)

    def render(self, queue: DrawQueue):
        pass
