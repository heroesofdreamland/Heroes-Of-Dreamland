from logic.entities.rewards.reward import Reward


class KillReward(Reward):
    def __init__(self, souls: int, experience: int):
        self.__experience = experience
        self.__souls = souls
        #future: drop[items]

    def apply(self, unit):
        unit.add_experience(self.__experience)

    def absorb_souls(self, unit):
        unit.add_souls(self.__souls)