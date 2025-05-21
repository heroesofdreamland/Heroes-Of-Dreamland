from typing import Tuple
import pygame
import heapq
from collections import defaultdict
from pygame import Surface
from logic.core.animated_object import AnimatedObject
from logic.core.camera import Camera
from logic.core.isometry import cartesian_to_isometric, isometric_to_cartesian, Isometry
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.opengl import OpenGL, SurfaceIdentifier
from logic.core.render.color import Color
from logic.core.screen import Screen
from logic.core.structures.queue import Queue


class _ZIndexQueue:
    def __init__(self):
        self.__queue = []
        self.__z_index_map = defaultdict(list)
        self.__z_index_set = set()

    def enqueue(self, z_index, element):
        if z_index not in self.__z_index_set:
            heapq.heappush(self.__queue, z_index)
            self.__z_index_set.add(z_index)
        self.__z_index_map[z_index].append(element)

    def dequeue(self) -> list:
        z_index = heapq.heappop(self.__queue)
        self.__z_index_set.remove(z_index)
        return self.__z_index_map.pop(z_index, [])

    def is_empty(self):
        return not self.__queue

    def reset(self):
        self.__queue = []
        self.__z_index_map = defaultdict(list)
        self.__z_index_set = set()


class DrawAnchor:
    TOP_LEFT = 0
    CENTER_LEFT = 1
    BOTTOM_LEFT = 2
    TOP_CENTER = 3
    CENTER = 4
    BOTTOM_CENTER = 5
    TOP_RIGHT = 6
    CENTER_RIGHT = 7
    BOTTOM_RIGHT = 8


def modify_top_left_coordinate(anchor: int,
                               position: tuple[float, float],
                               size: tuple[float, float]) -> tuple[float, float]:
    x, y = position
    width, height = size

    if anchor == DrawAnchor.TOP_LEFT:
        return position
    if anchor == DrawAnchor.CENTER:
        return x - width / 2, y - height / 2
    if anchor == DrawAnchor.CENTER_LEFT:
        return x, y - height / 2
    if anchor == DrawAnchor.BOTTOM_LEFT:
        return x, y - height
    if anchor == DrawAnchor.TOP_CENTER:
        return x - width / 2, y
    if anchor == DrawAnchor.BOTTOM_CENTER:
        return x - width / 2, y - height
    if anchor == DrawAnchor.TOP_RIGHT:
        return x - width, y
    if anchor == DrawAnchor.CENTER_RIGHT:
        return x - width, y - height / 2
    if anchor == DrawAnchor.BOTTOM_RIGHT:
        return x - width, y - height


class _QueueObject:
    def __init__(self, game_space: bool, anchor: int, priority: int, iso_position: tuple[float, float]):
        self.__game_space = game_space
        self.__anchor = anchor
        self.__priority = priority
        self.__iso_position = iso_position

    def z_index(self) -> tuple[int, float]:
        return self.__priority, self.__iso_position[1]

    def draw(self, iso_camera: tuple[float, float], screen_scale: int, screen_size: tuple[int, int]):
        pass

    def convert(self, iso_camera: tuple[float, float], screen_scale: int, position: tuple[float, float],
                size: tuple[float, float]) -> tuple[float, float]:
        if self.__game_space:
            iso_x, iso_y = cartesian_to_isometric(coordinate=position)
            cam_x, cam_y = iso_camera
            position = (iso_x - cam_x) * screen_scale, (iso_y - cam_y) * screen_scale
        return modify_top_left_coordinate(anchor=self.__anchor, position=position, size=size)

    def __lt__(self, other):
        return (self.__priority, self.__iso_position[1], self.__iso_position[0]) < (
            other.__priority, other.__iso_position[1], other.__iso_position[0])

    def __eq__(self, other):
        return (self.__priority, self.__iso_position[1], self.__iso_position[0]) == (
            other.__priority, other.__iso_position[1], other.__iso_position[0])


class AnimatedQueueObject(_QueueObject):
    def __init__(self,
                 animated_object: AnimatedObject,
                 game_space: bool,
                 anchor: int,
                 priority: int):
        self.__animated_object = animated_object
        super().__init__(game_space=game_space, anchor=anchor, priority=priority, iso_position=cartesian_to_isometric(
            coordinate=(animated_object.position.x, animated_object.position.y)))

    def draw(self, iso_camera: tuple[float, float], screen_scale: int, screen_size: tuple[int, int]):
        texture = self.__animated_object.get_texture()
        if texture is None:
            return
        x_offset, y_offset = self.__animated_object.offset
        OpenGL.draw(texture=texture,
                    position=self.convert(iso_camera=iso_camera,
                                          screen_scale=screen_scale,
                                          position=(self.__animated_object.position.x + x_offset,
                                                    self.__animated_object.position.y + y_offset),
                                          size=texture.size),
                    screen_size=screen_size,
                    angle=self.__animated_object.angle)


