import math

from pymunk import Vec2d, Shape

from logic.core.animated_object import AnimatedObject
from logic.core.draw_queue import DrawQueue
from logic.core.isometry import cartesian_to_isometric
from logic.core.lifecycle import Lifecycle
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.timer import Timer
from logic.environment.environment import Environment, Spaces
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.damage_data import DamageData
from logic.entities.units.models.animation_type import AnimationType


class Projectile(Lifecycle):
    def __init__(self,
                 position: Vec2d,
                 shape: Shape,
                 animated_object: AnimatedObject,
                 speed: float,
                 damage_data: DamageData,
                 group: LifecycleGroup,
                 enemies_provider: EnemiesProvider):
        super().__init__(group)
        self.__is_in_space = False
        self.__animated_object = animated_object
        self.__speed = speed
        self.__damage_data = damage_data
        self.__shape = shape
        self.__shape.body.position = position
        self.__animated_object.configure_animation(AnimationType.FLIES)
        self.__enemies_provider = enemies_provider
        self.__owner: Unit | None = None
        self.__direction: Vec2d | None = None
        self.__timer = Timer(duration=10)

    @property
    def shape_radius(self) -> float:
        return self.__shape.radius

    def enable_physics(self, enable: bool):
        if enable and not self.__is_in_space:
            Spaces.SHARED.add(self.__shape.body, self.__shape)
            self.__is_in_space = True
        elif not enable and self.__is_in_space:
            Spaces.SHARED.remove(self.__shape.body, self.__shape)
            self.__is_in_space = False

    def pre_update(self):
        self.__shape.body.velocity = [0, 0]

    def update(self):
        if self.__direction is not None:
            self.__shape.body.velocity = [self.__speed * self.__direction.x, self.__speed * self.__direction.y]
            self.__check_collisions(units=self.__enemies_provider())
            if self.__timer.is_completed():
                self.__timer.stop(group=self.group)
                self.is_alive = False

    def render(self, queue: DrawQueue):
        self.__animated_object.position = self.__shape.body.position
        queue.draw(group=self.group, animated_object=self.__animated_object, game_space=True)

    def launch(self, destination: Vec2d, owner: Unit | None, animation_offset: tuple[float, float]):
        self.enable_physics(enable=True)
        self.__owner = owner
        start_position = self.__shape.body.position
        direction_x = destination.x - start_position.x
        direction_y = destination.y - start_position.y
        distance = math.hypot(direction_x, direction_y)
        self.__direction = Vec2d(x=direction_x / distance, y=direction_y / distance)
        self.__timer.start(group=self.group)
        iso_destination = cartesian_to_isometric(coordinate=(destination.x, destination.y))
        iso_start_position = cartesian_to_isometric(coordinate=(start_position.x, start_position.y))
        iso_direction_x = iso_destination[0] - iso_start_position[0]
        iso_direction_y = iso_destination[1] - iso_start_position[1]
        self.__animated_object.offset = animation_offset
        self.__animated_object.angle = -math.atan2(iso_direction_y, iso_direction_x) * 180 / math.pi

    def __check_collisions(self, units: list[Unit | None]):
        for unit in units:
            if unit is not None and self.__shape.shapes_collide(unit.shape).points:
                unit.get_damage(damage_data=self.__damage_data, attacker=self.__owner)
                self.is_alive = False
                return
        if Environment.map.collider.is_shape_colliding_with_walls(self.__shape):
            self.is_alive = False
            return
