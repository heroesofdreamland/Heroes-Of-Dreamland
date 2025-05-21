from logic.core.lifecycle_group import LifecycleGroup, LifecycleGroupIndex
from pymunk import Space

from logic.core.scene import SceneManager
from logic.events.event_manager import EventManager


class Groups:
    background = LifecycleGroup(index=LifecycleGroupIndex(index=0))
    __main_objects_index = LifecycleGroupIndex(index=1, sort_by_coordinate=True)
    level = LifecycleGroup(index=__main_objects_index)
    player = LifecycleGroup(index=__main_objects_index)
    objects = LifecycleGroup(index=__main_objects_index)
    gui = LifecycleGroup(index=LifecycleGroupIndex(index=3))
    transition = LifecycleGroup(index=LifecycleGroupIndex(index=4))
    menu = LifecycleGroup(index=LifecycleGroupIndex(index=5))
    foreground = LifecycleGroup(index=LifecycleGroupIndex(index=6))

    @staticmethod
    def reset():
        Groups.background.reset()
        Groups.level.reset()
        Groups.player.reset()
        Groups.objects.reset()
        Groups.gui.reset()
        Groups.menu.reset()


class Environment:
    player = None
    map = None
    orders = []
    scene_manager: SceneManager | None = None
    event_manager: EventManager | None = None

    @staticmethod
    def reset():
        Environment.player = None
        Environment.orders = []
        if Environment.map is not None:
            Environment.map.reset()
            Environment.map = None


class Spaces:
    SHARED = Space()
