# pro-flap — Flappy Bird in Python/Pygame

A clean, modular Flappy Bird clone built with Python 3.11 and pygame.
Runs natively on desktop **and** in the browser via [pygbag](https://github.com/pygame-web/pygbag) (WebAssembly).
Auto-deployed to GitHub Pages on every push to `main`.

---

## Project Structure

```
pro-flap/
├── main.py                   # Entry point — asyncio game loop
├── environment.yml           # Conda environment (python 3.11 + pygame + pygbag)
├── game/
│   ├── constants.py          # All tunable numbers (physics, colors, sizes)
│   ├── state.py              # GameState enum: MENU | PLAYING | GAME_OVER
│   ├── bird.py               # Bird: gravity, flap, tilt, hitbox
│   ├── pipe.py               # Pipe + PipeManager: spawn, scroll, collision
│   ├── ground.py             # Scrolling ground strip
│   ├── score.py              # Current score + session best
│   └── renderer.py           # All pygame.draw calls (pure drawing, no logic)
└── .github/workflows/
    └── deploy.yml            # CI: pygbag build → GitHub Pages
```

---

## How It Works

### Game loop (`main.py`)
The loop is an `async def` function called via `asyncio.run()`.
This is required by pygbag — `await asyncio.sleep(0)` at the end of every frame
yields control back to the browser's event loop so the tab stays responsive.

```
Frame:
  1. Collect events  (SPACE / click → flap/start/restart)
  2. Update physics  (bird gravity, pipe scroll, ground scroll)
  3. Check collisions → GAME_OVER
  4. Render          (background → pipes → ground → bird → HUD → overlay)
  5. await asyncio.sleep(0)   ← browser yield point
```

### State machine
```
MENU  ──(flap)──▶  PLAYING  ──(hit pipe/ground)──▶  GAME_OVER
  ▲                                                       │
  └───────────────────(flap)─────────────────────────────┘
```

### Module responsibilities

| Module | What it owns |
|---|---|
| `constants.py` | Every magic number — change physics/colors here only |
| `state.py` | `GameState` enum — the single source of truth for game phase |
| `bird.py` | Velocity, gravity, flap impulse, tilt angle, inset hitbox |
| `pipe.py` | `Pipe` (top+bottom rects, passed flag) + `PipeManager` (timer spawn, cull, score) |
| `ground.py` | Wrapping scroll offset, collision rect |
| `score.py` | `current` and session `best` counters |
| `renderer.py` | Pure drawing — receives objects, emits draw calls, owns fonts |

### pygbag compatibility rules (baked in)
- Game loop is `async def main()` + `await asyncio.sleep(0)` each frame
- No `sys.exit()` — `return` from `main()` instead
- No WAV/MP3 audio (OGG only if you add sound later)
- No BMP images — uses `pygame.draw` primitives only (zero asset files)

---

## Quick Start

### 1. Set up the conda environment

```bash
conda env create -f environment.yml
conda activate pro-flap
```

### 2. Run on desktop

```bash
python main.py
```

Controls: **Space** or **mouse click** to flap / start / restart.

### 3. Run in browser (local test)

```bash
python -m pygbag main.py
# Open http://localhost:8000 in your browser
```

### 4. Build the WebAssembly bundle

```bash
python -m pygbag --build main.py
# Output is in build/web/ — upload these files to any static host
```

---

## Hosting on GitHub Pages (automatic)

Push to `main` and the GitHub Actions workflow (`.github/workflows/deploy.yml`) will:

1. Install `pygame` + `pygbag`
2. Run `python -m pygbag --build main.py`
3. Deploy `build/web/` to the `gh-pages` branch

Enable GitHub Pages in your repo settings:
**Settings → Pages → Source → Deploy from branch → `gh-pages` / `/ (root)`**

Your game will then be live at:
`https://<your-github-username>.github.io/pro-flap/`

---

## Tweaking the game

All tunable constants live in `game/constants.py`:

| Constant | Default | Effect |
|---|---|---|
| `GRAVITY` | `0.5` | How fast the bird falls |
| `FLAP_STRENGTH` | `-9.0` | Upward impulse on flap |
| `PIPE_SPEED` | `3` | Horizontal scroll speed |
| `PIPE_GAP` | `160` | Vertical gap between pipes |
| `PIPE_INTERVAL` | `1500` ms | Time between pipe spawns |
| `MAX_FALL_SPEED` | `12.0` | Terminal velocity |
| `BIRD_HITBOX_SHRINK` | `4` px | Hitbox inset (bigger = more forgiving) |