class StaticQueueObject(_QueueObject):
    def __init__(self,
                 surface: Surface,
                 identifier: SurfaceIdentifier | None,
                 position: tuple[float, float],
                 game_space: bool,
                 anchor: int,
                 angle: float,
                 priority: int):
        self.__surface = surface
        self.__identifier = identifier
        self.__position = position
        self.__angle = angle
        super().__init__(game_space=game_space, anchor=anchor, priority=priority,
                         iso_position=cartesian_to_isometric(coordinate=position))

    def draw(self, iso_camera: tuple[float, float], screen_scale: int, screen_size: tuple[int, int]):
        texture = OpenGL.surface_texture(surface=self.__surface, identifier=self.__identifier)
        OpenGL.draw(texture=texture,
                    position=self.convert(iso_camera=iso_camera, screen_scale=screen_scale, position=self.__position,
                                          size=texture.size),
                    screen_size=screen_size,
                    angle=self.__angle)


class StaticBatchQueueObject(_QueueObject):
    def __init__(self,
                 surface: Surface,
                 identifier: SurfaceIdentifier | None,
                 positions: list[tuple[float, float]],
                 iso_position: tuple[float, float],
                 game_space: bool,
                 anchor: int,
                 angle: float,
                 priority: int):
        self.__surface = surface
        self.__identifier = identifier
        self.__positions = positions
        self.__angle = angle
        self.__game_space = game_space
        self.__anchor = anchor
        self.__priority = priority
        super().__init__(game_space=game_space, anchor=anchor, priority=priority, iso_position=iso_position)

    def draw(self, iso_camera: tuple[float, float], screen_scale: int, screen_size: tuple[int, int]):
        texture = OpenGL.surface_texture(surface=self.__surface, identifier=self.__identifier)
        positions = []
        for position in self.__positions:
            positions.append(
                self.convert(iso_camera=iso_camera, screen_scale=screen_scale, position=position, size=texture.size))
        OpenGL.draw_batch(texture=texture,
                          positions=positions,
                          screen_size=screen_size,
                          angle=self.__angle)


