from pymunk import Vec2d
from logic.core.animated_object import AnimatedObject
from logic.core.animation import Animation
from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle import Lifecycle
from logic.core.lifecycle_group import LifecycleGroup
from logic.entities.units.models.animation_type import AnimationType


class DeathObject(Lifecycle):
    def __init__(self,
                 position: Vec2d,
                 offset: tuple[float, float],
                 group: LifecycleGroup,
                 animation_path: str = 'resources/used_resources/animated_objects/undeads/death',
                 animation_frames_count: int = 14,
                 animation_scale: float = 0.5):
        self.__position = position
        self.animated_object = AnimatedObject(
            animations = {
                AnimationType.DEATH: Animation(path=animation_path,
                                               count=animation_frames_count,
                                               duration=0.5,
                                               repeat=False),
            },
            scale = animation_scale,
            offset = offset
        )
        super().__init__(group)

    def update(self):
        self.animated_object.configure_animation(AnimationType.DEATH)
        if self.animated_object.is_animation_completed():
            self.is_alive = False

    def render(self, queue: DrawQueue):
        self.animated_object.position = self.__position
        queue.draw(group=self.group, animated_object=self.animated_object, game_space=True)
