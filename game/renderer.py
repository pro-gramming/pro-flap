from __future__ import annotations

import math
import pygame
from game.constants import (
    WIDTH, HEIGHT, GROUND_HEIGHT,
    PIPE_WIDTH,
    BIRD_HEIGHT,
    SKY_TOP, SKY_BOTTOM,
    PIPE_COLOR, PIPE_EDGE,
    GROUND_COLOR, GROUND_EDGE,
    BIRD_BODY, BIRD_EYE, BIRD_PUPIL, BIRD_BEAK, BIRD_WING,
    TEXT_COLOR, SHADOW_COLOR,
)
from game.bird import Bird
from game.pipe import PipeManager
from game.ground import Ground
from game.score import Score


class Renderer:
    """Owns all pygame.draw calls. Stateless — receives game objects per frame."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font_large = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 32)

    # ------------------------------------------------------------------
    # Public draw methods
    # ------------------------------------------------------------------

    def draw_frame(
        self,
        bird: Bird,
        pipe_manager: PipeManager,
        ground: Ground,
        score: Score,
        state,  # GameState — avoid circular import with string annotation
    ) -> None:
        from game.state import GameState

        self._draw_background()
        self._draw_pipes(pipe_manager)
        self._draw_ground(ground)
        self._draw_bird(bird)
        self._draw_score(score.current)

        if state == GameState.MENU:
            self._draw_menu()
        elif state == GameState.GAME_OVER:
            self._draw_game_over(score)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _draw_background(self) -> None:
        # Vertical gradient sky
        for y in range(HEIGHT - GROUND_HEIGHT):
            t = y / (HEIGHT - GROUND_HEIGHT)
            r = int(SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * t)
            g = int(SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * t)
            b = int(SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * t)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))

    def _draw_pipes(self, pipe_manager: PipeManager) -> None:
        for pipe in pipe_manager.pipes:
            for rect in (pipe.top_rect, pipe.bottom_rect):
                pygame.draw.rect(self.screen, PIPE_COLOR, rect, border_radius=4)
                # Edge highlight on left side
                pygame.draw.rect(self.screen, PIPE_EDGE, rect, width=3, border_radius=4)
                # Cap
                cap_height = 16
                if rect == pipe.top_rect:
                    cap = pygame.Rect(rect.x - 4, rect.bottom - cap_height, PIPE_WIDTH + 8, cap_height)
                else:
                    cap = pygame.Rect(rect.x - 4, rect.top, PIPE_WIDTH + 8, cap_height)
                pygame.draw.rect(self.screen, PIPE_COLOR, cap, border_radius=4)
                pygame.draw.rect(self.screen, PIPE_EDGE, cap, width=3, border_radius=4)

    def _draw_ground(self, ground: Ground) -> None:
        ground_rect = ground.get_rect()
        pygame.draw.rect(self.screen, GROUND_COLOR, ground_rect)
        # Top edge stripe
        pygame.draw.rect(self.screen, GROUND_EDGE, pygame.Rect(0, ground_rect.top, WIDTH, 4))
        # Scrolling grass tufts
        tuft_spacing = 40
        tuft_y = ground_rect.top + 6
        for i in range(-1, WIDTH // tuft_spacing + 2):
            x = (i * tuft_spacing - ground.offset) % (WIDTH + tuft_spacing) - tuft_spacing // 2
            pygame.draw.ellipse(self.screen, GROUND_EDGE, pygame.Rect(x, tuft_y, 18, 8))

    def _draw_bird(self, bird: Bird) -> None:
        rect = bird.rect
        cx, cy = rect.centerx, rect.centery
        angle_rad = math.radians(-bird.angle)

        def rot(dx: float, dy: float):
            """Rotate a point around the bird centre by bird.angle."""
            rx = dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
            ry = dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
            return (cx + rx, cy + ry)

        # Wing (drawn behind body)
        wing_pts = [rot(-4, 6), rot(-14, 10), rot(-10, -2)]
        pygame.draw.polygon(self.screen, BIRD_WING, wing_pts)

        # Body ellipse approximated by a circle
        radius = BIRD_HEIGHT // 2
        pygame.draw.circle(self.screen, BIRD_BODY, (cx, cy), radius)

        # Eye
        eye_pos = rot(5, -4)
        pygame.draw.circle(self.screen, BIRD_EYE, (int(eye_pos[0]), int(eye_pos[1])), 5)
        pygame.draw.circle(self.screen, BIRD_PUPIL, (int(eye_pos[0]) + 1, int(eye_pos[1])), 3)

        # Beak
        beak_pts = [rot(9, 1), rot(16, 3), rot(9, 6)]
        pygame.draw.polygon(self.screen, BIRD_BEAK, beak_pts)

    def _draw_score(self, current: int) -> None:
        self._draw_text(str(current), self.font_large, TEXT_COLOR, WIDTH // 2, 60, shadow=True)

    def _draw_menu(self) -> None:
        self._draw_text("FLAPPY BIRD", self.font_medium, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 60, shadow=True)
        self._draw_text("Press SPACE or TAP to start", self.font_small, TEXT_COLOR, WIDTH // 2, HEIGHT // 2, shadow=True)

    def _draw_game_over(self, score: Score) -> None:
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        self._draw_text("GAME OVER", self.font_medium, (255, 80, 80), WIDTH // 2, HEIGHT // 2 - 80, shadow=True)
        self._draw_text(f"Score: {score.current}", self.font_medium, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 20, shadow=True)
        self._draw_text(f"Best:  {score.best}", self.font_small, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 30, shadow=True)
        self._draw_text("SPACE / TAP to restart", self.font_small, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 80, shadow=True)

    def _draw_text(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple,
        cx: int,
        cy: int,
        shadow: bool = False,
    ) -> None:
        if shadow:
            shadow_surf = font.render(text, True, SHADOW_COLOR)
            shadow_rect = shadow_surf.get_rect(center=(cx + 2, cy + 2))
            self.screen.blit(shadow_surf, shadow_rect)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(cx, cy))
        self.screen.blit(surf, rect)
