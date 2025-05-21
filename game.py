from logic.controller.debug_controller import DebugController
from logic.controller.game_controller import GameController
from logic.core.camera import Camera
from logic.core.game_loop import GameLoop
from logic.core.scene import SceneManager
from logic.environment.environment import Environment, Spaces, Groups
from logic.events.event_manager import EventManager
from logic.level_design.scenes.camera_settings_scene import CameraSettingsScene
from logic.level_design.scenes.debug_settings_scene import DebugSettingsScene
from logic.level_design.scenes.hero_select_scene import HeroSelectScene
from logic.level_design.scenes.keyboard_settings_scene import KeyboardSettingsScene
from logic.level_design.scenes.main_gameplay_scene import MainGameplayScene
from logic.level_design.scenes.main_menu_scene import MainMenuScene
from logic.level_design.scenes.resolution_settings_scene import ResolutionSettingsScene
from logic.level_design.scenes.scenes import Scenes
from logic.level_design.scenes.settings_scene import SettingsScene
from logic.settings.key_settings import KeySettings
from logic.core.screen import Screen
from logic.settings.debug_settings import DebugSettings


def main():
    KeySettings.initialize()
    Screen.initialize()
    Camera.initialize()

    game_loop = GameLoop()
    Environment.scene_manager = SceneManager(loop=game_loop)
    Environment.event_manager = EventManager()
    game_controller = GameController(game_loop=game_loop,
                                     spaces=[Spaces.SHARED],
                                     group=Groups.background)
    game_loop.register(game_controller)

    debug_controller = DebugController(game_loop=game_loop, group=Groups.foreground)
    game_loop.register(debug_controller)

    Environment.scene_manager.register(scene_type=MainMenuScene, name=Scenes.MAIN_MENU.value)
    Environment.scene_manager.register(scene_type=SettingsScene, name=Scenes.SETTINGS.value)
    Environment.scene_manager.register(scene_type=ResolutionSettingsScene, name=Scenes.RESOLUTION_SETTINGS.value)
    Environment.scene_manager.register(scene_type=KeyboardSettingsScene, name=Scenes.KEYBOARD_SETTINGS.value)
    Environment.scene_manager.register(scene_type=CameraSettingsScene, name=Scenes.CAMERA_SETTINGS.value)
    Environment.scene_manager.register(scene_type=DebugSettingsScene, name=Scenes.DEBUG_SETTINGS.value)
    Environment.scene_manager.register(scene_type=HeroSelectScene, name=Scenes.HERO_SELECT_MENU.value)
    Environment.scene_manager.register(scene_type=MainGameplayScene, name=Scenes.MAIN_GAMEPLAY.value)
    Environment.scene_manager.activate(Scenes.MAIN_MENU.value)

    game_controller.start()


if DebugSettings.debug_settings['run_profiling']:
    import cProfile
    cProfile.run('main()', 'profile_data.prof')
    # Run in terminal:
    # snakeviz profile_data.prof
else:
    main()
