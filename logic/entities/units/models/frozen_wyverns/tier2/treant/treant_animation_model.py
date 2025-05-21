from logic.core.animation import Animation
from logic.entities.units.models.animation_type import AnimationType
from logic.entities.units.models.animation_model import AnimationModel


class TreantAnimationModel(AnimationModel):
    def __init__(self, attack_animation_duration: float = 0):
        path = 'resources/used_resources/units/frozen_wyverns/tier4/treant/'
        animations = {
            AnimationType.IDLE: Animation(path=path + AnimationType.IDLE.value,
                                          count=16,
                                          duration=0.5,
                                          repeat=True),
            AnimationType.DEATH: Animation(path=path + AnimationType.DEATH.value,
                                           count=9,
                                           duration=0.5,
                                           repeat=False),
            AnimationType.RUN: Animation(path=path + AnimationType.RUN.value,
                                         count=8,
                                         duration=0.5,
                                         repeat=True),
            AnimationType.ATTACK: Animation(path=path + AnimationType.ATTACK.value,
                                            count=27,
                                            duration=attack_animation_duration,
                                            repeat=True),
        }
        super().__init__(animations=animations)
