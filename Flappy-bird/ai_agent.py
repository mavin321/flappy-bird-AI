"""Simple AI agent for Flappy Bird.

The agent is rule-based: it looks at the next pipe's gap and the bird's
current height/velocity and decides whether to flap. This keeps the code
lightweight and works with the existing game loop.
"""

from __future__ import annotations

from typing import Iterable, Optional

import pygame


class RuleBasedAIAgent:
    """Lightweight agent that chooses flap/no-op actions."""

    def __init__(self, flap_buffer: int = 25) -> None:
        # flap_buffer adds a margin so the bird stays a bit below gap center (larger = lower path)
        self.flap_buffer = flap_buffer

    def reset(self) -> None:
        """Reset any internal state (kept for future extensions)."""
        return None

    def choose_action(
        self, bird: pygame.sprite.Sprite, pipes: Iterable[pygame.sprite.Sprite], pipe_gap: int
    ) -> bool:
        """Return True to flap, False to glide."""
        next_pipe = self._next_bottom_pipe(bird, pipes)
        if not next_pipe:
            # No pipes yet: hover around mid-screen to avoid crashing early.
            return bird.rect.centery > 260

        gap_center = next_pipe.rect.top - pipe_gap / 2
        height_delta = bird.rect.centery - gap_center
        horizontal_distance = next_pipe.rect.right - bird.rect.left
        bird_velocity = getattr(bird, "vel", 0)

        # Flap if the bird is below the desired track or is dropping too fast near a pipe.
        if height_delta > self.flap_buffer:
            return True
        if horizontal_distance < 70 and height_delta > 0 and bird_velocity > 4:
            return True

        return False

    def _next_bottom_pipe(
        self, bird: pygame.sprite.Sprite, pipes: Iterable[pygame.sprite.Sprite]
    ) -> Optional[pygame.sprite.Sprite]:
        """Return the closest upcoming bottom pipe relative to the bird."""
        candidates = [
            pipe
            for pipe in pipes
            if getattr(pipe, "position", -1) == -1 and pipe.rect.right >= bird.rect.left
        ]
        if not candidates:
            return None
        return min(candidates, key=lambda p: p.rect.right)
