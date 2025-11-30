# Flappy Bird with AI

A pygame recreation of Flappy Bird with an optional rule-based AI that can take over the bird and fly through pipes automatically.

## Features
- Classic Flappy Bird gameplay with scrolling pipes and score tracking.
- Toggleable AI (`USE_AI` in `flappybird.py`) that predicts the upcoming pipe gap and issues flap/no-op actions.
- Click-to-flap manual mode still supported.
- Simple assets bundled locally (`images/`, `music/`).

## Requirements
- Python 3.9+ recommended.
- Install dependencies:
  ```bash
  python -m venv flappyenv
  source flappyenv/bin/activate  # Windows: flappyenv\Scripts\activate
  pip install -r requirements.txt
  ```
  Core runtime is `pygame`; other pinned packages are unused by the game but kept for completeness.

## How to Run
From the `Flappy-bird/` directory:
```bash
python flappybird.py
```

## Controls
- **AI mode (default):** `USE_AI = True` near the top of `flappybird.py`. The AI will start flying automatically.
- **Manual mode:** Set `USE_AI = False` and click/hold the left mouse button to flap.
- **Restart:** Click the restart button when the game is over.
- **Quit:** Close the window.

## AI Overview
- Location: `ai_agent.py` (`RuleBasedAIAgent`).
- Strategy: Predicts where the bird will be when it reaches the next pipe, compares glide vs. flap trajectories, and chooses the action closest to the gap center with safety guards for ceiling/ground and rising too fast.
- Integration: `flappybird.py` creates a single agent instance and feeds it the bird, pipe group, and current gap size each frame; the agent sets a flag consumed by the bird update loop.
- Tuning knobs:
  - `USE_AI` (bool) in `flappybird.py` to enable/disable.
  - `flap_strength` (currently `-4` in `flappybird.py`) controls flap height.
  - `RuleBasedAIAgent` parameters (buffer/margins) can be adjusted in `ai_agent.py` for tighter or looser flight paths.

## Project Structure
- `flappybird.py` — main game loop, rendering, input handling, and AI wiring.
- `ai_agent.py` — rule-based AI policy.
- `images/` — sprites for background, ground, pipes, and bird animation.
- `music/` — background music.
- `requirements.txt` — Python dependencies.

## Notes
- Audio plays by default; mute system volume if needed.
- If the AI feels too cautious or too aggressive, tweak the margin/bias values in `ai_agent.py` and/or the `flap_strength` in `flappybird.py` to suit your preferred path through gaps.
