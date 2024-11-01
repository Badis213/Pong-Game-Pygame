# Game settings
WIDTH = 800  # Width of the game window
HEIGHT = 600  # Height of the game window
BLACK = (0, 0, 10)  # Dark background for a space feel
WHITE = (255, 255, 255)  # Bright white for visibility
PADDING = 30  # Space between the sides of the screen and the paddles (in pixels)
Y_CENTER = HEIGHT // 2  # Center of the screen in Y axis
X_CENTER = WIDTH // 2
FPS = 60 # Frame per seconds

# Paddle settings
PADDLE_WIDTH = 10  # Width of each paddle
PADDLE_HEIGHT = 100  # Height of each paddle
PADDLE_SPEED = 10

# Left paddle position
L_PADDLE_X = PADDING  # X position of the left paddle
L_PADDLE_Y = Y_CENTER - PADDLE_HEIGHT // 2  # Y starting position of the left paddle

# Right paddle position
R_PADDLE_X = WIDTH - PADDING - PADDLE_WIDTH  # X position of the right paddle
R_PADDLE_Y = Y_CENTER - PADDLE_HEIGHT // 2 # Y starting position of the right paddle

# Ball settings
BALL_DIAMETER = 20
BALL_RADIUS = BALL_DIAMETER // 2
BALL_SPEED = 10

# Ball starting position
BALL_X = X_CENTER
BALL_Y = Y_CENTER