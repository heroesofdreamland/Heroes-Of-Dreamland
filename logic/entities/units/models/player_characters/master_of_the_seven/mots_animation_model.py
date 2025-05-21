from logic.core.animation import Animation
from logic.entities.units.models.animation_type import AnimationType
from logic.entities.units.models.animation_model import AnimationModel


class MasterOfTheSevenAnimationModel(AnimationModel):
    def __init__(self, attack_animation_duration: float = 0):
        path = 'resources/used_resources/units/player_characters/master_of_the_seven/'
        animations = {
            AnimationType.IDLE: Animation(path=path + AnimationType.IDLE.value,
                                          count=14,
                                          duration=0.5,
                                          repeat=True),
            AnimationType.DEATH: Animation(path=path + AnimationType.DEATH.value,
                                           count=22,
                                           duration=0.5,
                                           repeat=False),
            AnimationType.RUN: Animation(path=path + AnimationType.RUN.value,
                                         count=8,
                                         duration=0.5,
                                         repeat=True),
            AnimationType.ATTACK: Animation(path=path + AnimationType.ATTACK.value,
                                            count=17,
                                            duration=attack_animation_duration,
                                            repeat=True),
            AnimationType.BREATHING: Animation(path=path + AnimationType.BREATHING.value,
                                               count=14,
                                               duration=0.5,
                                               repeat=True)
        }
        super().__init__(animations=animations)
