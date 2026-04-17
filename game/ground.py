import pygame
from game.constants import WIDTH, HEIGHT, GROUND_HEIGHT, PIPE_SPEED


class Ground:
    """Scrolling ground strip at the bottom of the screen."""

    def __init__(self) -> None:
        self.offset: int = 0
        self.y: int = HEIGHT - GROUND_HEIGHT
        self.rect = pygame.Rect(0, self.y, WIDTH, GROUND_HEIGHT)

    def update(self) -> None:
        self.offset = (self.offset + PIPE_SPEED) % WIDTH

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def reset(self) -> None:
        self.offset = 0
