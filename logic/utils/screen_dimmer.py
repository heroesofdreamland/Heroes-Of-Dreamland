from logic.core.draw_queue import DrawQueue, DrawAnchor
from logic.core.render.color import Color
from logic.core.render.components.rect import Rect
from logic.core.screen import Screen
from logic.ui.colors import Colors


class ScreenDimmer:
    def __init__(self, color: Color = Colors.SEMITRANSPARENT):
        self.__color = color

    def render(self, queue: DrawQueue):
        screen_width, screen_height = Screen.get_current_resolution()
        Rect(
            size=(screen_width, screen_height),
            color=self.__color
        ).draw(
            position=(0, 0),
            queue=queue,
            anchor=DrawAnchor.TOP_LEFT,
            game_space=False
        )
