from logic.core.animation import Animation
from logic.entities.units.models.animation_type import AnimationType
from logic.entities.units.models.animation_model import AnimationModel


class TraderAnimationModel(AnimationModel):
    def __init__(self):
        path = 'resources/used_resources/units/traders/neutral_thescientist/'
        animations = {
            AnimationType.IDLE: Animation(path=path + AnimationType.BREATHING.value,
                                          count=14,
                                          duration=0.5,
                                          repeat=True),
        }
        super().__init__(animations=animations)
