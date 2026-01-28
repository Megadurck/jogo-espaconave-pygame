import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    
    def __init__(self, ai_settings, screen):
        """Inicializa a espaçonave e define sua posição inicial"""
        super(Ship, self).__init__()
        
        self.screen = screen
        self.ai_settings = ai_settings
        
        #Carrega a imagem da espaçonave e obtém seu rect
        self.image = pygame.image.load("img/ship1.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #Inicia cada nova espaçonave na parte inferior central da tela
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Armazena um valor decimal para o centro da espaçonave
        self.center = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        
        # Flag de movimento
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    
    def update(self):
        """Atualiza a posição da espaçonave de acordo com a flag demovimento."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor 
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        # movimento horizontal
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
        
            
        # Atualiza o objeto rect de acordo com self.center
        self.rect.centerx = self.center
        self.rect.centery = self.centery

    def blitme(self):
        """Desenha a espaçonave em sua posição atual"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Centraliza a espaçonave na tela"""
        self.center = self.screen_rect.centerx
        self.centery = self.screen_rect.bottom - 50
        