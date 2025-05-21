from logic.controller.control_hints_contoller import ControlHintsController
from logic.controller.keyboard_settings_controller import KeyboardSettingsController
from logic.core.scene import Scene
from logic.environment.environment import Groups
from logic.level_design.scenes.scenes import Scenes


class KeyboardSettingsScene(Scene):
    def __init__(self):
        super().__init__(
            name=Scenes.KEYBOARD_SETTINGS.value,
            controllers=[
                KeyboardSettingsController(group=Groups.gui),
                ControlHintsController(group=Groups.menu)
            ]
        )
