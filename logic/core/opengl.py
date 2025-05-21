import warnings

import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.raw.GLU import gluOrtho2D
from pygame import Surface
from logic.core.resource_cache import cached_image


class SurfaceIdentifier:
    def __init__(self,
                 identifier: str,
                 value: str|None = None):
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        result = self.__class__.__name__ + "(identifier=" + self.identifier
        if self.value is not None:
            return result + ", value=" + self.value + ")"
        else:
            return result + ")"


class Texture:
    def __init__(self,
                 texture_id,
                 size: tuple[float, float]):
        self.texture_id = texture_id
        self.size = size


class TextureCache:
    images: dict[tuple[str, float, bool], Texture] = {}
    temporary_textures: list[int] = []
    identified_textures: dict[str, tuple[Texture, str | None]] = {}

    @staticmethod
    def clear():
        TextureCache.images = {}
        TextureCache.temporary_textures = []
        TextureCache.identified_textures = {}


class OpenGL:
    _glEnable = glEnable
    _glBlendFunc = glBlendFunc
    _glViewport = glViewport
    _glMatrixMode = glMatrixMode
    _glLoadIdentity = glLoadIdentity
    _glClear = glClear
    _glGetIntegerv = glGetIntegerv
    _glBindTexture = glBindTexture
    _glEnableClientState = glEnableClientState
    _glVertexPointer = glVertexPointer
    _glTexCoordPointer = glTexCoordPointer
    _glDrawElements = glDrawElements
    _glBegin = glBegin
    _glEnd = glEnd
    _glTexCoord2f = glTexCoord2f
    _glVertex2f = glVertex2f
    _glPushMatrix = glPushMatrix
    _glPopMatrix = glPopMatrix
    _gluOrtho2D = gluOrtho2D
    _glRotatef = glRotatef
    _glTranslatef = glTranslatef
    _glClearColor = glClearColor
    _glTexParameteri = glTexParameteri
    _glTexImage2D = glTexImage2D
    _glDisableClientState = glDisableClientState
    _glDeleteTextures = glDeleteTextures

    # Preallocate arrays with a size large enough to handle typical batch sizes
    _MAX_BATCH_SIZE = 1000  # Adjust this value based on typical batch size
    _opengl_positions = np.empty((_MAX_BATCH_SIZE * 8,), dtype=np.float32)
    _texture_coords = np.empty((_MAX_BATCH_SIZE * 8,), dtype=np.float32)
    _indices = np.empty((_MAX_BATCH_SIZE * 6,), dtype=np.uint32)

    # Cache last texture id to reuse if needed
    _last_texture_id: int | None = None

    @staticmethod
    def configure(screen_size: tuple[int, int]):
        TextureCache.clear()
        OpenGL._glEnable(GL_TEXTURE_2D)
        OpenGL._glEnable(GL_BLEND)
        OpenGL._glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        screen_width, screen_height = screen_size
        OpenGL._glViewport(0, 0, screen_width, screen_height)
        OpenGL._glMatrixMode(GL_PROJECTION)
        OpenGL._glLoadIdentity()
        OpenGL._gluOrtho2D(0, screen_width, 0, screen_height)
        OpenGL._glMatrixMode(GL_MODELVIEW)
        OpenGL._glLoadIdentity()

    @staticmethod
    def clear():
        OpenGL._glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if TextureCache.temporary_textures:
            OpenGL._glDeleteTextures(len(TextureCache.temporary_textures), TextureCache.temporary_textures)
            TextureCache.temporary_textures = []
            warnings.warn("queue.draw_surface(...) without identifier is detected. Provide an identifier to avoid performance issues")

    @staticmethod
    def get_viewport_size():
        # This returns the viewport as (x, y, width, height)
        viewport = OpenGL._glGetIntegerv(GL_VIEWPORT)
        return viewport[2], viewport[3]

    @staticmethod
    def __is_visible(bounding_box: tuple[float, float, float, float], screen_size: tuple[int, int]):
        min_x, min_y, width, height = bounding_box
        screen_width, screen_height = screen_size

        # Early exit for visibility check
        return not (min_x > screen_width or min_y > screen_height or min_x + width < 0 or min_y + height < 0)

    @staticmethod
    def draw(texture: Texture,
             position: tuple[float, float],
             angle: float,
             screen_size: tuple[int, int]):
        x, y = position
        texture_w, texture_h = texture.size
        _, screen_h = screen_size
        if OpenGL.__is_visible(bounding_box=(x, y, texture_w, texture_h), screen_size=screen_size):
            # Invert y coordinate for OpenGL
            opengl_rect = x, screen_h - y - texture_h, texture_w, texture_h
            OpenGL.__draw_texture(texture.texture_id, [opengl_rect], angle)

    @staticmethod
    def draw_batch(texture: Texture,
                   positions: list[tuple[float, float]],
                   angle: float,
                   screen_size: tuple[int, int]):
        texture_w, texture_h = texture.size
        _, screen_h = screen_size
        position_index = 0
        texture_index = 0
        index_index = 0
        index_count = 0

        for position in positions:
            x, y = position
            if OpenGL.__is_visible(bounding_box=(x, y, texture_w, texture_h), screen_size=screen_size):
                # Invert y coordinate for OpenGL
                y = screen_h - y - texture_h
                # Define vertices in OpenGL coordinates and add to preallocated array
                OpenGL._opengl_positions[position_index:position_index + 8] = [
                    x, y,
                    x + texture_w, y,
                    x + texture_w, y + texture_h,
                    x, y + texture_h
                ]
                position_index += 8

                # Add texture coordinates (same for every quad)
                OpenGL._texture_coords[texture_index:texture_index + 8] = [
                    0.0, 0.0,
                    1.0, 0.0,
                    1.0, 1.0,
                    0.0, 1.0
                ]
                texture_index += 8

                # Add indices for drawing the quad (2 triangles per quad)
                OpenGL._indices[index_index:index_index + 6] = [
                    index_count, index_count + 1, index_count + 2,
                    index_count, index_count + 2, index_count + 3
                ]
                index_index += 6
                index_count += 4

        if position_index > 0:
            # Use only the filled part of the arrays
            opengl_positions = OpenGL._opengl_positions[:position_index]
            texture_coords = OpenGL._texture_coords[:texture_index]
            indices = OpenGL._indices[:index_index]
            # Draw the batch using the optimized method
            OpenGL.__draw_textures(texture.texture_id, opengl_positions, texture_coords, indices, angle)

    @staticmethod
    def __draw_textures(texture_id: int,
                        vertices: np.ndarray,
                        tex_coords: np.ndarray,
                        indices: np.ndarray,
                        angle: float):
        if texture_id != OpenGL._last_texture_id:
            OpenGL._glBindTexture(GL_TEXTURE_2D, texture_id)
            OpenGL._last_texture_id = texture_id
        OpenGL._glEnableClientState(GL_VERTEX_ARRAY)
        OpenGL._glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        OpenGL._glVertexPointer(2, GL_FLOAT, 0, vertices)
        OpenGL._glTexCoordPointer(2, GL_FLOAT, 0, tex_coords)
        if angle != 0:
            OpenGL._glPushMatrix()
            OpenGL._glRotatef(angle, 0.0, 0.0, 1.0)
        OpenGL._glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, indices)
        if angle != 0:
            OpenGL._glPopMatrix()
        OpenGL._glDisableClientState(GL_VERTEX_ARRAY)
        OpenGL._glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    @staticmethod
    def __draw_texture(texture_id: int,
                       opengl_rects: list[tuple[float, float, float, float]],
                       angle: float):
        if texture_id != OpenGL._last_texture_id:
            OpenGL._glBindTexture(GL_TEXTURE_2D, texture_id)
            OpenGL._last_texture_id = texture_id
        for opengl_rect in opengl_rects:
            x_opengl, y_opengl, w_opengl, h_opengl = opengl_rect
            OpenGL._glPushMatrix()
            if angle != 0:
                center_x = x_opengl + w_opengl / 2.0
                center_y = y_opengl + h_opengl / 2.0
                OpenGL._glTranslatef(center_x, center_y, 0.0)
                OpenGL._glRotatef(angle, 0.0, 0.0, 1.0)
                OpenGL._glTranslatef(-center_x, -center_y, 0.0)
            OpenGL._glBegin(GL_QUADS)
            OpenGL._glTexCoord2f(0.0, 0.0)
            OpenGL._glVertex2f(x_opengl, y_opengl)
            OpenGL._glTexCoord2f(1.0, 0.0)
            OpenGL._glVertex2f(x_opengl + w_opengl, y_opengl)
            OpenGL._glTexCoord2f(1.0, 1.0)
            OpenGL._glVertex2f(x_opengl + w_opengl, y_opengl + h_opengl)
            OpenGL._glTexCoord2f(0.0, 1.0)
            OpenGL._glVertex2f(x_opengl, y_opengl + h_opengl)
            OpenGL._glEnd()
            OpenGL._glPopMatrix()

    @staticmethod
    def surface_texture(surface: Surface, identifier: SurfaceIdentifier|None) -> Texture:
        if identifier is None:
            # If None is provided, temporary texture cache is used. New texture is created on every call (should be avoided)
            texture = OpenGL.__create_texture(surface)
            TextureCache.temporary_textures.append(texture.texture_id)
            return texture
        else:
            # If SurfaceIdentifier is provided, we use following cache logic for caching textures:
            #   - The same object should have the same (but unique) identifier, but may have different value. Value
            #   represents the state of the rendered object (for example, dynamic text or size of the resizeable
            #   rectangle)
            #   - If there is a cached object with provided identifier, it should have the same value to be fully
            #   reused. If value is different, previous texture with old value is removed from cache. New texture will
            #   be generated and stored instead.
            #
            # This SurfaceIdentifier caching logic is needed to cover the cases where there is a "static surface" but it
            # may change with time. For example, if there is a timer text rendered on the screen. Every second, text
            # changes - identifier of this SurfaceIdentifier remains the same, but value changes. It helps to remove the
            # old texture from the cache to avoid memory issues.
            if identifier.identifier in TextureCache.identified_textures:
                # If there is an already cached texture with identifier, check if it's cached with the same value
                cached_texture, cached_value = TextureCache.identified_textures[identifier.identifier]
                if cached_value == identifier.value:
                    # If the cached texture has the same identifier and value, return cached value
                    return cached_texture
                else:
                    # If the cached texture has the same identifier but another value, create new texture and delete old cached value
                    # print('Texture invalidated: ', identifier.identifier, identifier.value)
                    texture = OpenGL.__create_texture(surface)
                    TextureCache.identified_textures[identifier.identifier] = texture, identifier.value
                    OpenGL._glDeleteTextures(1, [cached_texture.texture_id])
                    return texture
            else:
                # If there is no cached textures with the same identifier, create new texture and cache it
                texture = OpenGL.__create_texture(surface)
                TextureCache.identified_textures[identifier.identifier] = texture, identifier.value
                return texture

    @staticmethod
    def image_texture(path: str, scale: float, mirrored: bool) -> Texture:
        if (path, scale, mirrored) in TextureCache.images:
            return TextureCache.images[(path, scale, mirrored)]
        image = cached_image(path=path, mirrored=mirrored, scale=scale)
        texture = OpenGL.__create_texture(image)
        TextureCache.images[(path, scale, mirrored)] = texture
        return texture

    @staticmethod
    def __create_texture(surface: Surface) -> Texture:
        texture_data = pygame.image.tostring(surface, "RGBA", True)
        width, height = surface.get_size()

        texture_id = glGenTextures(1)
        if texture_id != OpenGL._last_texture_id:
            OpenGL._glBindTexture(GL_TEXTURE_2D, texture_id)
            OpenGL._last_texture_id = texture_id
        OpenGL._glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        OpenGL._glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        OpenGL._glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        OpenGL._glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        OpenGL._glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        texture = Texture(texture_id=texture_id, size=(width, height))
        return texture
