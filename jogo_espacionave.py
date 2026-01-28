import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from starfild import StarField
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

#Inicializa o jogo e cria um objeto para a tela
def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #Cria o botão Play
    play_button = Button(ai_settings, screen, "Play")
    
    #Cria uma espaçonave
    ship = Ship(ai_settings, screen)
    #Cria um grupo no qual serão armazenados os projéteis
    bullets = Group()
    #cria o grupo de alienígenas
    aliens = Group()
    #cria a frota de alienígenas
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #Cria o campo de estrelas
    star_field = StarField(ai_settings)

    #cria as gotas de chuva
    raindrops = Group()
    gf.create_raindrop(ai_settings, screen, raindrops)

    #Cria as estatísticas do jogo
    stats = GameStats(ai_settings)

    #Cria o placar
    sb = Scoreboard(ai_settings, screen, stats)
    
    #Inicia o laço principal do jogo
    while True:
        #observa eventos de teclado e de mause
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_raindrops(raindrops, ai_settings)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, star_field, raindrops, play_button)
        star_field.stars.update()
if __name__ == "__main__":
    run_game()