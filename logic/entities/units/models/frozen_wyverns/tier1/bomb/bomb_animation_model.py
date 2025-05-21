from logic.core.animation import Animation
from logic.entities.units.models.animation_type import AnimationType
from logic.entities.units.models.animation_model import AnimationModel


class BombAnimationModel(AnimationModel):
    def __init__(self):
        path = 'resources/used_resources/units/chaos_incarnatech/tier1/bomb/bomb/'
        animations = {
            AnimationType.IDLE: Animation(path=path + AnimationType.IDLE.value,
                                          count=10,
                                          duration=1,
                                          repeat=True),
            AnimationType.DEATH: Animation(path=path + AnimationType.DEATH.value,
                                           count=27,
                                           duration=1,
                                           repeat=False),
            AnimationType.RUN: Animation(path=path + AnimationType.RUN.value,
                                         count=10,
                                         duration=1,
                                         repeat=True)
        }
        super().__init__(animations=animations)
