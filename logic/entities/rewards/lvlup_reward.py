from typing import cast

from logic.entities.rewards.reward import Reward


class LevelUpReward(Reward):
    def __init__(self, souls: float, damage: float):
        self.__souls = souls
        self.__damage = damage

    def apply(self, unit):
        unit.add_souls(self.__souls)
        unit.add_level(1)
        unit.reset_experience()
        unit.effects_clean()
        from logic.entities.abilities.manual_attack_ability import ManualAttackAbility
        attack_ability = unit.ability(ManualAttackAbility)
        if attack_ability is not None:
            cast(ManualAttackAbility, attack_ability).damage_data.damage += self.__damage

