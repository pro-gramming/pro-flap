from __future__ import annotations

import random
import pygame
from game.constants import (
    WIDTH, HEIGHT, GROUND_HEIGHT,
    PIPE_WIDTH, PIPE_GAP, PIPE_SPEED,
    PIPE_INTERVAL, PIPE_MIN_HEIGHT,
)


class Pipe:
    """A single pipe pair (top + bottom) at a given x position."""

    def __init__(self, x: int) -> None:
        self.x = x
        self.passed: bool = False

        # Random gap centre, kept away from ceiling and ground
        gap_min = PIPE_MIN_HEIGHT + PIPE_GAP // 2
        gap_max = HEIGHT - GROUND_HEIGHT - PIPE_MIN_HEIGHT - PIPE_GAP // 2
        gap_centre = random.randint(gap_min, gap_max)

        self.top_rect = pygame.Rect(x, 0, PIPE_WIDTH, gap_centre - PIPE_GAP // 2)
        self.bottom_rect = pygame.Rect(
            x,
            gap_centre + PIPE_GAP // 2,
            PIPE_WIDTH,
            HEIGHT - GROUND_HEIGHT - (gap_centre + PIPE_GAP // 2),
        )

    def update(self) -> None:
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def is_off_screen(self) -> bool:
        return self.x + PIPE_WIDTH < 0

    def collides_with(self, hitbox: pygame.Rect) -> bool:
        return hitbox.colliderect(self.top_rect) or hitbox.colliderect(self.bottom_rect)

    def bird_has_passed(self, bird_rect: pygame.Rect) -> bool:
        """Returns True the first time the bird's right edge clears the pipe."""
        if not self.passed and bird_rect.right > self.x + PIPE_WIDTH:
            self.passed = True
            return True
        return False


class PipeManager:
    """Spawns, scrolls, and culls pipes; handles collision and scoring."""

    def __init__(self) -> None:
        self.pipes: list[Pipe] = []
        self._spawn_timer: int = 0

    def reset(self) -> None:
        self.pipes.clear()
        self._spawn_timer = 0

    def update(self, dt_ms: int) -> None:
        self._spawn_timer += dt_ms
        if self._spawn_timer >= PIPE_INTERVAL:
            self._spawn_timer = 0
            self.pipes.append(Pipe(WIDTH + 10))

        for pipe in self.pipes:
            pipe.update()

        self.pipes = [p for p in self.pipes if not p.is_off_screen()]

    def check_collision(self, hitbox: pygame.Rect) -> bool:
        return any(p.collides_with(hitbox) for p in self.pipes)

    def check_passed(self, bird_rect: pygame.Rect) -> int:
        """Returns number of pipes the bird passed this frame (0 or 1)."""
        return sum(1 for p in self.pipes if p.bird_has_passed(bird_rect))
