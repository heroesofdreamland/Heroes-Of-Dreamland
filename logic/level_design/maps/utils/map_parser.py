import warnings

from logic.core.unit_ai.types import GridPoint
from logic.level_design.maps.utils.map_model import MapModel, MapCell, MapData


def parse_map(name: str, path: str) -> MapModel:
    map_array = []
    width = 0
    height = 0
    data_mode = False
    graphics_mode = False
    wall_tile: str | None = None
    floor_tile: str | None = None
    wall_height: int = 1
    exits: dict[GridPoint, tuple[str, str]] = {}
    with open(path) as map_file:
        for line in map_file:
            if line == "==== DATA ====\n":
                data_mode = True
                continue
            if line == "==== GRAPHICS ====\n":
                graphics_mode = True
                continue
            if graphics_mode:
                element, data = __parse_data(line)
                if element == "wall":
                    wall_tile = data
                if element == "floor":
                    floor_tile = data
                if element == "height":
                    wall_height = int(data)
                continue
            if data_mode:
                element, data = __parse_data(line)
                cell = MapCell(element[0])
                index = int(element[1:])
                point = __find_point(map_array, cell, index)
                match cell:
                    case MapCell.EXIT:
                        map_name, spawn_point = map(str.strip, data.split(","))
                        exits[point] = map_name, spawn_point
                continue
            line_array = []
            height += 1
            line_width = 0
            for char in line:
                if char == '\n':
                    continue
                try:
                    cell = MapCell(char)
                    line_width += 1
                    line_array.append(cell)
                except ValueError:
                    warnings.warn("Attempt to parse map with unknown character '" + char + "'. Add it to the MapCell enumeration!")

            if line_width > width:
                width = line_width
            map_array.append(line_array)
    data = MapData(exits=exits, wall_tile=wall_tile, floor_tile=floor_tile, wall_height=wall_height)
    return MapModel(name=name, width=width, height=height, elements=map_array, data=data)


def __parse_data(s: str) -> tuple[str, str]:
    # Split the string by '->' and strip any whitespace from both parts
    key, value = map(str.strip, s.split("->"))
    return key, value


def __find_point(elements: list[list[MapCell]], cell: MapCell, n: int) -> GridPoint:
    count = 0

    for j, row in enumerate(elements):
        for i, element in enumerate(row):
            if element == cell:
                if count == n:
                    return i, j
                count += 1
    # If the n-th occurrence is not found, raise an exception or return a default value
    raise ValueError(f"The {n}-th occurrence of the given cell was not found.")

