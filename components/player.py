import pygame

class Player:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, screen_width):
        # mouse_x, _ = pygame.mouse.get_pos()
        # self.x = mouse_x - self.width // 2
        # if self.x < 0:
        #     self.x = 0
        # elif self.x + self.width > screen_width:
        #     self.x = screen_width - self.width
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        
        # Ensure the player stays within the screen bounds
        self.x = max(0, min(self.x, screen_width - self.width))
