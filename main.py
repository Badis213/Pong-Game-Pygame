import pygame as pg
from settings import *
import os
from math import cos, sin, pi
from random import choice

# key mapping
UP_KEY = pg.K_UP
DOWN_KEY = pg.K_DOWN
Z_KEY = pg.K_z
S_KEY = pg.K_s
R_KEY = pg.K_r
ESC_KEY = pg.K_ESCAPE

# pygame setup
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Pong Game")

# init mixer
pg.mixer.init()

# set icon
current_dir = os.path.dirname(__file__)  # Gets the directory of the current script
icon_path = os.path.join(current_dir, 'Assets', 'ping-pong.png')  # Constructs the relative path
icon = pg.image.load(icon_path)  # Load the image
pg.display.set_icon(icon)

# init font
font_path = f'{current_dir}\\Assets\\PressStart2P-Regular.ttf'  # Update with the path to your font file
font_size = 36
font = pg.font.Font(font_path, font_size)  # Load the pixel-style font

# init sounds
hit_sound = pg.mixer.Sound(f'{current_dir}\\assets\\hit_sound.wav')
goal_sound = pg.mixer.Sound(f'{current_dir}\\assets\\goal.wav')


clock = pg.time.Clock()
running = True
end_screen = False
dt = 0

# Paddle class
class Paddle:
    def __init__(self, x, y, speed):
        self.position = [x, y] # Paddle position
        self.speed = speed # Paddle speed (in the y axis)
        self.rect = pg.Rect(self.position[0], self.position[1], PADDLE_WIDTH, PADDLE_HEIGHT)  # Rectangle for Paddle

    
    def check_collisions(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

    def movement(self, direction):
        if direction == 'UP':
            self.rect.y -= self.speed
        elif direction == 'DOWN':
            self.rect.y += self.speed

        self.check_collisions()

    def draw(self):
        pg.draw.rect(screen, WHITE, self.rect)


# Ball class
class Ball:
    def __init__(self, x, y, speed, radius):
        self.position = [x, y]
        self.speed = speed
        self.radius = radius
        self.diameter = radius * 2
        self.angle = choice([pi/4, (pi/4)+pi])
        self.rect = pg.Rect(x - radius, y - radius, self.diameter, self.diameter)
        
    def check_collisions(self, paddles):
        # Check for top collision
        if self.rect.top <= 0:
            self.rect.top = 0
            self.angle = -self.angle  # Reflect the angle
            hit_sound.play()
        # Check for bottom collision
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.angle = -self.angle  # Reflect the angle
            hit_sound.play()

        # Check for left collision
        if self.rect.left <= 0:
            self.rect.left = 0
            start_positions()
            score_update(player=2)
            goal_sound.play()
        # Check for right collision
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            start_positions()
            score_update(player=1)
            goal_sound.play()

        for paddle in paddles:
            if self.rect.colliderect(paddle):
                self.angle = pi - self.angle
                hit_sound.play()

    def movement(self):
        self.position[0] += self.speed * cos(self.angle)
        self.position[1] += self.speed * sin(self.angle)
        
        # update position with integers
        self.rect.center = (int(self.position[0]), int(self.position[1]))
        self.check_collisions([paddle_p1, paddle_p2])

    def draw(self):
        pg.draw.circle(screen, WHITE, self.rect.center, self.radius)

# create paddles and ball instances
paddle_p1 = Paddle(L_PADDLE_X, L_PADDLE_Y, PADDLE_SPEED)
paddle_p2 = Paddle(R_PADDLE_X, R_PADDLE_Y, PADDLE_SPEED)
ball = Ball(BALL_X, BALL_Y, BALL_SPEED, BALL_RADIUS)

# movement function
def keys_check():
    if keys[UP_KEY]:
        paddle_p2.movement('UP')
    elif keys[DOWN_KEY]:
        paddle_p2.movement('DOWN')
    if keys[Z_KEY]:
        paddle_p1.movement('UP')
    elif keys[S_KEY]:
        paddle_p1.movement('DOWN')


# score update
p1_score = 0
p2_score = 0
def score_update(player):
    global p1_score, p2_score, end_screen
    if player == 1:
        p1_score += 1
        if p1_score == 10:
            end_screen = True
    elif player == 2:
        p2_score += 1
        if p2_score == 10:
            end_screen = True

# Win text function
def draw_win_text(player):
    winner = "PLAYER 1" if player == 1 else "PLAYER 2"
    
    # Create a smaller font instance just for the win text
    small_font_size = 16  # Smaller font size for win text
    small_font = pg.font.Font(font_path, small_font_size)

    screen.fill(BLACK)

    # Render winner text
    win_text = font.render(f"{winner} WON", True, WHITE)
    text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))  # Center the text
    screen.blit(win_text, text_rect)

    # Render restart message
    restart_text = small_font.render("Press 'R' to Restart or 'ESC' to Quit", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))  # Center the text
    screen.blit(restart_text, restart_rect)

# Function to draw scores on the screen
def draw_score(score, font, x_position, y_position):
    text_surface = font.render(f"{score}", True, WHITE)  # Render the text
    screen.blit(text_surface, (x_position, y_position))  # Draw the text on the surface

# Function when goal
def start_positions():
    ball.position = [BALL_X, BALL_Y]
    paddle_p1.position = [L_PADDLE_X, L_PADDLE_Y]
    paddle_p2.position = [R_PADDLE_X, R_PADDLE_Y]
    ball.angle = choice([pi/4, (pi/4)+pi])

# GAME LOOP
while running:
    # poll the events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # handling keys
    keys = pg.key.get_pressed()
    keys_check()

    # fill the screen with the background color
    screen.fill(BLACK)

    # If end of the game
    if end_screen:
        # Draw win text
        draw_win_text(1 if p1_score == 10 else 2)
        pg.display.flip()  # Update the display

        # Check for restart or quit keys
        if keys[R_KEY]:  # Restart the game
            p1_score = 0
            p2_score = 0
            end_screen = False
            start_positions()  # Reset positions
            continue
        elif keys[ESC_KEY]:  # Quit the game
            running = False

        continue  

    # rendering the scene
    y_position = 20 # Fixed position from the top of the screen to the text
    p1_text_surface = font.render(f"{p1_score}", True, WHITE)  # Render Player 1's score
    p1_x_position = X_CENTER - p1_text_surface.get_width() - 30  # Position to the left of center
    draw_score(p1_score, font, p1_x_position, y_position)  # Draw score

    p2_text_surface = font.render(f"{p2_score}", True, WHITE)  # Render Player 2's score
    p2_x_position = X_CENTER + 30  # Position to the right of center
    draw_score(p2_score, font, p2_x_position, y_position)  # Draw score

    pg.draw.line(screen, WHITE, (X_CENTER, 0), (X_CENTER, HEIGHT))
    paddle_p1.draw()
    paddle_p2.draw()
    ball.movement()
    ball.draw()

    # Quit the game if esc
    if keys[ESC_KEY]:
        running = False

    # update the display
    pg.display.flip()

    # control the frame rate and calculate dt
    dt = clock.tick(FPS) / 1000 # controls fps and calculates dt (time in seconds since the last frame)

pg.quit()