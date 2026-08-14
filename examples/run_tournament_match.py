#!/usr/bin/env python3
"""Play one 11v11 match with random agents on both sides (smoke test)."""

import argparse
import random

from gfootball.tournament import make_env


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--steps", type=int, default=200)
  parser.add_argument("--render", action="store_true")
  args = parser.parse_args()

  env = make_env(render=args.render)
  obs, info = env.reset()
  n_actions = env.action_space.nvec[0] if hasattr(env.action_space, "nvec") else env.action_space.n

  total = 0.0
  for _ in range(args.steps):
    if isinstance(obs, (list, tuple)):
      action = [random.randrange(n_actions) for _ in obs]
    else:
      action = random.randrange(n_actions)
    obs, reward, terminated, truncated, info = env.step(action)
    total += float(sum(reward) if hasattr(reward, "__len__") else reward)
    if terminated or truncated:
      break

  env.close()
  print("ok steps_reward=%.3f" % total)


if __name__ == "__main__":
  main()
