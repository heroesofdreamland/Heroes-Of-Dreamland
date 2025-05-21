from logic.entities.rewards.lvlup_reward import LevelUpReward

threshold_rewards = [
        (10, LevelUpReward(10, 1.5)),
        (20, LevelUpReward(20, 3)),
        (30, LevelUpReward(30, 4.5)),
        (10, LevelUpReward(40, 6)),
        (10, LevelUpReward(50, 7.5)),
        (10, LevelUpReward(100, 10))
]
max_level_threshold_reward = len(threshold_rewards) - 1
