# Screen
WIDTH: int = 400
HEIGHT: int = 600
FPS: int = 60

# Physics
GRAVITY: float = 0.5
FLAP_STRENGTH: float = -9.0
MAX_FALL_SPEED: float = 12.0

# Pipes
PIPE_SPEED: int = 3
PIPE_GAP: int = 160        # vertical gap between top and bottom pipe
PIPE_INTERVAL: int = 1500  # ms between pipe spawns
PIPE_WIDTH: int = 60
PIPE_MIN_HEIGHT: int = 60  # minimum visible pipe height

# Ground
GROUND_HEIGHT: int = 80

# Bird
BIRD_WIDTH: int = 34
BIRD_HEIGHT: int = 24
BIRD_X: int = 80           # fixed horizontal position
BIRD_HITBOX_SHRINK: int = 4  # px inset on each side for forgiving collision

# Colors
SKY_TOP    = (112, 197, 206)
SKY_BOTTOM = (161, 218, 227)
PIPE_COLOR = (106, 190, 48)
PIPE_EDGE  = (84,  156, 36)
GROUND_COLOR = (222, 216, 149)
GROUND_EDGE  = (189, 174,  84)
BIRD_BODY  = (255, 215,   0)
BIRD_EYE   = (255, 255, 255)
BIRD_PUPIL = (0,     0,   0)
BIRD_BEAK  = (255, 140,   0)
BIRD_WING  = (255, 180,   0)
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0)
OVERLAY_COLOR = (0, 0, 0, 140)  # RGBA for semi-transparent overlay
