import pygame

class Score:
    def __init__(self, x, y, font_size=30, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.color = color
        self.score = 0
        self.font = pygame.font.Font(None, font_size)

    def increase(self):
        self.score += 1

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, self.color)
        screen.blit(score_text, (self.x, self.y))
