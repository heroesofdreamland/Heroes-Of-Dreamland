from pymunk import Vec2d
from logic.core.animated_object import AnimatedObject
from logic.core.animation import Animation
from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle import Lifecycle
from logic.core.lifecycle_group import LifecycleGroup
from logic.entities.units.models.animation_type import AnimationType


class LevelUpObject(Lifecycle):
    def __init__(self,
                 position: Vec2d,
                 offset: tuple[float, float],
                 group: LifecycleGroup,
                 animation_path: str = 'resources/used_resources/effects/level_up/level_up2',
                 animation_frames_count: int = 24,
                 animation_scale: float = 1):
        self.position = position
        self.animated_object = AnimatedObject(
        {
            AnimationType.LEVEL_UP: Animation(path=animation_path,
                                              count=animation_frames_count,
                                              duration=0.5,
                                              repeat=False),
        },
            scale=animation_scale,
            offset=offset
        )
        super().__init__(group)

    def update(self):
        self.animated_object.configure_animation(AnimationType.LEVEL_UP)

    def render(self, queue: DrawQueue):
        self.animated_object.position = self.position
        queue.draw(group=self.group, animated_object=self.animated_object, game_space=True)
        if self.animated_object.is_animation_completed():
            self.is_alive = False
