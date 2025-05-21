from typing import Callable

from logic.core.unit_ai.types import GridPoint
from logic.level_design.maps.utils.map_model import MapCell


def iterate_map(elements: list[list[MapCell]], action: Callable[[MapCell, GridPoint], None]):
    y = 0
    for line in elements:
        x = 0
        for cell in line:
            action(cell, (x, y))
            x += 1
        y += 1
