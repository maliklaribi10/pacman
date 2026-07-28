import pygame

def display_score():
    current_score = (pygame.time.get_ticks() - start) // 1000
    score_surface = test_font.render(f"Score: {current_score}", False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rectangle)
    return current_score

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner") # permet de changer le nom de la fenetre de jeu
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50) # nouvelle police d'ecriture et nouvelle taille de texte
game_active = False
start = pygame.time.get_ticks()
score = 0
choice = 0

# test_surface = pygame.Surface((100, 200)) # la surface que l'on veut rajouter de largeur 100 et de hauteur 200
# test_surface.fill("Red") # Remplir la surface de rouge

sky_surface = pygame.image.load("graphics/Sky.png").convert() # ajouter une image. Le convert sert a convertir tes image en une extention pygame prefere et facile dutilisation pour lui
ground_surface = pygame.image.load("graphics/ground.png").convert()

# text_surface = test_font.render("My game", False, (64,64,64)) # permet de creer une surface ou il y a du texte
# text_rectangle = text_surface.get_rect(center = (400, 50))

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rectangle = snail_surface.get_rect(midbottom = (600, 300))

player_surface = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (80, 300)) # tu prend ta surface du joueur et tu creer un rectangle autour de lui, puis tu lui dis grace a quoi tu veux le placer ici cest en bas au milieu du coup cest grace a la position en bas au milieu quon va placer le bonhomme
player_gravity = 0

# player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
# player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
# player_stand_rectangle = player_stand.get_rect(center = (400, 200))

title_surface = test_font.render("Astronauts Game", False, (64, 64, 64))
title_rectangle = title_surface.get_rect(center = (400, 50))

start_surface = test_font.render("Start Game", False, (64, 64, 64))
start_rectangle = start_surface.get_rect(center = (400, 100))

option_surface = test_font.render("Options", False, (64, 64, 64))
option_rectangle = option_surface.get_rect(center = (400, 200))

restart_surface = test_font.render("Press SPACE to run", False, (64, 64, 64))
restart_rectangle = restart_surface.get_rect(center = (400, 330))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rectangle.bottom == 300:
                if player_rectangle.collidepoint(event.pos):
                    player_gravity = -20
            if event.type == pygame.KEYDOWN and player_rectangle.bottom == 300:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN:
                if choice == 0:
                    if event.key == pygame.K_UP:
                        choice = 0
                    if event.key == pygame.K_DOWN:
                        choice = -1
                elif choice == -1:
                    if event.key == pygame.K_UP:
                        choice = 0
                    if event.key == pygame.K_DOWN:
                        choice = -2
                elif choice == -2:
                    if event.key == pygame.K_UP:
                        choice = -1
                    if event.key == pygame.K_DOWN:
                        choice = -3
                elif choice == -3:
                    if event.key == pygame.K_UP:
                        choice = -2
                    if event.key == pygame.K_DOWN:
                        choice = -3

                if choice == 0 and event.key == pygame.K_RETURN:
                    snail_rectangle.midbottom = (600, 300)
                    player_rectangle.midbottom = (80, 300)
                    game_active = True
                    start = pygame.time.get_ticks()


    if game_active:
        screen.blit(sky_surface, (0, 0)) # permet d'integrer la nouvelle surface a notre display: tu prend le coin gauche de notre surface et tu la place de (width, height) par rapport a notre screen
        screen.blit(ground_surface, (0, 300))
        # pygame.draw.rect(screen, "#c0e8ec", text_rectangle)
        # pygame.draw.rect(screen, "#c0e8ec", text_rectangle, 10)
        score = display_score()
        # screen.blit(text_surface, text_rectangle)

        snail_rectangle.x -= 4 # tu prend la position x de ton rectangle et tu enleve 4 pixel
        if snail_rectangle.right <= 0: 
            snail_rectangle.left = 800
        screen.blit(snail_surface, snail_rectangle)

        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300:
            player_rectangle.bottom = 300
        screen.blit(player_surface, player_rectangle)
        if snail_rectangle.colliderect(player_rectangle):
            game_active = False
    else:
        screen.fill((94, 129, 162))
        # screen.blit(player_stand, player_stand_rectangle)
        if choice == 0:
            pygame.draw.rect(screen, "Red", start_rectangle, 1)
        if choice == -1:
            pygame.draw.rect(screen, "Red", start_rectangle, -1)
            pygame.draw.rect(screen, "Red", option_rectangle, 1)
        screen.blit(start_surface, start_rectangle)
        screen.blit(option_surface, option_rectangle)
        score_message = test_font.render(f"Your score:  {score}", False, (64, 64, 64))
        score_message_rectangle = score_message.get_rect(center = (400, 330))
        screen.blit(title_surface, title_rectangle)
        if score == 0:
            screen.blit(restart_surface, restart_rectangle)
        else:
            screen.blit(score_message, score_message_rectangle)

    
    # if player_rectangle.colliderect(snail_rectangle):
    #     print("ERROOOOOR")

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rectangle.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())

    pygame.display.update()  # sert à mettre à jour la fenêtre de jeu pour que les modifications que tu as dessinées deviennent visibles à l'écran
    clock.tick(60) # permet de dire a pygame que ta boucle ne doit pas s'executer plus de 60 fois par secondes FPS
