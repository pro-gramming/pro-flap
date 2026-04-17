import pygame
from game.constants import (
    BIRD_WIDTH, BIRD_HEIGHT, BIRD_X, BIRD_HITBOX_SHRINK,
    GRAVITY, FLAP_STRENGTH, MAX_FALL_SPEED, HEIGHT, GROUND_HEIGHT,
)


class Bird:
    """Player-controlled bird: physics, state, and collision geometry."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        start_y = HEIGHT // 2 - BIRD_HEIGHT // 2
        self.rect = pygame.Rect(BIRD_X, start_y, BIRD_WIDTH, BIRD_HEIGHT)
        self.vel_y: float = 0.0
        self.alive: bool = True
        self.angle: float = 0.0  # visual tilt in degrees (positive = nose down)

    def flap(self) -> None:
        if self.alive:
            self.vel_y = FLAP_STRENGTH

    def update(self) -> None:
        if not self.alive:
            # Dead bird still falls
            self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)
            self.rect.y += int(self.vel_y)
            self.angle = 90.0
            return

        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)
        self.rect.y += int(self.vel_y)

        # Clamp to ceiling
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0.0

        # Visual tilt: nose-up when rising, nose-down when falling
        if self.vel_y < 0:
            self.angle = max(self.angle - 6, -25)
        else:
            self.angle = min(self.angle + 4, 90)

        # Ground collision kills the bird
        ground_top = HEIGHT - GROUND_HEIGHT
        if self.rect.bottom >= ground_top:
            self.rect.bottom = ground_top
            self.alive = False

    def get_hitbox(self) -> pygame.Rect:
        """Slightly inset rect for more forgiving collision detection."""
        s = BIRD_HITBOX_SHRINK
        return self.rect.inflate(-s * 2, -s * 2)
