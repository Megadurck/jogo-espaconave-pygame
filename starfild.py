from random import randint
import pygame
from star import Star

class StarField:
    def __init__(self, ai_settings):
        self.stars = pygame.sprite.Group()
        self._create_star_field(ai_settings)

    def _create_star_field(self, ai_settings):
        star_spacing = 40

        number_stars_x = ai_settings.screen_width // star_spacing
        number_rows = ai_settings.screen_height // star_spacing

        for row in range(number_rows):
            for col in range(number_stars_x):
                x = col * star_spacing + randint(-10, 10)
                y = row * star_spacing + randint(-10, 10)
                size = randint(1, 3)
                star = Star(x, y, size)
                self.stars.add(star)
