from pymunk import Circle, Body, Vec2d
from logic.core.animated_object import AnimatedObject
from logic.core.animation import Animation
from logic.core.lifecycle_group import LifecycleGroup
from logic.entities.effects.negative.frost_effect import FrostEffect
from logic.entities.projectiles.projectile import Projectile
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.data.damage_data import DamageData
from logic.entities.units.models.animation_type import AnimationType


class Arrow(Projectile):
    def __init__(self,
                 x: float,
                 y: float,
                 group: LifecycleGroup,
                 enemies_provider: EnemiesProvider):
        path = 'resources/used_resources/projectiles/arrow/'
        animations = {
            AnimationType.FLIES: Animation(path=path + AnimationType.FLIES.value,
                                           count=6,
                                           duration=0.5,
                                           repeat=True),
        }
        shape = Circle(body=Body(body_type=Body.KINEMATIC), radius=5)
        shape.sensor = True
        super().__init__(position=Vec2d(x, y),
                         shape=shape,
                         group=group,
                         animated_object=AnimatedObject(animations=animations, scale=0.8, offset=(0, -1)),
                         speed=500,
                         damage_data=DamageData(damage=1, effects=[FrostEffect(duration=6, amount=0.2)]),
                         enemies_provider=enemies_provider)
