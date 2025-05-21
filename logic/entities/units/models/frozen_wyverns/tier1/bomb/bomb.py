from pymunk import Vec2d, Circle, Body

from logic.entities.abilities.explosion_ability import ExplosionAbility
from logic.entities.abilities.move_with_closest_enemy_ability import MoveWithClosestEnemyAbility
from logic.entities.abilities.spawn_object_ability import SpawnObjectAbility
from logic.entities.abilities.status_bar_ability import StatusBarAbility
from logic.core.lifecycle_group import LifecycleGroup
from logic.entities.effects.negative.frost_effect import FrostEffect
from logic.entities.rewards.kill_reward import KillReward
from logic.entities.units.models.frozen_wyverns.tier1.bomb.bomb_animation_model import BombAnimationModel
from logic.settings.physics_settings import enemy_body_type
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.damage_data import DamageData


class Bomb(Unit):
    def __init__(self,
                 identifier: str,
                 group: LifecycleGroup,
                 x: float,
                 y: float,
                 enemies_provider: EnemiesProvider,
                 config: dict|None = None):

        animation_model = BombAnimationModel()
        shape = Circle(body=Body(body_type=enemy_body_type), radius=16)
        shape.density = 1

        super().__init__(identifier=identifier,
                         position=Vec2d(x, y),
                         shape=shape,
                         group=group,
                         animation_model=animation_model,
                         animated_object=animation_model.build_animated_object(scale=1.5, offset=(-30, -30)),
                         speed=30,
                         attack_config=None,
                         souls=1,
                         armor=0,
                         abilities=[
                             SpawnObjectAbility(),
                             MoveWithClosestEnemyAbility(
                                 retreat_chase_radius=None,
                                 enemies_provider=enemies_provider
                             ),
                             ExplosionAbility(
                                 trigger_radius=32,
                                 damage_radius=40,
                                 #damage_data=DamageData(damage=50, effects=[FrostEffect(duration=6, amount=3)]),
                                 damage_data=DamageData(damage=50, effects=[]),
                                 enemies_provider=enemies_provider
                             ),
                             StatusBarAbility(offset=(-40, -40)),
                         ],
                         reward=KillReward(souls=1, experience=1),
                         enemies_provider=enemies_provider,
                         name='Bomb')
