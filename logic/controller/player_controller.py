from typing import MutableSequence

from logic.core.camera import Camera
from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.lifecycle import Lifecycle
from logic.environment.environment import Environment, Groups
from logic.utils.screen_dimmer import ScreenDimmer
from logic.entities.units.data.unit_life_state import UnitLifeState


# PlayerController responsibilities:
# - Wrapping the Environment.player to allow easy replacement without affecting the game loop
class PlayerController(Lifecycle):
    def __init__(self, group: LifecycleGroup):
        super().__init__(group=group)
        self.__screen_dimmer = ScreenDimmer()

    def process_input(self, events: MutableSequence):
        Environment.player.process_input(events)

    def pre_update(self):
        Environment.player.pre_update()

    def update(self):
        Environment.player.update()
        if Environment.player.life_state == UnitLifeState.DEATH:
            Groups.objects.set_input_enabled(is_enabled=False, reason='player_death')
            Groups.objects.set_update_enabled(is_enabled=False, reason='player_death')
            Groups.objects.set_render_enabled(is_enabled=False, reason='player_death')
            Groups.player.set_input_enabled(is_enabled=False, reason='player_death')
            Groups.level.set_update_enabled(is_enabled=False, reason='player_death')

    def post_update(self):
        Environment.player.post_update()
        Camera.set_follow_position(position=Environment.player.position)

    def render(self, queue: DrawQueue):
        if Environment.player.life_state == UnitLifeState.DEATH:
            self.__screen_dimmer.render(queue=queue)
        Environment.player.render(queue)
