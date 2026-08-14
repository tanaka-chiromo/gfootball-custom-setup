"""Bridge gfootball's legacy gym 4-tuple API to gymnasium reset/step."""

from __future__ import annotations


class GymnasiumCompat:
  """Wraps a gfootball env so reset() -> (obs, info) and step() is 5-tuple."""

  def __init__(self, env):
    self.env = env
    self.observation_space = getattr(env, "observation_space", None)
    self.action_space = getattr(env, "action_space", None)
    self.metadata = getattr(env, "metadata", {"render_modes": []})
    self.reward_range = getattr(env, "reward_range", (-float("inf"), float("inf")))
    self.spec = getattr(env, "spec", None)

  def reset(self, **kwargs):
    result = self.env.reset(**kwargs)
    if isinstance(result, tuple) and len(result) == 2:
      return result
    return result, {}

  def step(self, action):
    result = self.env.step(action)
    if len(result) == 4:
      obs, reward, done, info = result
      return obs, reward, done, False, info
    return result

  def render(self, *args, **kwargs):
    return self.env.render(*args, **kwargs)

  def close(self):
    close = getattr(self.env, "close", None)
    if close is not None:
      return close()
    return None

  def seed(self, seed=None):
    seed_fn = getattr(self.env, "seed", None)
    if seed_fn is not None:
      return seed_fn(seed)
    return None

  def __getattr__(self, name):
    return getattr(self.env, name)
