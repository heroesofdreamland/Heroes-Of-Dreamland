from logic.controller.camera_settings_controller import CameraSettingsController
from logic.core.scene import Scene
from logic.environment.environment import Groups
from logic.level_design.scenes.scenes import Scenes


class CameraSettingsScene(Scene):
    def __init__(self):
        super().__init__(
            name=Scenes.CAMERA_SETTINGS.value,
            controllers=[
                CameraSettingsController(group=Groups.gui)
            ]
        )
