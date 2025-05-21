from logic.core.draw_queue import DrawQueue, DrawAnchor
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.lifecycle import Lifecycle
from logic.core.game_loop import GameLoop
from logic.core.render.components.text import Text
from logic.ui.colors import Colors
from logic.settings.debug_settings import DebugSettings
from logic.ui.fonts import Fonts


class DebugController(Lifecycle):
    def __init__(self, game_loop: GameLoop, group: LifecycleGroup):
        self.game_loop = game_loop
        super().__init__(group=group)

    def render(self, queue: DrawQueue):
        if DebugSettings.debug_settings['show_fps']:
            Text(
                text="FPS: " + str(self.game_loop.current_fps),
                font=Fonts.blackcraft(size=20),
                color=Colors.WHITE
            ).draw(
                position=(16, 16),
                queue=queue,
                anchor=DrawAnchor.TOP_LEFT,
                game_space=False
            )
