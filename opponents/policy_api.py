import gin
from competitive_rl import make_envs
from gym import spaces
import numpy as np

from .ppo.ppo_trainer import PPOTrainer, ppo_config

@gin.configurable
class PPOPolicyAPI:
    def __init__(self, log_dir=None, suffix=None, _test=False):
        # self.resized_dim = 42
        # env = make_envs(env_id='cCarRacing-v0', num_envs=1)
        # a hack: avoid make a useless env only to fetch observation space, which can cause GPU usage spike
        env = type('', (), {})()    # fake env object
        env.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(4, 96, 96),
            dtype=np.uint8
        )

        env.action_space = spaces.Box(np.array([-1, -1]), np.array([+1, +1]), dtype=np.float32)
        self.obs_shape = env.observation_space.shape
        self.agent = PPOTrainer(env, ppo_config)
        if log_dir is not None:  # log_dir is None only in testing
            success = self.agent.load_w(log_dir, suffix)
            if not success and not _test:
                raise ValueError("Failed to load agent!")

    def reset(self):
        pass

    def __call__(self, obs):
        action = self.agent.compute_action(obs, True)[1]
        action = action.detach().cpu().numpy()
        return action[0]