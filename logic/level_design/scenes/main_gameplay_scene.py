from logic.controller.background_controller import BackgroundController
from logic.controller.control_hints_contoller import ControlHintsController
from logic.controller.gui_controller import GuiController
from logic.controller.inventory_controller import InventoryController
from logic.controller.map_controller import MapRootController, MapTransitionController
from logic.controller.guild_grandmaster_controller import GuildGrandmasterController
from logic.controller.objects_controller import ObjectsController
from logic.controller.pause_menu_controller import PauseMenuController
from logic.controller.player_controller import PlayerController
from logic.controller.orders_controller import OrdersController
from logic.controller.store_controller import StoreController
from logic.core.scene import Scene
from logic.environment.environment import Groups
from logic.level_design.scenes.scenes import Scenes


class MainGameplayScene(Scene):
    def __init__(self):
        super().__init__(
            name=Scenes.MAIN_GAMEPLAY.value,
            controllers=[
                BackgroundController(group=Groups.background),
                OrdersController(group=Groups.background),
                GuildGrandmasterController(group=Groups.background),
                MapRootController(group=Groups.level),
                PlayerController(group=Groups.player),
                ObjectsController(group=Groups.objects),
                GuiController(group=Groups.gui),
                MapTransitionController(group=Groups.transition),
                StoreController(group=Groups.menu),
                ControlHintsController(group=Groups.menu),
                InventoryController(group=Groups.menu),
                ControlHintsController(group=Groups.menu),
                PauseMenuController(group=Groups.menu),
            ]
        )
