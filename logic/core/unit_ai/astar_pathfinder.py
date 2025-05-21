import heapq

from logic.core.unit_ai.types import GridPoint, GridPath


class AStarPathfinder:
    def __init__(self, elements: list[list[int]]):
        self.__elements = elements
        self.__grid_width = len(self.__elements)
        self.__grid_height = len(self.__elements[0])
        self.__cache = {}

    def find_shortest_path(self, start: GridPoint, end: GridPoint) -> GridPath:
        """Finds the shortest path from start to end using bidirectional A* search."""
        cache_key = (start, end)
        if cache_key in self.__cache:
            return self.__cache[cache_key]

        # If start or end is not walkable, find the closest walkable points
        if not self.__is_walkable(start):
            start = self.__find_closest_walkable_point(start)
            if start is None:
                self.__cache[cache_key] = []
                return []  # No reachable points from the original start

        if not self.__is_walkable(end):
            end = self.__find_closest_walkable_point(end)
            if end is None:
                self.__cache[cache_key] = []
                return []  # No reachable points from the original end

        if start == end:
            self.__cache[cache_key] = [start]
            return [start]

        # Priority queues for forward and backward search
        forward_open_set = []
        backward_open_set = []
        heapq.heappush(forward_open_set, (0, start))
        heapq.heappush(backward_open_set, (0, end))

        # Dictionaries to store the g-scores and paths from both directions
        forward_g_score = {start: 0}
        backward_g_score = {end: 0}
        forward_came_from = {}
        backward_came_from = {}

        meeting_point = None

        while forward_open_set and backward_open_set:
            # Expand forward search
            if self.__expand_search(forward_open_set, forward_g_score, forward_came_from, backward_g_score, end):
                meeting_point = self.__get_meeting_point(forward_g_score, backward_g_score)
                break

            # Expand backward search
            if self.__expand_search(backward_open_set, backward_g_score, backward_came_from, forward_g_score, start):
                meeting_point = self.__get_meeting_point(forward_g_score, backward_g_score)
                break

        # If no meeting point was found, return an empty path
        if meeting_point is None:
            self.__cache[cache_key] = []
            return []

        # Construct the final path from start to end through the meeting point
        final_path = self.__construct_bidirectional_path(forward_came_from, backward_came_from, meeting_point)
        self.__cache[cache_key] = final_path
        return final_path

    def find_closest_point_index(self, start: GridPoint, points: list[GridPoint]) -> int | None:
        """Finds the closest point index to the start position."""
        closest_point_index = None
        result_normal_path = None

        for index, point in enumerate(points):
            normal_path = self.find_shortest_path(start, point)
            if not normal_path:
                continue
            if result_normal_path is None or len(normal_path) < len(result_normal_path):
                result_normal_path = normal_path
                closest_point_index = index

        return closest_point_index

    def __expand_search(self, open_set, g_score, came_from, other_g_score, target):
        """Helper function to expand the search in one direction."""
        _, current = heapq.heappop(open_set)
        if current in other_g_score:
            return True  # Indicate that a meeting point has been found

        x, y = current
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        for neighbor in neighbors:
            if self.__is_walkable(neighbor):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.__normal_heuristic(neighbor, target)
                    heapq.heappush(open_set, (f_score, neighbor))

        return False

    @staticmethod
    def __get_meeting_point(forward_g_score, backward_g_score) -> GridPoint | None:
        """Finds the best meeting point with the lowest combined g-score."""
        min_cost = float('inf')
        meeting_point = None
        for point in forward_g_score.keys() & backward_g_score.keys():
            cost = forward_g_score[point] + backward_g_score[point]
            if cost < min_cost:
                min_cost = cost
                meeting_point = point
        return meeting_point

    def __construct_bidirectional_path(self, forward_came_from, backward_came_from, meeting_point):
        """Constructs the final path from start to end through the meeting point."""
        path_from_start = self.__reconstruct_path(forward_came_from, meeting_point)
        path_from_end = self.__reconstruct_path(backward_came_from, meeting_point)
        path_from_end.reverse()  # Reverse the backward path to join it with the forward path
        return path_from_start + path_from_end[1:]  # Avoid duplicate meeting point

    def __is_walkable(self, point: GridPoint) -> bool:
        """Check if the given point is within bounds and walkable."""
        x, y = point
        return self.__grid_width > x >= 0 and 0 <= y < self.__grid_height and self.__elements[x][y] != 1

    def __find_closest_walkable_point(self, point: GridPoint) -> GridPoint | None:
        """Find the closest walkable point to the given start or end point."""
        x, y = point
        visited = set()
        queue = [(x, y, 0)]  # (x, y, distance)

        while queue:
            cx, cy, dist = queue.pop(0)
            if self.__is_walkable((cx, cy)):
                return cx, cy

            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))

            # Explore neighbors
            neighbors = [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]
            for nx, ny in neighbors:
                if 0 <= nx < self.__grid_width and 0 <= ny < self.__grid_height:
                    queue.append((nx, ny, dist + 1))

        return None

    @staticmethod
    def __normal_heuristic(a: GridPoint, b: GridPoint) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def __reconstruct_path(came_from: dict[GridPoint, GridPoint], current: GridPoint) -> GridPath:
        """Reconstructs the path from start to end by following the came_from map."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
