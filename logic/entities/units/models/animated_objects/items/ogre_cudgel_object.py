from pymunk import Vec2d
from logic.core.animated_object import AnimatedObject
from logic.core.animation import Animation
from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle import Lifecycle
from logic.core.lifecycle_group import LifecycleGroup
from logic.environment.environment import Environment
from logic.entities.units.data.unit_side import UnitSide
from logic.entities.units.models.animation_type import AnimationType


class OgreCudgelObject(Lifecycle):
    def __init__(self,
                 position: Vec2d,
                 offset: tuple[float, float],
                 side: UnitSide,
                 group: LifecycleGroup,
                 animation_path: str = 'resources/used_resources/units/undeads/tier1/skeleton_warrior/attack',
                 animation_frames_count: int = 12,
                 animation_scale: float = 2.5):
        self.__position = position
        self.animated_object = AnimatedObject(
        {
            AnimationType.CAST: Animation(path=animation_path,
                                          count=animation_frames_count,
                                          duration=0.5,
                                          repeat=False),
        },
            scale=animation_scale,
            offset=offset
        )
        self.animated_object.mirrored = side == UnitSide.LEFT
        super().__init__(group)

    def update(self):
        self.animated_object.configure_animation(AnimationType.CAST)
        if self.animated_object.is_animation_completed():
            Environment.map.objects.remove(self)

    def render(self, queue: DrawQueue):
        self.animated_object.position = self.__position
        queue.draw(group=self.group, animated_object=self.animated_object, game_space=True)
