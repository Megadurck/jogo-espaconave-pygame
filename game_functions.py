#game_functions.py
import sys
import pygame
import random
from time import sleep
from bullet import Bullet # type: ignore
from alien import Alien # type: ignore
from starfild import StarField # type: ignore
from raindrop import Raindrop # type: ignore
from game_stats import GameStats # type: ignore

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_LEFT:
         ship.moving_left = True
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()    
def fire_bullet(ai_settings, screen, ship, bullets):
    # Cria um novo projétil e o adiciona ao grupo de projéteis
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
       
        
def check_keyup_events(event, ship):
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    #observa eventos de teclado e de mause
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event,ai_settings, screen, ship, bullets)
                    
            elif event.type == pygame.KEYUP:
                check_keyup_events(event, ship)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Inicia um novo jogo quando o jogador clicar em Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #reinicia as configurações do jogo
        ai_settings.initialize_dynamic_settings()
        #oculta o cursor do mouse
        pygame.mouse.set_visible(False)
        #Reinicia as estatísticas do jogo
        stats.reset_stats()
        stats.game_active = True

        #Reinicia os dados estaticos do jogo
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #Esvazia a lista de alienígenas e de projéteis
        aliens.empty()
        bullets.empty()

        #Cria uma nova frota e centraliza a espaçonave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

                

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, star_field, raindrops, play_button):
    """Atualiza as imagens na tela e alterna para a nova tela."""
    # Redesenha a tela a cada passagem pelo laço
    screen.fill(ai_settings.bg_color)
    #Cria o campo de estrelas
    star_field.stars.draw(screen)
    #desenha o placar
    sb.show_score()
    # Desenha as gotas de chuva
    for raindrop in raindrops.sprites():
        raindrop.blitme()
    # Redesenha todos os projéteis atrás da espaçonave e dos alienígenas
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    # Desenha os alienígenas
    aliens.draw(screen)

    # Desenha o botão Play se o jogo estiver inativo
    if not stats.game_active:
        play_button.draw_button()

    # Deixa a tela mais recente visível
    pygame.display.flip()
    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Atualiza a posição dos projéteis e se livra dos projéteis antigos'''
    #Atualiza as posições dos progéteis
    bullets.update()
    
    #livra-se dos projéteis que desapareceram
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):            
    #Verifica se algum projétil atingiu um alienígena
    colisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if colisions:
        for aliens in colisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb) 

    if len(aliens) == 0:
        #Destrói os projéteis existentes e cria uma nova frota
        bullets.empty()
        ai_settings.increase_speed()

        #Aumenta o nível
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

        

def get_number_aliens_x(ai_settings, alien_width):
    """Determina o número de alienígenas que cabem em uma linha."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determina o número de linhas de alienígenas que cabem na tela."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Cria um alienígena e o posiciona na linha."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Cria uma frota completa de alienígenas."""
    #Cria um alienígena e calcula o número de alienígenas em uma linha
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = 4  # Número fixo de linhas de alienígenas

    #Cria a frota de alienígenas
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Responde apropriadamente se algum alienígena alcançou uma borda."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Faz toda a frota descer e mudar a direção."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Verifica se algum alienígena alcançou a parte inferior da tela."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Trata esse caso do mesmo modo que se a espaçonave fosse atingida
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Verifica se a frota está na borda e atualiza a posição de todos os alienígenas."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #Verifica colisões entre alienígenas e a espaçonave
    if pygame.sprite.spritecollideany(ship, aliens):
        print("ship hit!")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    #Verifica se algum alienígena alcançou a parte inferior da tela
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def create_raindrop(ai_settings, screen, raindrops):
    """Cria uma gota de chuva e a adiciona ao grupo de gotas de chuva."""
    for _ in range(20):  # Cria 20 gotas de chuva
        raindrop = Raindrop(ai_settings, screen)
        raindrop.y = random.randint(-ai_settings.screen_height, ai_settings.screen_height)
        raindrop.rect.y = raindrop.y
        raindrops.add(raindrop)

def check_raindrop_edges(raindrop):
    """Verifica se a gota de chuva alcançou a borda inferior da tela."""
    screen_rect = raindrop.screen.get_rect()
    if raindrop.rect.top >= screen_rect.bottom:
        return True
    return False

def update_raindrops(raindrops, ai_settings):
    raindrops.update()

    for raindrop in raindrops.sprites():
        if check_raindrop_edges(raindrop):
            raindrop.y = random.randint(-100, -40)
            raindrop.rect.x = random.randint(
                0,
                ai_settings.screen_width - raindrop.rect.width
            )

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Reponde ao fato de a espaçonave ter sido atingida por um alienígena."""
    if stats.ships_left > 0:
        #Decrementa o número de espaçonaves restantes
        stats.ships_left -= 1
        #Atualiza o placar
        sb.prep_ships()
        #Esvazia a lista de alienígenas e de projéteis
        aliens.empty()
        bullets.empty()

        #Cria uma nova frota e centraliza a espaçonave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #Faz uma pausa
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_high_score(stats, sb):
    """Verifica se há uma nova pontuação máxima."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()