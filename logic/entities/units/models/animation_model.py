from logic.core.animated_object import AnimatedObject
from logic.core.animation import Animation
from logic.entities.units.models.animation_type import AnimationType


class AnimationModel:
    def __init__(self, animations: dict[AnimationType, Animation]):
        self.__animations = animations

    def build_animated_object(self, scale: float = 1, offset: tuple[float, float] = (0, 0)) -> AnimatedObject:
        return AnimatedObject(animations=self.__animations, scale=scale, offset=offset)
