import gym

from stable_baselines3 import A2C,DQN

env = gym.make("FrozenLake-v1")

model = A2C("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10_000)

obs = env.reset()
for i in range(1000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
#    print (done)
    env.render()
    if done:
      obs = env.reset()
