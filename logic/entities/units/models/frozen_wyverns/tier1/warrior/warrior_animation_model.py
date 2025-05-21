from logic.core.animation import Animation
from logic.entities.units.models.animation_type import AnimationType
from logic.entities.units.models.animation_model import AnimationModel


class WarriorAnimationModel(AnimationModel):
    def __init__(self, attack_animation_duration: float = 0, is_summoned: bool = False):
        path = 'resources/used_resources/units/frozen_wyverns/tier1/sinergy/' if is_summoned else 'resources/used_resources/units/frozen_wyverns/tier1/sinergy/'
        animations = {
            AnimationType.IDLE: Animation(path=path + AnimationType.IDLE.value,
                                          count=16,
                                          duration=0.5,
                                          repeat=True),
            AnimationType.DEATH: Animation(path=path + AnimationType.DEATH.value,
                                           count=15,
                                           duration=0.8,
                                           repeat=False),
            # AnimationType.STUN: Animation(path=path + AnimationType.STUN.value,
            #                                count=15,
            #                                duration=0.5,
            #                                repeat=True),
            AnimationType.RUN: Animation(path=path + AnimationType.RUN.value,
                                         count=8,
                                         duration=0.5,
                                         repeat=True),
            AnimationType.ATTACK: Animation(path=path + AnimationType.ATTACK.value,
                                            count=19,
                                            duration=attack_animation_duration,
                                            repeat=True),
            AnimationType.RESURRECTION: Animation(path=path + AnimationType.RESURRECTION.value,
                                                  count=15,
                                                  duration=0.5,
                                                  repeat=False),
            AnimationType.DEATH_WITH_RESURRECTION: Animation(path=path + AnimationType.DEATH_WITH_RESURRECTION.value,
                                                  count=15,
                                                  duration=0.5,
                                                  repeat=False)
        }
        super().__init__(animations=animations)
