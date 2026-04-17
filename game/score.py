class Score:
    """Tracks current score and session-best high score."""

    def __init__(self) -> None:
        self.current: int = 0
        self.best: int = 0

    def increment(self) -> None:
        self.current += 1
        if self.current > self.best:
            self.best = self.current

    def reset(self) -> None:
        self.current = 0
