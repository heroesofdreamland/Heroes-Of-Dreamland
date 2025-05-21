from logic.controller.debug_settings_controller import DebugSettingsController
from logic.core.scene import Scene
from logic.environment.environment import Groups
from logic.level_design.scenes.scenes import Scenes


class DebugSettingsScene(Scene):
    def __init__(self):
        super().__init__(
            name=Scenes.DEBUG_SETTINGS.value,
            controllers=[
                DebugSettingsController(group=Groups.gui)
            ]
        )