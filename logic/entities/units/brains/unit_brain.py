from __future__ import annotations

from typing import Any, MutableSequence

from pymunk import Vec2d, Shape

from logic.entities.abilities.ability import Ability
from logic.core.animated_object import AnimatedObject
from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.lifecycle import Lifecycle
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.rewards.kill_reward import KillReward
from logic.entities.units.brains.mixins.unit_abilities_mixin import UnitAbilitiesMixin
from logic.entities.units.brains.mixins.unit_animations_mixin import UnitAnimationsMixin
from logic.entities.units.brains.mixins.unit_armor_mixin import UnitArmorMixin
from logic.entities.units.brains.mixins.unit_attack_mixin import UnitAttackMixin, UnitAttackConfig
from logic.entities.units.brains.mixins.unit_effects_mixin import UnitEffectsMixin
from logic.entities.units.brains.mixins.unit_items_mixin import UnitItemsMixin
from logic.entities.units.brains.mixins.unit_life_mixin import UnitLifeMixin
from logic.entities.units.brains.mixins.unit_physics_mixin import UnitPhysicsMixin
from logic.entities.units.brains.mixins.unit_progress_mixin import UnitProgressMixin
from logic.entities.units.brains.mixins.unit_speed_mixin import UnitSpeedMixin
from logic.entities.units.data.unit_metadata import UnitMetadataKey
from logic.entities.units.models.animation_model import AnimationModel


class Unit(Lifecycle,
           UnitSpeedMixin,
           UnitArmorMixin,
           UnitEffectsMixin,
           UnitAbilitiesMixin,
           UnitAttackMixin,
           UnitItemsMixin,
           UnitLifeMixin,
           UnitAnimationsMixin,
           UnitPhysicsMixin,
           UnitProgressMixin):
    def __init__(self,
                 identifier: str,
                 position: Vec2d,
                 shape: Shape,
                 group: LifecycleGroup,
                 animation_model: AnimationModel,
                 animated_object: AnimatedObject,
                 speed: float,
                 attack_config: UnitAttackConfig | None,
                 souls: float,
                 armor: float,
                 abilities: list[Ability],
                 reward: KillReward | None,
                 enemies_provider: EnemiesProvider,
                 name: str):

        self.animation_model = animation_model
        self.animated_object = animated_object

        Lifecycle.__init__(self, group=group)
        UnitSpeedMixin.__init__(self, speed=speed, animated_object=self.animated_object, body=shape.body)
        UnitArmorMixin.__init__(self, armor=armor)
        UnitEffectsMixin.__init__(self)
        UnitAbilitiesMixin.__init__(self, abilities=abilities)
        UnitAttackMixin.__init__(self, config=attack_config, enemies_provider=enemies_provider)
        UnitItemsMixin.__init__(self)
        UnitLifeMixin.__init__(self, souls=souls, reward=reward)
        UnitAnimationsMixin.__init__(self)
        UnitPhysicsMixin.__init__(self, shape=shape, position=position)
        UnitProgressMixin.__init__(self)

        self.identifier = identifier
        self.metadata: dict[UnitMetadataKey, Any] = {
            UnitMetadataKey.ORIGINAL_SPEED: speed,
            UnitMetadataKey.ORIGINAL_SOULS: souls,
            UnitMetadataKey.ORIGINAL_ARMOR: armor,
        }
        self.name = name

        self.__mixins = [
            UnitPhysicsMixin,
            UnitArmorMixin,
            UnitEffectsMixin,
            UnitAbilitiesMixin,
            UnitItemsMixin,
            UnitLifeMixin,
            UnitSpeedMixin,
            UnitAttackMixin,
            UnitProgressMixin,
            UnitAnimationsMixin
        ]

    def process_input(self, events: MutableSequence):
        for mixin in self.__mixins:
            mixin.process_input(self, events=events)

    def pre_update(self):
        for mixin in self.__mixins:
            mixin.pre_update(self)

    def update(self):
        for mixin in self.__mixins:
            mixin.update(self)

    def post_update(self):
        for mixin in self.__mixins:
            mixin.post_update(self)

    def render(self, queue: DrawQueue):
        for mixin in self.__mixins:
            mixin.render(self, queue=queue)
