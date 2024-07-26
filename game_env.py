import pygame
import numpy as np
from components.player import Player
from components.ball import Ball
from components.settings import PLAYER_SPEED, INITIAL_BALL_SPEED_Y, BALL_SPEED_INCREASE_AMOUNT, BALL_SPEED_INCREASE_INTERVAL, BALL_SPAWN_INTERVAL, GAME_DURATION

class GameEnv:
    def __init__(self):
        self.width = 1200
        self.height = 750
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Ball Drop AI')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        
        # Reset the game environment to the initial state
        self.player = Player(x=self.width // 2, y=self.height - 50, width=90, height=25, color=(255, 0, 0), speed=PLAYER_SPEED)
        self.balls = []
        self.score = 0
        self.ball_speed_y = INITIAL_BALL_SPEED_Y
        self.last_ball_time = pygame.time.get_ticks() / 1000
        self.last_speed_increase_time = pygame.time.get_ticks() / 1000
        self.start_time = pygame.time.get_ticks() / 1000
        self.countdown_timer = GAME_DURATION
        
        return self.get_state()

    def get_state(self):
        # Initialize ball positions
        ball_positions = [0] * 100  # 50 balls * 2 coordinates (x, y)
        
        # Fill ball positions
        for i, ball in enumerate(self.balls[:50]):  # Consider up to 50 balls
            ball_positions[2 * i] = ball.x / self.width
            ball_positions[2 * i + 1] = ball.y / self.height
        
        # Normalize the player position, ball speed, and countdown timer
        return np.array([
            self.player.x / self.width,           
            *ball_positions,                      
            self.ball_speed_y / 10.0,          
            self.countdown_timer / GAME_DURATION   
        ])


    def step(self, action):
        reward = 0
        # Apply the action and update the environment
        if action == 0:
            self.player.x -= self.player.speed  # Move left
        elif action == 1:
            self.player.x += self.player.speed  # Move right

        self.player.x = np.clip(self.player.x, 0, self.width - self.player.width)
        
        current_time = pygame.time.get_ticks() / 1000  # Convert to seconds
        
        # Update countdown timer
        elapsed_game_time = current_time - self.start_time
        self.countdown_timer = max(0, GAME_DURATION - int(elapsed_game_time))

        if self.countdown_timer <= 0:
            return self.get_state(), 0, True  # Game over

        # Update balls
        balls_to_remove = []
        
        for ball in self.balls:
            ball.move()
            if ball.collides_with(self.player):
                self.score += 1
                reward += 1  # Reward for catching a ball
                balls_to_remove.append(ball)
            elif ball.is_off_screen():
                reward -= 1  # Penalty for missing a ball
                balls_to_remove.append(ball)
        
        for ball in balls_to_remove:
            self.balls.remove(ball)

        # Check if it's time to add a new ball
        if (current_time - self.last_ball_time) >= BALL_SPAWN_INTERVAL:
            new_ball = Ball(
                x=np.random.randint(0, self.width - 40),
                y=0,
                width=40,
                color=(0, 0, 255),
                speed_x=0,
                speed_y=self.ball_speed_y,
                screen_width=self.width,
                screen_height=self.height
            )
            self.balls.append(new_ball)
            self.last_ball_time = current_time

        # Check if it's time to increase ball speed
        if current_time - self.last_speed_increase_time >= BALL_SPEED_INCREASE_INTERVAL:
            self.ball_speed_y += BALL_SPEED_INCREASE_AMOUNT
            self.last_speed_increase_time = current_time
        
        return self.get_state(), reward, False

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.player.draw(screen)
        for ball in self.balls:
            ball.draw(screen)
        pygame.display.flip()
