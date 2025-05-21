from logic.controller.settings_menu_controller import SettingsMenuController
from logic.core.scene import Scene
from logic.environment.environment import Groups
from logic.level_design.scenes.scenes import Scenes


class SettingsScene(Scene):
    def __init__(self):
        super().__init__(
            name=Scenes.HERO_SELECT_MENU.value,
            controllers=[
                SettingsMenuController(group=Groups.gui)
            ]
        )
