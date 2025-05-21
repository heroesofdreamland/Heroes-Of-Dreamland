from pymunk import Vec2d, Circle, Body

from logic.entities.abilities.auto_attack_ability import MeleeAutoAttackAbility
from logic.entities.abilities.death_object_ability import DeathObjectAbility
from logic.entities.abilities.move_with_closest_enemy_ability import MoveWithClosestEnemyAbility
from logic.entities.abilities.resurrection_ability import ResurrectionAbility
from logic.entities.abilities.spawn_object_ability import SpawnObjectAbility
from logic.entities.abilities.status_bar_ability import StatusBarAbility
from logic.core.lifecycle_group import LifecycleGroup
from logic.entities.effects.negative.frost_effect import FrostEffect
from logic.entities.rewards.kill_reward import KillReward
from logic.settings.physics_settings import enemy_body_type
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.brains.mixins.unit_attack_mixin import UnitAttackConfig
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.damage_data import DamageData
from logic.entities.units.data.enemy_config import EnemyConfigKey
from logic.entities.units.models.frozen_wyverns.tier1.warrior.warrior_animation_model import WarriorAnimationModel


class Warrior(Unit):
    def __init__(self,
                 identifier: str,
                 group: LifecycleGroup,
                 x: float,
                 y: float,
                 enemies_provider: EnemiesProvider,
                 config: dict|None = None):
        is_summoned = False
        if config is not None and EnemyConfigKey.IS_SUMMONED in config:
            is_summoned = config[EnemyConfigKey.IS_SUMMONED]

        attack_animation_duration = 0.5
        animation_model = WarriorAnimationModel(attack_animation_duration=attack_animation_duration, is_summoned=is_summoned)

        shape = Circle(body=Body(body_type=enemy_body_type), radius=20)
        shape.density = 1
        abilities = [
            SpawnObjectAbility(),
            DeathObjectAbility(),
            MeleeAutoAttackAbility(
                trigger_radius=shape.radius,
                damage_radius=70,
                #damage_data=DamageData(damage=1, effects=[FrostEffect(duration=6)]),
                damage_data=DamageData(damage=1, effects=[]),
                enemies_provider=enemies_provider
            ),
            MoveWithClosestEnemyAbility(
                retreat_chase_radius=None,
                enemies_provider=enemies_provider
            ),
            StatusBarAbility(offset=(-36, -36)),
        ]
        if not is_summoned:
            abilities.append(ResurrectionAbility(wait_duration=2))


        super().__init__(identifier=identifier,
                         position=Vec2d(x, y),
                         shape=shape,
                         group=group,
                         animation_model=animation_model,
                         animated_object=animation_model.build_animated_object(scale=1, offset=(-32, -32)),
                         speed=30,
                         attack_config=UnitAttackConfig(duration=attack_animation_duration, attack_moment=0.6, cooldown=0),
                         souls=1,
                         armor=0,
                         abilities=abilities,
                         reward=KillReward(souls=1, experience=1),
                         enemies_provider=enemies_provider,
                         name='Warrior')
