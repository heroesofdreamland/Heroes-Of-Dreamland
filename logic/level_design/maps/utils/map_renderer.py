from logic.core.draw_queue import DrawQueue, DrawAnchor
from logic.core.isometry import cartesian_to_isometric
from logic.core.opengl import SurfaceIdentifier
from logic.core.resource_cache import cached_image
from logic.core.screen import Screen
from logic.core.unit_ai.types import GridPoint, ContinuousPoint
from logic.level_design.maps.utils.map_cell import MapCell
from logic.level_design.maps.utils.map_iterator import iterate_map


class MapRenderer:
    def __init__(self,
                 elements: list[list[MapCell]],
                 cell_size: int,
                 wall_tile: str | None,
                 floor_tile: str | None,
                 wall_height: int):
        self.__cell_size = cell_size
        self.__wall_tile = wall_tile
        self.__wall_tile_coordinates: dict[float, tuple[ContinuousPoint, list[ContinuousPoint]]] = {}
        self.__floor_tile = floor_tile
        self.__floor_tile_coordinates: list[ContinuousPoint] = []
        self.__wall_height = wall_height
        iterate_map(elements=elements, action=lambda cell, index: self.__fill_data_arrays(cell=cell, index=index))
        self.__wall_tile_z_indices: list[float] = sorted(self.__wall_tile_coordinates.keys())

    def render(self, queue: DrawQueue):
        scale = Screen.get_screen_scale() * 2.4
        if self.__floor_tile is not None:
            image = cached_image(path='resources/used_resources/tiles/tile_' + self.__floor_tile + '.png', scale=scale)
            queue.draw_surfaces(surface=image,
                                identifier=SurfaceIdentifier(identifier="map_tile_" + self.__floor_tile),
                                positions=self.__floor_tile_coordinates,
                                anchor=DrawAnchor.CENTER,
                                game_space=True,
                                priority=-2)
        if self.__wall_tile is not None:
            image = cached_image(path='resources/used_resources/tiles/tile_' + self.__wall_tile + '.png', scale=scale)
            for index in self.__wall_tile_z_indices:
                batch_iso_position, positions = self.__wall_tile_coordinates[index]
                queue.draw_surfaces(surface=image,
                                    identifier=SurfaceIdentifier(identifier="map_tile_" + self.__wall_tile),
                                    positions=positions,
                                    batch_iso_position=batch_iso_position,
                                    anchor=DrawAnchor.CENTER,
                                    game_space=True,
                                    priority=0)

    def __cell_center(self, index: GridPoint) -> ContinuousPoint:
        return index[0] * self.__cell_size + self.__cell_size / 2, index[1] * self.__cell_size + self.__cell_size / 2

    def __fill_data_arrays(self, cell: MapCell, index: GridPoint):
        cell_center = self.__cell_center(index)
        self.__floor_tile_coordinates.append(cell_center)
        match cell:
            case MapCell.WALL:
                iso_wall_center = cartesian_to_isometric(coordinate=cell_center)
                z_index = iso_wall_center[1]  # depth is measured by y-index in isometric space
                if z_index not in self.__wall_tile_coordinates:
                    self.__wall_tile_coordinates[z_index] = (iso_wall_center, [])

                for index in range(1, self.__wall_height + 1):
                    wall_level_center = cell_center[0] - index * 20, cell_center[1] - index * 20
                    self.__wall_tile_coordinates[z_index][1].append(wall_level_center)
