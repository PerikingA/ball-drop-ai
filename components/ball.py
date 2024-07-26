import pygame

class Ball:
    def __init__(self, x, y, width, color, speed_x, speed_y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.width = width
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.width))

    def move(self):
        self.y += self.speed_y

    def collides_with(self, player):
        ball_rect = pygame.Rect(self.x, self.y, self.width, self.width)
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        return ball_rect.colliderect(player_rect)

    def is_off_screen(self):
        return self.y > self.screen_height
