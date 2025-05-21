from typing import MutableSequence

import pygame
from pymunk import Space
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.lifecycle import Lifecycle
from logic.core.game_loop import GameLoop
from logic.environment.environment import Environment


# GameController responsibilities:
# - Starting the pygame engine
# - Starting and stopping the game loop
# - Processing the common input
class GameController(Lifecycle):
    def __init__(self,
                 game_loop: GameLoop,
                 spaces: list[Space],
                 group: LifecycleGroup):
        self.game_loop = game_loop
        self.spaces = spaces
        pygame.init()
        super().__init__(group=group)

    def start(self):
        self.game_loop.start(self.spaces)

    def process_input(self, events: MutableSequence):
        for event in events:
            if event.type == pygame.QUIT:
                self.game_loop.stop()

    def post_update(self):
        Environment.event_manager.publish()
