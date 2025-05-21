from logic.controller.resolution_settings_controller import ResolutionSettingsController
from logic.core.scene import Scene
from logic.environment.environment import Groups
from logic.level_design.scenes.scenes import Scenes


class ResolutionSettingsScene(Scene):
    def __init__(self):
        super().__init__(
            name=Scenes.RESOLUTION_SETTINGS.value,
            controllers=[
                ResolutionSettingsController(group=Groups.gui)
            ]
        )
