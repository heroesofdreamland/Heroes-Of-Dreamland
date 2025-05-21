from typing import Optional, cast, TypeVar

from logic.core.unit_ai.astar_pathfinder import AStarPathfinder
from logic.core.unit_ai.line_of_sight_checker import LineOfSightChecker
from logic.core.unit_ai.path_smoother import PathSmoother
from logic.core.unit_ai.types import ContinuousPoint, ContinuousPath, GridPoint, GridPath
from logic.level_design.maps.utils.map_cell import MapCell
from logic.level_design.maps.utils.map_iterator import iterate_map

T = TypeVar('T')


class MapPathfinder:
    def __init__(self, width: int, height: int, elements: list[list[MapCell]], cell_size: int):
        self.__cell_size = cell_size
        # Units with radius less than 20 can use regular map grid
        self.__maze_x1 = [[0 for _ in range(height)] for _ in range(width)]
        # Units with bigger radius should use more granular grid
        self.__maze_x2 = [[0 for _ in range(2 * height)] for _ in range(2 * width)]
        iterate_map(elements=elements, action=lambda cell, index: self.__fill_data_arrays(cell=cell, index=index))
        self.__adjust_maze_x2(width=2 * width, height=2 * height)
        self.__pathfinder_x1 = AStarPathfinder(elements=self.__maze_x1)
        self.__pathfinder_x2 = AStarPathfinder(elements=self.__maze_x2)
        # LineOfSightChecker and PathSmoother should use x1 grid
        self.__line_of_sight_checker = LineOfSightChecker(cell_size=cell_size, elements=self.__maze_x1)
        self.__path_smoother = PathSmoother(line_of_sight_checker=self.__line_of_sight_checker)

    def __granularity(self, unit_radius: float) -> int:
        if 2 * unit_radius < self.__cell_size:
            return 1
        else:
            return 2

    def __pathfinder(self, granularity: int) -> AStarPathfinder:
        if granularity == 1:
            return self.__pathfinder_x1
        else:
            return self.__pathfinder_x2

    def find_closest_enemy(self, start: ContinuousPoint, radius: float, enemies: list[T]) -> Optional[T]:
        granularity = self.__granularity(unit_radius=radius)
        pathfinder = self.__pathfinder(granularity=granularity)
        points = self.__enemies_grid_positions(enemies=enemies, granularity=granularity)
        closest_point_index = pathfinder.find_closest_point_index(start=self.__cell_index(coordinate=start, granularity=granularity), points=points)
        if closest_point_index is None:
            return None
        else:
            return enemies[closest_point_index]

    def find_path(self, start: ContinuousPoint, end: ContinuousPoint, radius: float) -> ContinuousPath:
        if self.is_path_clear(start=start, end=end, radius=radius):
            return [end]
        granularity = self.__granularity(unit_radius=radius)
        pathfinder = self.__pathfinder(granularity=granularity)
        grid_path = pathfinder.find_shortest_path(start=self.__cell_index(start, granularity=granularity), end=self.__cell_index(end, granularity=granularity))
        continuous_path = self.__convert_path(grid_path=grid_path, granularity=granularity)
        continuous_path.append(end)
        continuous_path = self.__path_smoother.smooth_path(path=continuous_path, radius=radius)
        if len(continuous_path) >= 2:
            x, y = continuous_path[1]
            if self.is_path_clear(start=start, end=(x, y), radius=radius):
                # Drop the first point if the second is directly reachable
                continuous_path.pop(0)
        return continuous_path

    def is_path_clear(self, start: ContinuousPoint, end: ContinuousPoint, radius: float) -> bool:
        return self.__line_of_sight_checker.is_path_clear(start=start, end=end, radius=radius)

    def __enemies_grid_positions(self, enemies: list[T], granularity: int) -> list[GridPoint]:
        from logic.entities.units.brains.unit_brain import Unit
        points = []
        for enemy in enemies:
            enemy_position = cast(Unit, enemy).position
            points.append(self.__cell_index(coordinate=(enemy_position.x, enemy_position.y), granularity=granularity))
        return points

    def __convert_path(self, grid_path: GridPath, granularity: int) -> ContinuousPath:
        result = []
        for index in grid_path:
            result.append(self.__cell_center(index=index, granularity=granularity))
        return result

    def __cell_center(self, index: GridPoint, granularity: int) -> ContinuousPoint:
        cell_size = self.__cell_size / granularity
        return index[0] * cell_size + cell_size / 2, index[1] * cell_size + cell_size / 2

    def __cell_index(self, coordinate: ContinuousPoint, granularity: int) -> GridPoint:
        cell_size = self.__cell_size / granularity
        x = int(coordinate[0] / cell_size)
        y = int(coordinate[1] / cell_size)
        return x, y

    def __fill_data_arrays(self, cell: MapCell, index: GridPoint):
        is_obstacle = False
        match cell:
            case MapCell.EXIT:
                is_obstacle = True
            case MapCell.WALL:
                is_obstacle = True

        if is_obstacle:
            self.__maze_x1[index[0]][index[1]] = 1
            self.__maze_x2[2 * index[0]][2 * index[1]] = 1
            self.__maze_x2[2 * index[0] + 1][2 * index[1]] = 1
            self.__maze_x2[2 * index[0]][2 * index[1] + 1] = 1
            self.__maze_x2[2 * index[0] + 1][2 * index[1] + 1] = 1

    def __adjust_maze_x2(self, width: int, height: int):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for x in range(width):
            for y in range(height):
                if self.__maze_x2[x][y] == 1:
                    for dx, dy in directions:
                        new_x = x + dx
                        new_y = y + dy
                        if 0 <= new_y < height and 0 <= new_x < width and self.__maze_x2[new_x][new_y] == 0:
                            self.__maze_x2[new_x][new_y] = 2
        for x in range(width):
            for y in range(height):
                if self.__maze_x2[x][y] == 2:
                    self.__maze_x2[x][y] = 1
