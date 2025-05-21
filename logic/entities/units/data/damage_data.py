from logic.entities.effects.effect import Effect


class DamageData:
    def __init__(self, damage: float, effects: list[Effect] | None = None):
        self.damage = damage
        if effects is None:
            self.effects = []
        else:
            self.effects = effects
