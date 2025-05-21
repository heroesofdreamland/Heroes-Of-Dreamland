from logic.core.animation import Animation
from logic.entities.units.models.animation_type import AnimationType
from logic.entities.units.models.animation_model import AnimationModel


class WyvernsMageAnimationModel(AnimationModel):
    def __init__(self, attack_animation_duration: float = 0, attack_cooldown: float = 0):
        path = 'resources/used_resources/units/frozen_wyverns/tier1/wyverns_mage/'
        animations = {
            AnimationType.IDLE: Animation(path=path + AnimationType.IDLE.value,
                                          count=18,
                                          duration=2.5,
                                          repeat=True),
            AnimationType.BREATHING: Animation(path=path + AnimationType.BREATHING.value,
                                               count=14,
                                               duration=attack_cooldown,
                                               repeat=False),
            # AnimationType.STUN: Animation(path=path + AnimationType.STUN.value,
            #                               count=14,
            #                               duration=0.5,
            #                               repeat=True),
            AnimationType.DEATH: Animation(path=path + AnimationType.DEATH.value,
                                           count=21,
                                           duration=0.5,
                                           repeat=False),
            # AnimationType.DEATH_WITH_RESURRECTION: Animation(path=path + AnimationType.DEATH_WITH_RESURRECTION.value,
            #                                count=23,
            #                                duration=0.5,
            #                                repeat=False),
            # AnimationType.RESURRECTION: Animation(path=path + AnimationType.RESURRECTION.value,
            #                                 count=23,
            #                                 duration=0.5,
            #                                 repeat=False),
            AnimationType.RUN: Animation(path=path + AnimationType.RUN.value,
                                         count=8,
                                         duration=0.5,
                                         repeat=True),
            AnimationType.ATTACK: Animation(path=path + AnimationType.ATTACK.value,
                                            count=20,
                                            duration=attack_animation_duration,
                                            repeat=True)
        }
        super().__init__(animations=animations)
