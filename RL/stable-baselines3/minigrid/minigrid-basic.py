import gymnasium as gym
import torch
import torch.nn as nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
import minigrid
from gymnasium.wrappers import RecordVideo
from minigrid.wrappers import ImgObsWrapper
from stable_baselines3 import PPO
import os
import time


class MinigridFeaturesExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space: gym.Space, features_dim: int = 512, normalized_image: bool = False) -> None:
        super().__init__(observation_space, features_dim)
        n_input_channels = observation_space.shape[0]
        self.cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 16, (2, 2)),
            nn.ReLU(),
            nn.Conv2d(16, 32, (2, 2)),
            nn.ReLU(),
            nn.Conv2d(32, 64, (2, 2)),
            nn.ReLU(),
            nn.Flatten(),
        )

        # Compute shape by doing one forward pass
        with torch.no_grad():
            n_flatten = self.cnn(torch.as_tensor(observation_space.sample()[None]).float()).shape[1]

        self.linear = nn.Sequential(nn.Linear(n_flatten, features_dim), nn.ReLU())

    def forward(self, observations: torch.Tensor) -> torch.Tensor:
        return self.linear(self.cnn(observations))
    
policy_kwargs = dict(
    features_extractor_class=MinigridFeaturesExtractor,
    features_extractor_kwargs=dict(features_dim=128),
)

env = gym.make("MiniGrid-Fetch-8x8-N3-v0", render_mode="rgb_array")
env = ImgObsWrapper(env)

model = None
if not os.path.exists("ppo_minigrid.zip"):
    model = PPO("CnnPolicy", env, policy_kwargs=policy_kwargs, verbose=1)
    model.learn(100000)
    model.save("ppo_minigrid")
else: 
    model = PPO("CnnPolicy", env=env, policy_kwargs=policy_kwargs, verbose=1).load("ppo_minigrid",env=env)

print (model)
vec_env = model.get_env()
obs = vec_env.reset()

# Wrap the environment with RecordVideo
#video_folder = './videos/'
#vec_env = RecordVideo(vec_env, video_folder=video_folder, episode_trigger=lambda episode_id: True)

for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = vec_env.step(action)
    #time.sleep(0.1)
    vec_env.render("human")