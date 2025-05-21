from pymunk import Vec2d

from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.lifecycle import Lifecycle
from logic.core.render.color import Color
from logic.core.timer import Timer
from logic.environment.environment import Environment
from logic.level_design.maps.utils.base_map_controller import BaseMapController
from logic.level_design.maps.utils.map_model import MapModel
from logic.level_design.maps.utils.map_parser import parse_map
from logic.utils.screen_dimmer import ScreenDimmer


class MapRootController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)
        self.__map_controllers: dict[str, BaseMapController] = {}
        self.__last_map_controller: BaseMapController | None = None

    def update(self):
        current_controller = self.__current_map_controller
        last_controller = self.__last_map_controller
        if current_controller != last_controller:
            if last_controller is not None:
                last_controller.pause_current_level(is_paused=True)
            if current_controller is not None:
                current_controller.pause_current_level(is_paused=False)
            self.__last_map_controller = current_controller
        if current_controller is not None:
            current_controller.update()

    def render(self, queue: DrawQueue):
        current_controller = self.__current_map_controller
        if current_controller is not None:
            current_controller.render(queue=queue)

    @property
    def __current_map_controller(self) -> BaseMapController | None:
        current_map_model = Environment.map
        if current_map_model is None:
            return None
        map_name = current_map_model.name
        if map_name not in self.__map_controllers:
            import importlib
            module = importlib.import_module('logic.level_design.maps.maps.' + map_name + '.map_controller')
            self.__map_controllers[map_name] = getattr(module, 'MapController')(group=self.group, map_model=current_map_model)
        return self.__map_controllers[map_name]


class MapTransitionController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)
        self.__map_switch_duration: float = 1.5
        self.__map_switch_timer = Timer(duration=self.__map_switch_duration)
        self.__current_map_model: MapModel | None = None
        self.__map_model_cache: dict[str, MapModel] = {}
        self.__switch_map(map_name='lobby', spawn_name='P0')
        self.__map_activated_exit: str | None = None

    def update(self):
        if self.__map_switch_timer.is_running():
            if self.__transition_progress >= 0.5 and self.__map_activated_exit is not None:
                map_name, spawn_name = self.__map_activated_exit
                self.__switch_map(map_name=map_name, spawn_name=spawn_name)
                self.__map_activated_exit = None
            elif self.__map_switch_timer.is_completed():
                self.__map_switch_timer.stop(group=self.group)
        else:
            activated_exit = self.__current_map_model.collider.exit_colliding_with_shape(shape=Environment.player.shape)
            if activated_exit is not None:
                self.__map_activated_exit = activated_exit
                self.__map_switch_timer.start(group=self.group)

    def render(self, queue: DrawQueue):
        if self.__map_switch_timer.is_running():
            ScreenDimmer(color=Color(0, 0, 0, int(self.__dim_screen_alpha * 255))).render(queue=queue)

    @property
    def __transition_progress(self) -> float:
        return min(1, self.__map_switch_timer.get_time() / self.__map_switch_duration)

    @property
    def __dim_screen_alpha(self) -> float:
        percentage = self.__transition_progress
        if percentage < 0.2:
            return percentage / 0.2
        elif percentage > 0.8:
            return (1 - percentage) / 0.2
        else:
            return 1

    def __switch_map(self, map_name: str, spawn_name: str):
        if self.__current_map_model is not None:
            self.__current_map_model.enable_physics(enable=False)
        new_map = self.__cached_map_model(name=map_name)
        if new_map is not None:
            spawn_point = new_map.cell_center(index=new_map.find_cell(name=spawn_name))
            Environment.map = new_map
            Environment.player.set_position(position=Vec2d(x=spawn_point[0], y=spawn_point[1]))
            new_map.enable_physics(enable=True)
            self.__current_map_model = new_map
        else:
            Environment.map = None
            self.__current_map_model = None

    def __cached_map_model(self, name: str) -> MapModel | None:
        if name not in self.__map_model_cache:
            self.__map_model_cache[name] = parse_map(
                name=name,
                path='logic/level_design/maps/maps/' + name + '/' + name + '.map'
            )
        return self.__map_model_cache[name]
