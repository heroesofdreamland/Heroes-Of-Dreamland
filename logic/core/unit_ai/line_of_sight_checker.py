import math

from logic.core.unit_ai.types import ContinuousPoint, GridPoint


class LineOfSightChecker:
    def __init__(self, cell_size: float, elements: list[list[int]]):
        self.__cell_size_reciprocal = 1 / cell_size
        self.__elements = elements
        self.__grid_width = len(self.__elements)
        self.__grid_height = len(self.__elements[0])
        self.__is_in_wall_cache: dict[GridPoint, bool] = {}
        self.__is_path_clear_cache: dict[tuple[tuple[int, int], tuple[int, int]], bool] = {}
        self.__step_size = 5

    def is_path_clear(self, start: ContinuousPoint, end: ContinuousPoint, radius: float) -> bool:
        if start == end:
            return True
        if radius == 0:
            s_x, s_y = start
            e_x, e_y = end
            return self.__is_path_clear(start=(int(s_x), int(s_y)), end=(int(e_x), int(e_y)))

        line1, line2 = self.__find_parallel_lines(start, end, radius)
        return self.__is_path_clear(*line1) and self.__is_path_clear(*line2)

    def __is_path_clear(self, start: tuple[int, int], end: tuple[int, int]) -> bool:
        """Check if the line between start and end is clear, checking only at grid cell boundaries."""
        key = start, end
        if key in self.__is_path_clear_cache:
            return self.__is_path_clear_cache[key]

        distance = math.hypot(end[0] - start[0], end[1] - start[1])
        num_steps = int(distance // self.__step_size)

        if num_steps == 0:
            self.__is_path_clear_cache[key] = True
            return True

        x, y = start
        diff_x = (end[0] - start[0]) / num_steps
        diff_y = (end[1] - start[1]) / num_steps

        last_checked_grid = int(x * self.__cell_size_reciprocal), int(y * self.__cell_size_reciprocal)

        for i in range(num_steps + 1):
            current_grid = int(x * self.__cell_size_reciprocal), int(y * self.__cell_size_reciprocal)
            if current_grid != last_checked_grid:
                if self.__is_in_wall(point=current_grid):
                    self.__is_path_clear_cache[key] = False
                    return False
                last_checked_grid = current_grid
            x += diff_x
            y += diff_y

        self.__is_path_clear_cache[key] = True
        return True

    def __is_in_wall(self, point: GridPoint) -> bool:
        """Check if a point is in a wall cell, caching grid checks based on grid coordinates."""
        if point in self.__is_in_wall_cache:
            return self.__is_in_wall_cache[point]

        grid_x, grid_y = point

        result = False
        if 0 <= grid_x < self.__grid_width and 0 <= grid_y < self.__grid_height:
            result = self.__elements[grid_x][grid_y] == 1
        self.__is_in_wall_cache[point] = result
        return result

    @staticmethod
    def __find_parallel_lines(start: ContinuousPoint, end: ContinuousPoint, radius: float) -> tuple[tuple, tuple]:
        """Find two parallel lines at a given radius offset from the main line between start and end."""
        direction_vector = (end[0] - start[0], end[1] - start[1])
        length = math.hypot(direction_vector[0], direction_vector[1])
        direction_unit_vector = (direction_vector[0] / length, direction_vector[1] / length)

        perpendicular_vector = (-direction_unit_vector[1], direction_unit_vector[0])

        s1 = (int(start[0] + radius * perpendicular_vector[0]), int(start[1] + radius * perpendicular_vector[1]))
        s2 = (int(start[0] - radius * perpendicular_vector[0]), int(start[1] - radius * perpendicular_vector[1]))
        e1 = (int(end[0] + radius * perpendicular_vector[0]), int(end[1] + radius * perpendicular_vector[1]))
        e2 = (int(end[0] - radius * perpendicular_vector[0]), int(end[1] - radius * perpendicular_vector[1]))

        return (s1, e1), (s2, e2)
