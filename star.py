import pygame
import random

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, size=2):
        super().__init__()

        self.image = pygame.Surface((size, size))
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        # piscar ocasional
        if random.random() < 0.005:
            brightness = random.randint(180, 255)
            self.image.fill((brightness, brightness, brightness))
