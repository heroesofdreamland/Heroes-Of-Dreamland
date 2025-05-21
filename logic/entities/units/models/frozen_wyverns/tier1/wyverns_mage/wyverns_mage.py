from pymunk import Vec2d, Circle, Body

from logic.entities.abilities.auto_attack_ability import RangedAutoAttackAbility
from logic.entities.abilities.death_object_ability import DeathObjectAbility
from logic.entities.abilities.move_with_closest_enemy_ability import MoveWithClosestEnemyAbility
from logic.entities.abilities.resurrection_ability import ResurrectionAbility
from logic.entities.abilities.spawn_object_ability import SpawnObjectAbility
from logic.entities.abilities.status_bar_ability import StatusBarAbility
from logic.core.lifecycle_group import LifecycleGroup
from logic.entities.projectiles.arrow import Arrow
from logic.entities.rewards.kill_reward import KillReward
from logic.entities.units.models.frozen_wyverns.tier1.wyverns_mage.wyverns_mage_animation_model import \
    WyvernsMageAnimationModel
from logic.settings.physics_settings import enemy_body_type
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.brains.mixins.unit_attack_mixin import UnitAttackConfig
from logic.entities.units.brains.unit_brain import Unit


class WyvernsMage(Unit):
    def __init__(self,
                 identifier: str,
                 group: LifecycleGroup,
                 x: float,
                 y: float,
                 enemies_provider: EnemiesProvider,
                 config: dict|None = None):

        attack_animation_duration = 1
        attack_cooldown = 1.5
        animation_model = WyvernsMageAnimationModel(attack_animation_duration=attack_animation_duration, attack_cooldown=attack_cooldown)
        shape = Circle(body=Body(body_type=enemy_body_type), radius=20)
        shape.density = 1

        super().__init__(identifier=identifier,
                         position=Vec2d(x, y),
                         shape=shape,
                         group=group,
                         animation_model=animation_model,
                         animated_object=animation_model.build_animated_object(scale=1, offset=(-36, -36)),
                         speed=25,
                         attack_config=UnitAttackConfig(duration=attack_animation_duration, attack_moment=0.3, cooldown=attack_cooldown),
                         souls=1,
                         armor=0,
                         abilities=[
                             SpawnObjectAbility(),
                             DeathObjectAbility(),
                             RangedAutoAttackAbility(
                                 trigger_radius=200,
                                 damage_radius=250,
                                 projectile_type=Arrow,
                                 enemies_provider=enemies_provider,
                                 offset=(-30, -30)
                             ),
                             MoveWithClosestEnemyAbility(
                                 retreat_chase_radius=(0, 200),
                                 enemies_provider=enemies_provider
                             ),
                             StatusBarAbility(offset=(-36, -36)),
                             # ResurrectionAbility(wait_duration=2)
                         ],
                         reward=KillReward(souls=1, experience=1),
                         enemies_provider=enemies_provider,
                         name='Wyverns Mage')
