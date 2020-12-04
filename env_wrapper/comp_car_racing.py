from competitive_rl import make_envs
from competitive_rl.car_racing import make_competitive_car_racing
import numpy as np

class CarEnv():
    """
    Environment wrapper for CarRacing 
    """
    def __init__(self, crop, grass_penalty, action_repeat):
        self.crop = crop
        self.grass_penalty = grass_penalty
        self.action_repeat = action_repeat
    
    def set_logger(self, logger):
        self._logger = logger

    def seed(self, seed):
        self.env.seed(seed)

    def reset(self):
        obs = self.env.reset()
        return self.preprocess(obs)

    def step(self, action, evaluate=False):
        for i in range(self.action_repeat):
            total_reward = 0
            try:    # render error can happen due to: "ValueError: subsurface rectangle outside surface area"
                obs, reward, done, _ = self.env.step(action)
            except ValueError as e:
                obs = self.env.reset()
                reward = -100
                done = True
                if hasattr(self, '_logger') and self._logger is not None:
                    self._logger.warning("step ValueError with action: {}, overwrite reward to 0.".format(action))

            obs = self.preprocess(obs)
            if self.grass_penalty and not evaluate:
                if self.crop:
                    patch = obs[-30:-1, 43-20:43+20, 0]
                else:
                    patch = obs[-40:-10, 48-20:48+20, 0]
                if patch.mean() > 150.0:  # surrounded by grass -> penalty
                    reward -= self.grass_penalty
            
            total_reward += reward
            if done:
                break

        return obs, total_reward, done, {}

    def render(self, *arg):
        self.env.render(*arg)

    def preprocess(self, obs):
        obs = obs[0, :, :]   # unstack  
        if self.crop:
            obs = obs[0:-10, 5:-5]      # crop, remove bottom bar (96, 96) -> (86, 86)
        obs = np.stack((obs,)*1, axis=-1)
        return obs

class SingleCarEnv(CarEnv):
    def __init__(self, crop=True, grass_penalty=0, action_repeat=1):
        comp_envs = make_envs("cCarRacing-v0", num_envs=1, action_repeat=1)
        self.env = comp_envs.envs[0]
        super().__init__(crop, grass_penalty, action_repeat)

class CompetitiveCarEnv(CarEnv):
    def __init__(self, opponent_policy, crop=True, grass_penalty=0, action_repeat=1):
        self.opponent_policy = opponent_policy
        comp_envs = make_competitive_car_racing(opponent_policy, num_envs=1, action_repeat=1)
        self.env = comp_envs.envs[0]
        super().__init__(crop, grass_penalty, action_repeat) 
    