# Google Research Football — tournament build

This is a **patched, source-installable** copy of [Google Research Football](https://github.com/google-research/football) (`gfootball` 2.10.3.post1).

Do **not** `pip install gfootball` from PyPI. That package pins `gym<=0.21.0` (broken on current Python) and often fails while compiling the C++ engine.

Use this tree instead.

## What we changed vs upstream / PyPI

- `setup.py` is present and installable (the incomplete local `gfootball-src` tree was missing it).
- Runtime pin is `gym>=0.26.2,<0.27` plus `gymnasium`.
- Build isolation includes `psutil`; the engine script falls back if `psutil` is missing.
- The engine is compiled with the same Python that `pip` is using.
- Videos can be written as **mp4** (`avc1`, fallback `mp4v`), not only avi/webm.
- `gfootball.tournament.make_env()` returns a gymnasium-style env (`reset` → `(obs, info)`, `step` → 5-tuple).

`import gfootball` still works. Training stacks (Ray, SB3) are **not** bundled.

## System packages (required)

The C++ engine compiles on the participant machine.

**macOS**

```bash
brew install cmake sdl2 sdl2_image sdl2_ttf sdl2_gfx boost boost-python3
```

Use a Python that matches `boost-python3` when possible (Homebrew Python is the usual choice).

**Ubuntu / Debian**

```bash
sudo apt-get install git cmake build-essential libgl1-mesa-dev libsdl2-dev \
  libsdl2-image-dev libsdl2-ttf-dev libsdl2-gfx-dev libboost-all-dev \
  libdirectfb-dev libst-dev mesa-utils xvfb x11vnc python3-pip python3-dev
```

**Windows:** see `gfootball/doc/compile_engine.md` (vcpkg + `VCPKG_ROOT`).

## Install

Python **3.9–3.12** is the least painful. 3.13/3.14 can work if the engine compiles against that interpreter.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install psutil

# From this directory, or from a zip/git checkout of it:
python -m pip install --no-build-isolation .
```

`--no-build-isolation` is the reliable path (same as this project's training venv). With `pyproject.toml` a plain `pip install .` often works too because `psutil` is a build dependency.

Check:

```bash
python -c "import gfootball.env; from gfootball.tournament import make_env; print('ok')"
python examples/run_tournament_match.py --steps 50
```

## Tournament env

Default match: `11_vs_11_stochastic`, `simple115v2`, one agent-controlled player per side (teammates are built-in AI). Action space is **Discrete(19)** including idle (`0`).

```python
from gfootball.tournament import make_env

env = make_env()
obs, info = env.reset()
# obs is a list of two 115-d vectors: [left, right]
# right-side obs is already mirrored by gfootball
obs, reward, terminated, truncated, info = env.step([left_action, right_action])
```

Useful kwargs: `render=True`, `write_video=True`, `logdir="replays"`, `left_players=1`, `right_players=1`.

To dump a match video:

```python
env = make_env(write_video=True, write_full_episode_dumps=True, logdir="replays", render=True)
```

## Distribute to participants

Zip or git-clone **this folder** (it must include `setup.py`, `gfootball/`, and `third_party/`):

```bash
python -m pip install --no-build-isolation /path/to/gfootball-tournament
```

or:

```bash
python -m pip install --no-build-isolation git+https://YOUR_HOST/gfootball-tournament.git
```

Do not point people at PyPI `gfootball`.

## License

Apache 2.0 (upstream Google Research Football). Upstream README: `README.upstream.md`.
