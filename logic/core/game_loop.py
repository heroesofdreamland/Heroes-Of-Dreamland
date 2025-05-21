import pygame
from pymunk import Space
from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle import Lifecycle
from logic.core.lifecycle_group import LifecycleGroupIndex
from logic.core.opengl import OpenGL


class GameLoop:
    max_fps = 120
    physics_substeps = 5

    def __init__(self):
        self.__controllers: dict[LifecycleGroupIndex, list[Lifecycle]] = {}
        self.__draw_queue = DrawQueue()
        self.is_running = False
        self.current_fps = GameLoop.max_fps

    def start(self, spaces: list[Space]):
        self.is_running = True
        clock = pygame.time.Clock()
        while self.is_running:
            diff = clock.tick(self.max_fps) * 0.001
            self.__execute_input()
            for space in spaces:
                self.__execute_update(space, diff)
            self.__execute_render()
            self.current_fps = int(clock.get_fps())

        pygame.quit()

    def stop(self):
        self.is_running = False

    def register(self, controller: Lifecycle):
        if controller.group.index not in self.__controllers:
            self.__controllers[controller.group.index] = []
        self.__controllers[controller.group.index].append(controller)
        self.__controllers = dict(sorted(self.__controllers.items(), key=lambda el: el[0].index))

    def unregister(self, controller: Lifecycle):
        self.__controllers[controller.group.index].remove(controller)

    def __execute_input(self):
        events = pygame.event.get()
        for group_index in self.__controllers:
            for controller in self.__controllers[group_index]:
                if controller.group.is_input_enabled:
                    controller.process_input(events)

    def __execute_update(self, space, diff):
        for group_index in self.__controllers:
            for controller in self.__controllers[group_index]:
                controller.pre_update()
                if controller.group.is_update_enabled:
                    controller.update()
        for _ in range(GameLoop.physics_substeps):
            space.step(diff / GameLoop.physics_substeps)
        for group_index in self.__controllers:
            for controller in self.__controllers[group_index]:
                controller.post_update()

    def __execute_render(self):
        OpenGL.clear()
        for group_index in self.__controllers:
            for controller in self.__controllers[group_index]:
                if controller.group.is_render_enabled:
                    controller.render(queue=self.__draw_queue)
            self.__draw_queue.dequeue(sort_by_coordinate=group_index.sort_by_coordinate)
        pygame.display.flip()
