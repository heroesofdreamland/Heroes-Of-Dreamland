import math

from pymunk import Vec2d

from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.unit_life_state import UnitLifeState
from logic.entities.units.data.unit_side import UnitSide


class UnitDistancesHelper:
    @staticmethod
    def are_units_colliding(first: Unit, second: Unit) -> bool:
        return len(first.shape.shapes_collide(second.shape).points) > 0

    @staticmethod
    def is_unit_in_radius(center: Vec2d,
                          radius: float,
                          unit: Unit | None,
                          side: UnitSide | None = None,
                          should_be_alive: bool = True) -> bool:
        # Checks if the unit shape is in the specified circle.
        if unit is None:
            return False
        if should_be_alive and unit.life_state != UnitLifeState.ALIVE:
            return False

        unit_position = unit.position
        is_on_correct_side = True
        match side:
            case UnitSide.LEFT:
                is_on_correct_side = unit_position.x <= center.x
            case UnitSide.RIGHT:
                is_on_correct_side = unit_position.x >= center.x
        return is_on_correct_side and UnitDistancesHelper.distance_between_point_and_point(first=center, second=unit_position) <= radius + unit.shape.radius

    @staticmethod
    def distance_between_unit_and_unit(first: Unit, second: Unit) -> float:
        # Finds the distance between the shape of the first and the shape of the second unit.
        first_position = first.position
        second_position = second.position
        distance = math.hypot(first_position.x - second_position.x, first_position.y - second_position.y)
        return distance - first.shape.radius - second.shape.radius

    @staticmethod
    def distance_between_point_and_point(first: Vec2d, second: Vec2d) -> float:
        # Finds the distance between the points.
        return math.hypot(first.x - second.x, first.y - second.y)

    @staticmethod
    def units_in_radius(center: Vec2d,
                        radius: float,
                        units: list[Unit | None],
                        side: UnitSide | None = None) -> list[Unit]:
        # Returns the list of units in the specified circle.
        result: list[Unit] = []
        for unit in units:
            if unit is not None and UnitDistancesHelper.is_unit_in_radius(center=center, radius=radius, unit=unit, side=side):
                result.append(unit)
        return result

    @staticmethod
    def closest_unit(point: Vec2d, units: list[Unit | None]) -> tuple[Unit, float] | None:
        # Returns the closest unit to the specified point.
        result = None
        for unit in units:
            if unit is not None:
                unit_position = unit.position
                distance = math.hypot(point.x - unit_position.x, point.y - unit_position.y)
                if result is None or distance < result[1]:
                    result = unit, distance
        return result