"""Tournament helpers on top of the patched gfootball environment."""

from gfootball.env import create_environment
from gfootball.env.gymnasium_compat import GymnasiumCompat

DEFAULT_ENV_NAME = "11_vs_11_stochastic"
DEFAULT_REPRESENTATION = "simple115v2"
DEFAULT_REWARDS = "scoring"


def make_env(
    env_name=DEFAULT_ENV_NAME,
    representation=DEFAULT_REPRESENTATION,
    rewards=DEFAULT_REWARDS,
    left_players=1,
    right_players=1,
    render=False,
    write_video=False,
    write_full_episode_dumps=False,
    logdir="",
    gymnasium=True,
    other_config_options=None,
):
  """Create a match env with one (or more) agent-controlled players per side.

  Observations:
    - 1 player total: a single vector / image
    - 2+ players: a list, left controls first, then right
      (gfootball mirrors the right-side observation)

  Actions are Discrete(19) per controlled player (idle is 0).
  """
  extra = dict(other_config_options or {})
  extra.setdefault("video_format", "mp4")
  env = create_environment(
      env_name=env_name,
      stacked=False,
      representation=representation,
      rewards=rewards,
      write_full_episode_dumps=write_full_episode_dumps,
      render=render,
      write_video=write_video,
      logdir=logdir,
      number_of_left_players_agent_controls=left_players,
      number_of_right_players_agent_controls=right_players,
      other_config_options=extra,
  )
  if gymnasium:
    env = GymnasiumCompat(env)
  return env
