from pymunk import Circle, Body, Vec2d

from logic.entities.abilities.absorb_souls_ability import AbsorbSoulsAbility
from logic.entities.abilities.manual_attack_ability import ManualAttackAbility
from logic.entities.abilities.move_with_keyboard_ability import MoveWithKeyboardAbility
from logic.core.lifecycle_group import LifecycleGroup
from logic.entities.units.models.player_characters.kron.kron_animation_model import KronAnimationModel
from logic.settings.physics_settings import player_body_type
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.brains.mixins.unit_attack_mixin import UnitAttackConfig
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.damage_data import DamageData


class Kron(Unit):
    def __init__(self,
                 identifier: str,
                 group: LifecycleGroup,
                 x: float,
                 y: float,
                 enemies_provider: EnemiesProvider,
                 config: dict | None = None):

        attack_animation_duration = 0.9
        animation_model = KronAnimationModel(attack_animation_duration=attack_animation_duration)
        shape = Circle(body=Body(body_type=player_body_type), radius=18)
        shape.density = 10000
        position = Vec2d(x, y)

        super().__init__(identifier=identifier,
                         position=position,
                         shape=shape,
                         group=group,
                         animation_model=animation_model,
                         animated_object=animation_model.build_animated_object(scale=1, offset=(-30, -30)),
                         speed=250,
                         attack_config=UnitAttackConfig(duration=attack_animation_duration, attack_moment=0.6, cooldown=0),
                         souls=100,
                         armor=0,
                         abilities=[
                             MoveWithKeyboardAbility(),
                             ManualAttackAbility(
                                 damage_radius=40,
                                 max_attack_enemies=2,
                                 damage_data=DamageData(damage=1),
                                 enemies_provider=enemies_provider
                             ),
                             AbsorbSoulsAbility(radius=None),
                         ],
                         reward=None,
                         enemies_provider=enemies_provider,
                         name='Kron')