class DrawQueue:
    def __init__(self):
        self.__queue = Queue()
        self.__z_index_queue = _ZIndexQueue()

    def draw(self,
             group: LifecycleGroup,
             animated_object: AnimatedObject,
             game_space: bool,
             anchor: int = DrawAnchor.CENTER,
             priority: int = 0):
        # Priority is needed for ordering elements of the same group: The higher priority is, the later the object will be drawn
        animated_object.pause_animation(not group.is_animation_enabled)
        if animated_object.is_animation_configured():
            obj = AnimatedQueueObject(animated_object=animated_object,
                                      game_space=game_space,
                                      priority=priority,
                                      anchor=anchor)
            self.__queue.enqueue(obj)
            self.__z_index_queue.enqueue(obj.z_index(), obj)

    def draw_surface(self,
                     surface: Surface,
                     identifier: SurfaceIdentifier | None,
                     position: tuple[float, float],
                     game_space: bool,
                     anchor: int = DrawAnchor.TOP_LEFT,
                     angle: float = 0,
                     priority: int = 0):
        # Priority is needed for ordering elements of the same group: The higher priority is, the later the object will be drawn
        obj = StaticQueueObject(surface=surface,
                                identifier=identifier,
                                position=position,
                                game_space=game_space,
                                anchor=anchor,
                                angle=angle,
                                priority=priority)
        self.__queue.enqueue(obj)
        self.__z_index_queue.enqueue(obj.z_index(), obj)

    def draw_surfaces(self,
                      surface: Surface,
                      identifier: SurfaceIdentifier | None,
                      positions: list[tuple[float, float]],
                      game_space: bool,
                      batch_iso_position: tuple[float, float] = (0, 0),
                      anchor: int = DrawAnchor.TOP_LEFT,
                      angle: float = 0,
                      priority: int = 0):
        # Priority is needed for ordering elements of the same group: The higher priority is, the later the object will be drawn
        obj = StaticBatchQueueObject(surface=surface,
                                     identifier=identifier,
                                     positions=positions,
                                     iso_position=batch_iso_position,
                                     game_space=game_space,
                                     anchor=anchor,
                                     angle=angle,
                                     priority=priority)
        self.__queue.enqueue(obj)
        self.__z_index_queue.enqueue(obj.z_index(), obj)

    def debug_draw_circle(self,
                          color: Color,
                          radius: float,
                          position: tuple[float, float],
                          game_space: bool,
                          priority: int = 0):
        scaled_radius = radius * Screen.get_screen_scale()
        ellipse_width = scaled_radius * 2
        ellipse_height = scaled_radius * 2
        if game_space:
            ellipse_height *= Isometry.scale_factor
        surface = pygame.Surface(size=(ellipse_width, ellipse_height), flags=pygame.SRCALPHA)
        ellipse_rect = pygame.Rect(0, 0, ellipse_width, ellipse_height)
        pygame.draw.ellipse(surface, color.color(), ellipse_rect, 2)
        identifier = SurfaceIdentifier(identifier="debug_circle" + "_" + str(color) + "_" + str(radius))
        self.draw_surface(surface=surface,
                          identifier=identifier,
                          position=position,
                          game_space=game_space,
                          anchor=DrawAnchor.CENTER,
                          priority=priority)

    def debug_draw_rect(self,
                        color: Color,
                        size: Tuple[float, float],
                        position: tuple[float, float],
                        game_space: bool,
                        anchor: int = DrawAnchor.TOP_LEFT,
                        angle: float = 0,
                        priority: int = 0):
        screen_scale = Screen.get_screen_scale()
        surface = pygame.Surface(size=[size[0] * screen_scale, size[1] * screen_scale], flags=pygame.SRCALPHA)
        pygame.draw.rect(surface, color.color(), (0, 0, size[0] * screen_scale, size[1] * screen_scale), 2)
        identifier = SurfaceIdentifier(
            identifier="debug_rect" + "_" + str(color) + "_" + str(size[0]) + "x" + str(size[1]))
        self.draw_surface(surface=surface,
                          identifier=identifier,
                          position=position,
                          game_space=game_space,
                          anchor=anchor,
                          angle=angle,
                          priority=priority)

    def debug_draw_line(self,
                        color: Color,
                        start: tuple[float, float],
                        end: tuple[float, float],
                        game_space: bool,
                        width: int = 2,
                        priority: int = 0):
        iso_start = cartesian_to_isometric(coordinate=start) if game_space else start
        iso_end = cartesian_to_isometric(coordinate=end) if game_space else end
        top_left_x = min(iso_start[0], iso_end[0])
        top_left_y = min(iso_start[1], iso_end[1])
        screen_scale = Screen.get_screen_scale()
        min_width = abs(iso_end[0] - iso_start[0]) * screen_scale + width
        min_height = abs(iso_end[1] - iso_start[1]) * screen_scale + width
        surface = pygame.Surface((min_width, min_height), pygame.SRCALPHA)
        adjusted_start_pos = ((iso_start[0] - top_left_x) * screen_scale, (iso_start[1] - top_left_y) * screen_scale)
        adjusted_end_pos = ((iso_end[0] - top_left_x) * screen_scale, (iso_end[1] - top_left_y) * screen_scale)
        pygame.draw.line(surface, color.color(), adjusted_start_pos, adjusted_end_pos, width)
        identifier = SurfaceIdentifier(
            identifier="debug_line" + "_" + str(color) + "_" + str(iso_start) + "-" + str(iso_end))
        draw_position = min(iso_start[0], iso_end[0]), min(iso_start[1], iso_end[1])
        draw_position = isometric_to_cartesian(coordinate=draw_position) if game_space else draw_position
        self.draw_surface(surface=surface,
                          identifier=identifier,
                          position=draw_position,
                          game_space=game_space,
                          anchor=DrawAnchor.TOP_LEFT,
                          priority=priority)

    def dequeue(self, sort_by_coordinate: bool):
        screen_size = Screen.get_current_resolution()
        screen_scale = Screen.get_screen_scale()
        iso_camera = Camera.get_position()
        if sort_by_coordinate:
            while not self.__z_index_queue.is_empty():
                elements = self.__z_index_queue.dequeue()
                for element in elements:
                    element.draw(iso_camera=iso_camera, screen_scale=screen_scale, screen_size=screen_size)
        else:
            while not self.__queue.is_empty():
                element = self.__queue.dequeue()
                element.draw(iso_camera=iso_camera, screen_scale=screen_scale, screen_size=screen_size)
        self.__queue.reset()
        self.__z_index_queue.reset()
