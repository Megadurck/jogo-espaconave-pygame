#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Settings():
    """Uma classe para armazenar todas as configurações da Invasão Alienígena."""
    def __init__(self):
        """Inicializa as configurações do jogo."""
        #Configurações de tela
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (75, 80, 90)
        
        #Configurações~da espaçonave
        self.ship_limit = 2
        
        #Configurações dos projeteis 
        self.bullet_speed_factor = 4
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 0, 10, 10
        self.bullets_allowed = 10

        #Configurações dos alienígenas
        self.fleet_drop_speed = 10

        #A taxa com que a velocidade do jogo aumenta
        self.speedup_scale = 1.1

        #A taxa com que os pontos para cada alienígena aumentam
        self.score_scale = 1.5

        #Configurações das gotas de chuva
        self.raindrop_speed_factor = 1.2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicializa as configurações que mudam ao longo do jogo."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 5
        self.alien_speed_factor = 1

        #fleet_direction igual a 1 representa a direita; -1 representa a esquerda
        self.fleet_direction = 1

        #Pontuação
        self.alien_points = 50

    def increase_speed(self):
        """Aumenta as configurações de velocidade."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        #print(self.alien_points)

