from typing import cast

from pymunk import Vec2d

from logic.core.db_service import DBService
from logic.core.isometry import cartesian_to_isometric, isometric_to_cartesian
from logic.core.screen import Screen


class Camera:
    __camera_position: tuple[float, float] | None = None
    is_enabled = True

    __available_box_presets = [
        (0, 0),
        (0.3, 0.3)
    ]

    __default_box_preset = (0.3, 0.3) #30% of the screen width/height
    __current_box_preset = None
    __box_preset_data_path = 'resources/game_data/box_preset_data'

    @staticmethod
    def initialize():
        try:
            box_preset = cast(tuple[int, int], DBService.select_data("box_preset", Camera.__box_preset_data_path))
            Camera.__current_box_preset = box_preset
        except KeyError:
            Camera.__current_box_preset = Camera.__default_box_preset

    @staticmethod
    def get_available_box_presets():
        return Camera.__available_box_presets

    @staticmethod
    def set_box_preset(preset: tuple[int, int]):
        if preset in Camera.__available_box_presets:
            Camera.__current_box_preset = preset
            DBService.insert_data("box_preset", preset, Camera.__box_preset_data_path)
        else:
            raise ValueError(f"Preset {preset} is not available in the predefined list.")

    @staticmethod
    def get_position() -> tuple[float, float]:
        # Returns camera position, in isometric space.
        if Camera.is_enabled and Camera.__camera_position is not None:
            return Camera.__camera_position
        else:
            return 0, 0

    @staticmethod
    def set_follow_position(position: Vec2d):
        # Get screen resolution and scale
        screen_width, screen_height = Screen.get_current_resolution()
        scale = Screen.get_screen_scale()
        screen_width /= scale
        screen_height /= scale

        # Calculate the size of the bounding box
        box_width = screen_width * Camera.__current_box_preset[0]
        box_height = screen_height * Camera.__current_box_preset[1]

        # Calculate the bounding box coordinates (centered on the screen)
        box_left = (screen_width - box_width) / 2
        box_right = box_left + box_width
        box_top = (screen_height - box_height) / 2
        box_bottom = box_top + box_height

        # Initialize camera position if not set
        if Camera.__camera_position is None:
            Camera.__camera_position = cartesian_to_isometric(coordinate=(position.x - screen_width / 2, position.y - screen_height / 2))

        # Convert the player's position and camera position to isometric space
        player_iso_position = cartesian_to_isometric(coordinate=(position.x, position.y))
        camera_iso_position_x, camera_iso_position_y = Camera.__camera_position

        # Calculate player's position relative to the camera in isometric space
        player_screen_x = player_iso_position[0] - camera_iso_position_x
        player_screen_y = player_iso_position[1] - camera_iso_position_y

        # Adjust the camera if the player is outside the bounding box
        camera_dx = 0
        camera_dy = 0

        # Horizontal movement (left-right)
        if player_screen_x < box_left:  # Player is outside to the left of the box
            camera_dx = player_screen_x - box_left
        elif player_screen_x > box_right:  # Player is outside to the right of the box
            camera_dx = player_screen_x - box_right

        # Vertical movement (up-down)
        if player_screen_y < box_top:  # Player is outside above the box
            camera_dy = player_screen_y - box_top
        elif player_screen_y > box_bottom:  # Player is outside below the box
            camera_dy = player_screen_y - box_bottom

        # Update the camera's position by the calculated offsets
        camera_iso_position_x += camera_dx
        camera_iso_position_y += camera_dy

        # Save the updated camera position as Isometric coordinates
        Camera.__camera_position = (camera_iso_position_x, camera_iso_position_y)
