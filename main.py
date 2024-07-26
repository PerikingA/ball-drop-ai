import pygame
import sys
from components.player import Player
from components.ball import Ball
from components.settings import INITIAL_BALL_SPEED_Y, BALL_SPEED_INCREASE_AMOUNT, BALL_SPEED_INCREASE_INTERVAL, BALL_SPAWN_INTERVAL, GAME_DURATION, PREPARATION_TIME
from components.score import Score
import time
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1200, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Ball Drop AI')

# Set up the clock
clock = pygame.time.Clock()

# Font settings for score and timer
font_size = 50
font = pygame.font.Font(None, font_size)

def reset_game():
    global player, balls, score, ball_speed_y, last_ball_time, last_speed_increase_time, start_time, preparation_start_time, countdown_timer, game_started
    player = Player(x=width // 2, y=height - 50, width=90, height=25, color=(255, 0, 0), speed=5)
    balls = []
    score = Score(x=width - 150, y=10, font_size=font_size, color=(255, 255, 255))
    ball_speed_y = INITIAL_BALL_SPEED_Y
    last_ball_time = time.time()
    last_speed_increase_time = time.time()
    start_time = time.time()
    preparation_start_time = time.time()
    countdown_timer = GAME_DURATION
    game_started = False

reset_game()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and countdown_timer <= 0:
            reset_game()

    current_time = time.time()

    if not game_started:
        if current_time - preparation_start_time >= PREPARATION_TIME:
            game_started = True
            start_time = current_time  # Reset start time for countdown
        else:
            # Show prep message
            screen.fill((0, 0, 0))  
            text = font.render("Get Ready!", True, (255, 255, 255))
            screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
            pygame.display.flip()
            clock.tick(60)
            continue  

    # Update countdown timer
    elapsed_game_time = current_time - start_time
    countdown_timer = max(0, GAME_DURATION - int(elapsed_game_time))

    # Move player
    player.move(width)

    # Check if it's time to add a new ball
    if current_time - last_ball_time >= BALL_SPAWN_INTERVAL:
        new_ball = Ball(
            x=random.randint(0, width - 40),  # Random x position within screen width
            y=0,  # Start at the top of the screen
            width=40,
            color=(0, 0, 255),
            speed_x=0,  # No horizontal movement
            speed_y=ball_speed_y,  # Set the speed of falling
            screen_width=width,
            screen_height=height
        )
        balls.append(new_ball)
        last_ball_time = current_time

    # Check if it's time to increase ball speed
    if current_time - last_speed_increase_time >= BALL_SPEED_INCREASE_INTERVAL:
        ball_speed_y += BALL_SPEED_INCREASE_AMOUNT
        last_speed_increase_time = current_time

    # Move and draw balls
    screen.fill((0, 0, 0)) 
    balls_to_remove = []
    for ball in balls:
        ball.move()
        if ball.collides_with(player):
            if countdown_timer > 0:
                score.increase()
            balls_to_remove.append(ball)
        elif ball.is_off_screen():
            balls_to_remove.append(ball)
        else:
            ball.draw(screen)

    # Remove balls that collided with the player or went off screen
    for ball in balls_to_remove:
        balls.remove(ball)

    # Draw player
    player.draw(screen)

    # Draw score
    score.draw(screen)

    # Draw countdown timer
    timer_text = font.render(f"Time: {countdown_timer}", True, (255, 255, 255))
    screen.blit(timer_text, (width - timer_text.get_width() - 10, 50))

    # Update display
    pygame.display.flip()

    # End the game if time is up
    if countdown_timer <= 0:
        # Show game over message and wait for space to restart or quit
        screen.fill((0, 0, 0))  # Black
        
        score.draw(screen)
        
        # Draw game over message
        game_over_text = font.render("Game Over! Press SPACE to Restart or ESC to Quit", True, (255, 255, 255))
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2 + font_size))
        
        pygame.display.flip()
        
        # Wait for user input for restarting or quitting
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if (
                    event.type != pygame.QUIT
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
                ):
                    reset_game()
                    waiting = False
                elif (
                    event.type != pygame.QUIT
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                    or event.type == pygame.QUIT
                ):
                    waiting = False
                    running = False

# Quit Pygame
pygame.quit()
sys.exit()
