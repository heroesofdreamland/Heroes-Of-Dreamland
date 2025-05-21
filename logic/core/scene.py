import warnings
from typing import Type

from logic.core.game_loop import GameLoop
from logic.core.lifecycle import Lifecycle


class Scene:
    def __init__(self, name: str, controllers: list[Lifecycle]):
        self.name = name
        self.__controllers = controllers

    def activate(self, loop: GameLoop):
        for controller in self.__controllers:
            loop.register(controller)

    def deactivate(self, loop: GameLoop):
        for controller in self.__controllers:
            loop.unregister(controller)


class SceneManager:
    def __init__(self, loop: GameLoop):
        self.__game_loop = loop
        self.__registered_scene_types: dict[str, Type] = {}
        self.__active_scene: Scene | None = None

    def register(self, scene_type: Type, name: str):
        self.__registered_scene_types[name] = scene_type

    def activate(self, name: str):
        if name not in self.__registered_scene_types:
            warnings.warn(type(self).__name__ + ": Attempt to activate unregistered scene with name '" + name + "'. Register it first!")
            return
        scene_type = self.__registered_scene_types[name]
        scene = scene_type()
        if self.__active_scene == scene:
            warnings.warn(type(self).__name__ + ": Attempt to activate already active scene '" + name + "'")
            return
        if self.__active_scene is not None:
            self.__active_scene.deactivate(loop=self.__game_loop)
        scene.activate(loop=self.__game_loop)
        self.__active_scene = scene

    def current_activated_scene(self):
        return self.__active_scene
