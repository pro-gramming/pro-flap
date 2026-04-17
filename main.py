"""
Flappy Bird — main entry point.

Runs natively:   python main.py
Runs in browser: python -m pygbag main.py  (then open localhost:8000)

The asyncio game loop is required by pygbag so the WASM runtime can yield
control back to the browser between frames.
"""

import asyncio
import pygame

from game.constants import WIDTH, HEIGHT, FPS
from game.state import GameState
from game.bird import Bird
from game.pipe import PipeManager
from game.ground import Ground
from game.score import Score
from game.renderer import Renderer


def _handle_action(state: GameState, bird: Bird, pipe_manager: PipeManager,
                   ground: Ground, score: Score) -> GameState:
    """Process a 'flap / start / restart' action. Returns the new state."""
    if state == GameState.MENU:
        bird.reset()
        pipe_manager.reset()
        ground.reset()
        score.reset()
        bird.flap()
        return GameState.PLAYING

    if state == GameState.PLAYING:
        bird.flap()
        return GameState.PLAYING

    if state == GameState.GAME_OVER:
        bird.reset()
        pipe_manager.reset()
        ground.reset()
        score.reset()
        bird.flap()
        return GameState.PLAYING

    return state


async def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird = Bird()
    pipe_manager = PipeManager()
    ground = Ground()
    score = Score()
    renderer = Renderer(screen)
    state = GameState.MENU

    while True:
        dt_ms = clock.tick(FPS)

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # no sys.exit() for pygbag compatibility

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = _handle_action(state, bird, pipe_manager, ground, score)

            if event.type == pygame.MOUSEBUTTONDOWN:
                state = _handle_action(state, bird, pipe_manager, ground, score)

        # --- Update ---
        if state == GameState.PLAYING:
            bird.update()
            ground.update()
            pipe_manager.update(dt_ms)

            # Score: count pipes passed
            passed = pipe_manager.check_passed(bird.rect)
            for _ in range(passed):
                score.increment()

            # Collision → game over
            if not bird.alive or pipe_manager.check_collision(bird.get_hitbox()):
                bird.alive = False
                state = GameState.GAME_OVER

        elif state == GameState.MENU:
            ground.update()  # ground scrolls on menu for liveliness

        # --- Render ---
        renderer.draw_frame(bird, pipe_manager, ground, score, state)
        pygame.display.flip()

        # Yield to the browser's event loop (required by pygbag)
        await asyncio.sleep(0)


asyncio.run(main())
