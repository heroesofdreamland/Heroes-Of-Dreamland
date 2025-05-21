from enum import Enum


class MapCell(Enum):
    WALL = 'W'
    PLAYER = 'P'
    EXIT = 'E'
    SPACE = ' '
