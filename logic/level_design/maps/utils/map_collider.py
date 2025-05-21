import pymunk
import quads

from logic.core.unit_ai.types import GridPoint, ContinuousPoint


class MapCollider:
    def __init__(self, width: int, height: int, cell_size: int, wall_shapes: list[pymunk.Shape], exit_shapes: list[pymunk.Shape], exits: dict[GridPoint, tuple[str, str]]):
        self.__cell_size = cell_size
        self.__wall_shapes = wall_shapes
        self.__exit_shapes = exit_shapes
        self.__exits = exits
        self.__walls_quadtree = quads.QuadTree(
            center=(self.__cell_size * width / 2, self.__cell_size * height / 2),
            width=self.__cell_size * width,
            height=self.__cell_size * height
        )
        for index, wall_shape in enumerate(self.__wall_shapes):
            position = wall_shape.body.position
            self.__walls_quadtree.insert(point=(position.x, position.y), data=index)

    def is_shape_colliding_with_walls(self, shape: pymunk.Shape) -> bool:
        shape_position = shape.body.position
        wall_candidates = self.__walls_quadtree.nearest_neighbors(point=quads.Point(shape_position.x, shape_position.y), count=4)
        for candidate in wall_candidates:
            if self.__wall_shapes[candidate.data].shapes_collide(shape).points:
                return True
        return False

    def exit_colliding_with_shape(self, shape: pymunk.Shape) -> tuple[str, str] | None:
        for exit_shape in self.__exit_shapes:
            if exit_shape.sensor and exit_shape.shapes_collide(shape).points:
                position = exit_shape.body.position
                index = self.__cell_index(coordinate=(position.x, position.y))
                return self.__exits[index]
        return None

    def __cell_index(self, coordinate: ContinuousPoint) -> GridPoint:
        x = int(coordinate[0] / self.__cell_size)
        y = int(coordinate[1] / self.__cell_size)
        return x, y
