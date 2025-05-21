from pymunk import Vec2d, Circle, Body

from logic.entities.abilities.auto_attack_ability import MeleeAutoAttackAbility
from logic.entities.abilities.death_object_ability import DeathObjectAbility
from logic.entities.abilities.move_with_closest_enemy_ability import MoveWithClosestEnemyAbility
from logic.entities.abilities.spawn_object_ability import SpawnObjectAbility
from logic.entities.abilities.status_bar_ability import StatusBarAbility
from logic.entities.abilities.trojan_ability import TrojanAbility
from logic.core.lifecycle_group import LifecycleGroup
from logic.entities.rewards.kill_reward import KillReward
from logic.entities.units.models.frozen_wyverns.tier2.mini_treant.mini_treant_animation_model import MiniTreantAnimationModel
from logic.settings.physics_settings import enemy_body_type
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.brains.mixins.unit_attack_mixin import UnitAttackConfig
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.damage_data import DamageData
from logic.entities.units.data.enemy_config import EnemyConfigKey


class MiniTreant(Unit):
    def __init__(self,
                 identifier: str,
                 group: LifecycleGroup,
                 x: float,
                 y: float,
                 enemies_provider: EnemiesProvider,
                 config: dict|None = None):

        attack_animation_duration = 0.8
        trojan_depth = 2
        if config is not None and EnemyConfigKey.TROJAN_DEPTH in config:
            trojan_depth = config[EnemyConfigKey.TROJAN_DEPTH]

        trojan_size_scale: float = 1
        if trojan_depth == 1:
            trojan_size_scale = 0.7
        elif trojan_depth == 0:
            trojan_size_scale = 0.5

        animation_model = MiniTreantAnimationModel(attack_animation_duration=attack_animation_duration)
        shape = Circle(body=Body(body_type=enemy_body_type), radius=16 * trojan_size_scale)
        shape.density = 1

        super().__init__(identifier=identifier,
                         position=Vec2d(x, y),
                         shape=shape,
                         group=group,
                         animation_model=animation_model,
                         animated_object=animation_model.build_animated_object(scale=trojan_size_scale, offset=(-20 * trojan_size_scale, -20 * trojan_size_scale)),
                         speed=45 / trojan_size_scale,
                         attack_config=UnitAttackConfig(duration=attack_animation_duration,
                                                        attack_moment=0.6,
                                                        cooldown=0),
                         souls=2,
                         armor=0,
                         abilities=[
                             SpawnObjectAbility(),
                             DeathObjectAbility(),
                             MeleeAutoAttackAbility(
                                 trigger_radius=shape.radius,
                                 damage_radius=40 * trojan_size_scale,
                                 damage_data=DamageData(damage=1),
                                 enemies_provider=enemies_provider
                             ),
                             MoveWithClosestEnemyAbility(
                                 retreat_chase_radius=None,
                                 enemies_provider=enemies_provider
                             ),
                             StatusBarAbility(offset=(-20 * trojan_size_scale, -20 * trojan_size_scale)),
                             TrojanAbility(summon_type=MiniTreant,
                                           count_of_summons=3,
                                           depth=trojan_depth),
                         ],
                         reward=KillReward(souls=1, experience=1),
                         enemies_provider=enemies_provider,
                         name='Mini Treant')
