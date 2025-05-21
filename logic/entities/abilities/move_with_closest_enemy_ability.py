import math
from enum import Enum
from typing import cast

from pymunk import Vec2d

from logic.entities.abilities.ability import Ability
from logic.core.draw_queue import DrawQueue
from logic.core.isometry import cartesian_to_isometric
from logic.core.timer import Timer
from logic.core.unit_ai.types import ContinuousPath, ContinuousPoint
from logic.environment.environment import Groups, Environment
from logic.settings.debug_settings import DebugSettings
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.brains.helpers.unit_distances_helper import UnitDistancesHelper
from logic.entities.units.brains.mixins.unit_attack_mixin import AttackState
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.unit_life_state import UnitLifeState
from logic.entities.units.data.unit_side import UnitSide
from logic.ui.colors import Colors


class UnitMovementFSM(Enum):
    CHASE = 'chase'
    WAIT = 'wait'
    RETREAT = 'retreat'


class MoveWithClosestEnemyAbility(Ability):
    def __init__(self, retreat_chase_radius: tuple[float, float] | None, enemies_provider: EnemiesProvider):
        self.__retreat_chase_radius = retreat_chase_radius
        self.__enemies_provider = enemies_provider
        self.__pathfinding_timer = Timer(duration=0.5)
        self.__pathfinding_path: ContinuousPath = []
        self.__target_point: ContinuousPoint | None = None

    def update(self, owner):
        if owner.life_state != UnitLifeState.ALIVE:
            return
        if owner.attack_state != AttackState.NONE:
            owner.set_direction(x=0, y=0)
            return
        if self.__check_timer():
            owner_position = owner.position
            self.__refresh_path(owner=owner, owner_position=owner_position)
            self.__assign_new_waypoint()
        if self.__target_point is not None:
            owner_position = owner.position
            direction_x = self.__target_point[0] - owner_position.x
            direction_y = self.__target_point[1] - owner_position.y
            if math.hypot(direction_x, direction_y) >= owner.shape_radius / 2:
                owner.set_direction(x=direction_x, y=direction_y)
            else:
                self.__pathfinding_path.pop(0)
                self.__assign_new_waypoint()
        else:
            owner.set_direction(x=0, y=0)

    def render(self, owner: object, queue: DrawQueue):
        if DebugSettings.debug_settings['show_unit_pathfinding_path']:
            if self.__pathfinding_path is not None:
                owner_position = cast(Unit, owner).position
                prev_point = (owner_position.x, owner_position.y)
                for point in self.__pathfinding_path:
                    queue.debug_draw_circle(color=Colors.RED, position=point, radius=4, game_space=True)
                    queue.debug_draw_line(color=Colors.RED, start=prev_point, end=point, game_space=True)
                    prev_point = point

            if self.__target_point is not None:
                queue.debug_draw_circle(color=Colors.GREEN, position=self.__target_point, radius=3, game_space=True)

        if DebugSettings.debug_settings['show_unit_retreat_chase_radius'] and self.__retreat_chase_radius is not None:
            owner_position = cast(Unit, owner).position
            queue.debug_draw_circle(color=Colors.YELLOW, position=(owner_position.x, owner_position.y), radius=self.__retreat_chase_radius[0], game_space=True)
            queue.debug_draw_circle(color=Colors.GREEN, position=(owner_position.x, owner_position.y), radius=self.__retreat_chase_radius[1], game_space=True)

    def movement_state(self, owner: Unit, owner_position: Vec2d, closest_enemy: Unit) -> UnitMovementFSM:
        closest_enemy_position = closest_enemy.position
        distance_to_closest_enemy = UnitDistancesHelper.distance_between_point_and_point(first=owner_position, second=closest_enemy_position)
        if self.__retreat_chase_radius is None:
            if distance_to_closest_enemy >= owner.shape_radius + closest_enemy.shape_radius:
                return UnitMovementFSM.CHASE
            else:
                return UnitMovementFSM.WAIT
        else:
            if self.__retreat_chase_radius[0] >= distance_to_closest_enemy - closest_enemy.shape_radius:
                return UnitMovementFSM.RETREAT
            elif self.__retreat_chase_radius[1] <= distance_to_closest_enemy - closest_enemy.shape_radius:
                return UnitMovementFSM.CHASE
            elif Environment.map.pathfinder.is_path_clear(start=(owner_position.x, owner_position.y), end=(closest_enemy_position.x, closest_enemy_position.y), radius=owner.shape_radius):
                return UnitMovementFSM.WAIT
            else:
                return UnitMovementFSM.CHASE

    def __check_timer(self) -> bool:
        if not self.__pathfinding_timer.is_running():
            self.__pathfinding_timer.start(group=Groups.objects)
            return True
        if self.__pathfinding_timer.is_completed():
            self.__pathfinding_timer.stop(group=Groups.objects)
            return True
        return False

    def __refresh_path(self, owner: Unit, owner_position: Vec2d):
        self.__target_point = None
        closest_enemy = Environment.map.pathfinder.find_closest_enemy(start=owner_position, radius=owner.shape_radius, enemies=self.__enemies_provider())
        if closest_enemy is None:
            self.__pathfinding_path = []
            return
        closest_enemy_position = closest_enemy.position
        match self.movement_state(owner=owner, owner_position=owner_position, closest_enemy=closest_enemy):
            case UnitMovementFSM.CHASE:
                self.__pathfinding_path = Environment.map.pathfinder.find_path(
                    start=(owner_position.x, owner_position.y),
                    end=(closest_enemy_position.x, closest_enemy_position.y),
                    radius=owner.shape_radius
                )
            case UnitMovementFSM.WAIT:
                self.__pathfinding_path = []
                iso_x_direction = cartesian_to_isometric(coordinate=(closest_enemy_position.x - owner_position.x, closest_enemy_position.y - owner_position.y))[0]
                if iso_x_direction > 0.1:
                    owner.set_side(UnitSide.RIGHT)
                elif iso_x_direction < -0.1:
                    owner.set_side(UnitSide.LEFT)
            case UnitMovementFSM.RETREAT:
                self.__pathfinding_path = []

    def __assign_new_waypoint(self):
        self.__target_point = self.__pathfinding_path[0] if self.__pathfinding_path else None
