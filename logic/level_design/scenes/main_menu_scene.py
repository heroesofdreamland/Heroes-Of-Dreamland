from logic.controller.main_menu_controller import MainMenuController
from logic.core.scene import Scene
from logic.environment.environment import Groups
from logic.level_design.scenes.scenes import Scenes


class MainMenuScene(Scene):
    def __init__(self):
        super().__init__(
            name=Scenes.MAIN_MENU.value,
            controllers=[
                MainMenuController(group=Groups.gui)
            ]
        )
