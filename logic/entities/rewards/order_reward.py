from logic.entities.rewards.reward import Reward


class OrderReward(Reward):
    def __init__(self, fame: int):
        self.__fame = fame

    def apply(self, unit):
        unit.set_fame(unit.fame + self.__fame)
