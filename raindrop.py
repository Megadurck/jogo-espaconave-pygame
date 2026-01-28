import pygame
from pygame.sprite import Sprite
import random

class Raindrop(Sprite):
    """Uma classe que representa uma gota de chuva."""

    def __init__(self, ai_settings, screen):
        """Inicializa a gota de chuva e define sua posição inicial."""
        super(Raindrop, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Carrega a imagem da gota de chuva e define seu atributo rect
        self.image = pygame.image.load('img/raindrop.png')
        self.rect = self.image.get_rect()

        #Inicia cada nova gota de chuva em uma posição aleatória na parte superior da tela
        self.rect.x = random.randint(0, ai_settings.screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)

        #Armazena a posição exata da gota de chuva
        self.y = float(self.rect.y)
    
    def blitme(self):
        """Desenha a gota de chuva em sua posição atual."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move a gota de chuva para baixo."""
        self.y += self.ai_settings.raindrop_speed_factor
        self.rect.y = self.y