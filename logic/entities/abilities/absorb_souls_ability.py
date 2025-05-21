from logic.entities.abilities.detect_deaths_ability import DetectDeathsAbility
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.unit_life_state import UnitLifeState


class __SoulsAbsorptionManager:
    def __init__(self):
        self.__candidates = {}
        self.__is_resolved = False

    def add(self, owner: Unit, unit: Unit):
        self.__is_resolved = False
        if unit in self.__candidates:
            self.__candidates[unit].append(owner)
        else:
            self.__candidates[unit] = [owner]

    def resolve(self):
        if self.__is_resolved:
            return
        for unit in self.__candidates:
            closest_owner = None
            for current_owner in self.__candidates[unit]:
                if closest_owner is None:
                    closest_owner = current_owner
                else:
                    closest_owner_distance = closest_owner.distance(shape=unit.shape)
                    current_owner_distance = current_owner.distance(shape=unit.shape)
                    if current_owner_distance < closest_owner_distance:
                        closest_owner = current_owner
            if closest_owner is not None and unit.reward is not None:
                unit.reward.absorb_souls(closest_owner)

        self.__candidates = {}
        self.__is_resolved = True

_souls_absorption_manager = __SoulsAbsorptionManager()


class AbsorbSoulsAbility(DetectDeathsAbility):
    def __init__(self, radius: float | None):
        super().__init__(radius, self.__handle_enemy_death)

    def post_update(self, owner: object):
        super().post_update(owner=owner)
        _souls_absorption_manager.resolve()

    @staticmethod
    def __handle_enemy_death(owner: Unit, unit: Unit):
        if owner != unit and owner.life_state == UnitLifeState.ALIVE:
            _souls_absorption_manager.add(owner=owner, unit=unit)