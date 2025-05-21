from logic.core.unit_ai.line_of_sight_checker import LineOfSightChecker
from logic.core.unit_ai.types import ContinuousPath


class PathSmoother:
    def __init__(self, line_of_sight_checker: LineOfSightChecker):
        """
        Initialize the PathSmoother with a LineOfSightChecker instance and radius.

        :param line_of_sight_checker: An instance of LineOfSightChecker to check path clearance.
        """
        self.__line_of_sight_checker = line_of_sight_checker

    def smooth_path(self, path: ContinuousPath, radius: float) -> ContinuousPath:
        """
        Smooth the given path by removing unnecessary waypoints.

        :param path: The path to smooth, as a list of (x, y) coordinates.
        :param radius: The radius of the entity (e.g., enemy) to consider during path smoothing.
        :return: A smoothed path as a list of (x, y) coordinates.
        """
        if not path or len(path) <= 2:
            return path

        smoothed_path = [path[0]]  # Start with the first point
        current_point = path[0]

        for i in range(2, len(path)):
            if not self.__line_of_sight_checker.is_path_clear(current_point, path[i], radius):
                smoothed_path.append(path[i - 1])
                current_point = path[i - 1]

        smoothed_path.append(path[-1])  # Always include the last point
        return smoothed_path
