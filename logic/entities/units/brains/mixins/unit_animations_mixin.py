from typing import cast, MutableSequence

from logic.entities.abilities.resurrection_ability import ResurrectionAbility
from logic.core.draw_queue import DrawQueue
from logic.entities.units.brains.mixins.unit_attack_mixin import AttackState
from logic.entities.units.data.unit_life_state import UnitLifeState
from logic.entities.units.models.animation_type import AnimationType


class UnitAnimationsMixin:
    def process_input(self, events: MutableSequence):
        pass

    def pre_update(self):
        pass

    def update(self):
        from logic.entities.units.brains.unit_brain import Unit
        unit = cast(Unit, self)
        # Prioroty:
        # 1. unit dead
        # 2. unit move
        # 3. unit attack
        # 4. unit idle
        match unit.life_state:
            case UnitLifeState.DEATH:
                # unit dead
                resurrection_ability = unit.ability(ability_type=ResurrectionAbility)
                if resurrection_ability is None or not resurrection_ability.is_enabled:
                    unit.animated_object.configure_animation(AnimationType.DEATH)
                elif not resurrection_ability.is_resurrecting:
                    unit.animated_object.configure_animation(AnimationType.DEATH_WITH_RESURRECTION)
                else:
                    pass
            case UnitLifeState.ALIVE:
                if unit.is_moving:
                    unit.animated_object.configure_animation(AnimationType.RUN)
                else:
                    match unit.attack_state:
                        case AttackState.BEFORE_ATTACK | AttackState.ATTACK | AttackState.AFTER_ATTACK:
                            unit.animated_object.configure_animation(AnimationType.ATTACK)
                        case AttackState.NONE:
                            if unit.is_stunned and AnimationType.STUN in unit.animated_object.animations:
                                unit.animated_object.configure_animation(AnimationType.STUN)
                            else:
                                unit.animated_object.configure_animation(AnimationType.IDLE)
                        case AttackState.COOLDOWN:
                            if AnimationType.BREATHING in unit.animated_object.animations:
                                unit.animated_object.configure_animation(AnimationType.BREATHING)
                            else:
                                unit.animated_object.configure_animation(AnimationType.IDLE)

    def post_update(self):
        pass

    def render(self, queue: DrawQueue):
        from logic.entities.units.brains.unit_brain import Unit
        unit = cast(Unit, self)
        unit.animated_object.position = unit.position
        queue.draw(group=unit.group, animated_object=unit.animated_object, game_space=True)
