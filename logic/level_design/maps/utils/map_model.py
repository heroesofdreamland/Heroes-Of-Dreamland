import random

import pymunk
from pymunk import Vec2d, Body, Poly

from logic.core.lifecycle import Lifecycle
from logic.core.unit_ai.types import ContinuousPoint, GridPoint
from logic.environment.environment import Environment, Spaces
from logic.level_design.maps.utils.map_cell import MapCell
from logic.level_design.maps.utils.map_collider import MapCollider
from logic.level_design.maps.utils.map_iterator import iterate_map
from logic.level_design.maps.utils.map_pathfinder import MapPathfinder
from logic.level_design.maps.utils.map_renderer import MapRenderer
from logic.settings.debug_settings import DebugSettings


class MapData:
    def __init__(self,
                 exits: dict[GridPoint, tuple[str, str]],
                 wall_tile: str | None,
                 floor_tile: str | None,
                 wall_height: int):
        self.exits = exits
        self.wall_tile = wall_tile
        self.floor_tile = floor_tile
        self.wall_height = wall_height


class MapModel:
    cell_size = 40

    def __init__(self, name: str, width: int, height: int, elements: list[list[MapCell]], data: MapData):
        self.name = name
        self.width = width
        self.height = height
        self.elements = elements
        self.data = data
        self.enemies: list = []
        self.summons: list = []
        self.neutrals: list = []
        self.objects: list[Lifecycle] = []
        self.__wall_shapes: list[pymunk.Shape] = []
        self.__exit_shapes: list[pymunk.Shape] = []
        self.__spawn_positions: list[GridPoint] = []
        iterate_map(elements=elements, action=lambda cell, index: self.__fill_data_arrays(cell=cell, index=index))
        self.renderer = MapRenderer(
            elements=elements,
            cell_size=self.cell_size,
            floor_tile=data.floor_tile,
            wall_tile=data.wall_tile,
            wall_height=data.wall_height
        )
        self.pathfinder = MapPathfinder(
            width=width,
            height=height,
            elements=elements,
            cell_size=self.cell_size
        )
        self.collider = MapCollider(
            width=width,
            height=height,
            cell_size=self.cell_size,
            wall_shapes=self.__wall_shapes,
            exit_shapes=self.__exit_shapes,
            exits=self.data.exits
        )

    def reset(self):
        self.enemies = []
        self.summons = []
        self.neutrals = []
        self.objects = []
        self.enable_physics(enable=False)

    def enable_exits(self, enable: bool):
        if DebugSettings.debug_settings['always_enable_map_exits']:
            enable = True
        for exit_shape in self.__exit_shapes:
            exit_shape.friction = 0 if enable else 1
            exit_shape.sensor = enable

    def enable_physics(self, enable: bool):
        if enable:
            for wall_shape in self.__wall_shapes:
                Spaces.SHARED.add(wall_shape.body, wall_shape)
            for exit_shape in self.__exit_shapes:
                Spaces.SHARED.add(exit_shape.body, exit_shape)
        else:
            for wall_shape in self.__wall_shapes:
                Spaces.SHARED.remove(wall_shape.body, wall_shape)
            for exit_shape in self.__exit_shapes:
                Spaces.SHARED.remove(exit_shape.body, exit_shape)
        for obj in self.enemies + self.summons + self.neutrals:
            obj.enable_physics(enable=enable)
        for obj in self.objects:
            if hasattr(obj, 'enable_physics') and callable(getattr(obj, 'enable_physics')):
                obj.enable_physics(enable=enable)

    def random_spawn_position(self, distance_from_player: int = 4) -> Vec2d:
        player_position = Environment.player.position
        player_index = self.__cell_index(coordinate=(player_position.x, player_position.y))
        valid_positions = [pos for pos in self.__spawn_positions if abs(player_index[0] - pos[0]) + abs(player_index[1] - pos[1]) > distance_from_player]

        if valid_positions:
            index = random.choice(valid_positions)
        else:
            index = random.choice(self.__spawn_positions)
        position = self.cell_center(index=index)
        return Vec2d(x=position[0], y=position[1])

    def find_cell(self, name: str) -> GridPoint:
        cell = MapCell(name[0])
        index = int(name[1:])
        count = 0

        for j, row in enumerate(self.elements):
            for i, element in enumerate(row):
                if element == cell:
                    if count == index:
                        return i, j
                    count += 1
        # If the n-th occurrence is not found, raise an exception or return a default value
        raise ValueError(f"The {index}-th occurrence of the given cell was not found.")

    def cell_center(self, index: GridPoint) -> ContinuousPoint:
        return index[0] * self.cell_size + self.cell_size / 2, index[1] * self.cell_size + self.cell_size / 2

    def __fill_data_arrays(self, cell: MapCell, index: GridPoint):
        cell_center = self.cell_center(index=index)
        match cell:
            case MapCell.SPACE:
                self.__spawn_positions.append(index)
            case MapCell.EXIT:
                exit_body = Body(body_type=Body.STATIC)
                exit_body.position = cell_center
                vertices = [
                    (-self.cell_size / 8, -self.cell_size / 8),  # Bottom left
                    (self.cell_size / 8, -self.cell_size / 8),  # Bottom right
                    (self.cell_size / 8, self.cell_size / 8),  # Top right
                    (-self.cell_size / 8, self.cell_size / 8),  # Top left
                ]
                exit_shape = Poly(exit_body, vertices)
                exit_shape.elasticity = 0.0
                self.__exit_shapes.append(exit_shape)
            case MapCell.WALL:
                wall_body = Body(body_type=Body.STATIC)
                wall_body.position = cell_center
                vertices = [
                    (-self.cell_size / 2, -self.cell_size / 2),  # Bottom left
                    (self.cell_size / 2, -self.cell_size / 2),  # Bottom right
                    (self.cell_size / 2, self.cell_size / 2),  # Top right
                    (-self.cell_size / 2, self.cell_size / 2),  # Top left
                ]
                wall_shape = Poly(wall_body, vertices)
                wall_shape.friction = 1.0
                wall_shape.elasticity = 0.0
                self.__wall_shapes.append(wall_shape)

    def __cell_index(self, coordinate: ContinuousPoint) -> GridPoint:
        x = int(coordinate[0] / self.cell_size)
        y = int(coordinate[1] / self.cell_size)
        return x, y
