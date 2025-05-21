from logic.core.animation import Animation
from logic.entities.units.models.animation_type import AnimationType
from logic.entities.units.models.animation_model import AnimationModel


class SkeletonThrasherAnimationModel(AnimationModel):
    def __init__(self, attack_animation_duration: float = 0):
        path = 'resources/used_resources/units/undeads/tier4/skeleton_thrasher/'
        animations = {
            AnimationType.IDLE: Animation(path=path + AnimationType.IDLE.value,
                                          count=14,
                                          duration=0.5,
                                          repeat=True),
            AnimationType.DEATH: Animation(path=path + AnimationType.DEATH.value,
                                           count=10,
                                           duration=0.5,
                                           repeat=False),
            AnimationType.RUN: Animation(path=path + AnimationType.RUN.value,
                                         count=8,
                                         duration=0.5,
                                         repeat=True),
            AnimationType.ATTACK: Animation(path=path + AnimationType.ATTACK.value,
                                            count=12,
                                            duration=attack_animation_duration,
                                            repeat=True),
        }
        super().__init__(animations=animations)
