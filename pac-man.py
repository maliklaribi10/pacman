import pygame
from pygame.locals import QUIT, RESIZABLE
from mazegenerator import MazeGenerator
from typing import Self, Any
from random import randint, seed
import sys
import json
from time import time
from pydantic import Field, BaseModel, model_validator
import character as char


class Json(BaseModel):
    """Stocke et valide la configuration du jeu."""
    highscore_filename: str = Field(min_length=1, default="score.json")
    level: int = Field(ge=1, default=10)
    width: int = Field(default=20)
    height: int = Field(default=20)
    lives: int = Field(ge=1, default=5)
    pacgum: int = Field(ge=1)
    score_pacgum: int = Field(ge=1, default=10)
    score_superpacgum: int = Field(ge=1, default=50)
    score_ghost: int = Field(ge=1, default=200)
    seed: int = Field(ge=1, default=42)
    max_time: int = Field(ge=30, default=90)

    @model_validator(mode="after")
    def filename_validator(self) -> Self:
        """Vérifie le format du fichier de score.

        Raises:
            ValueError: Si le fichier n'est pas au format JSON.

        Returns:
            Self: La configuration validée.
        """
        if not self.highscore_filename.endswith(".json"):
            raise ValueError("Votre fichier doit absolument etre un .json")
        return self

    @model_validator(mode="after")
    def pacgum_validator(self) -> Self:
        """Vérifie le nombre de pac-gums.

        Raises:
            ValueError: Si le nombre de pac-gums est trop élevé.

        Returns:
            Self: La configuration validée.
        """
        if self.pacgum > self.width * self.height - 22:
            raise ValueError("Le nombre de pacgum est trop grand pour un labyrinthe de cette taille")
        return self


SCREEN_WIDTH = 1001
SCREEN_HEIGHT = 1050


def main_menu() -> None:
    """Affiche le menu principal."""
    title_surface = h1_font.render("Pac-Man", False, "Red")
    title_rectangle = title_surface.get_rect(center=(SCREEN_WIDTH/2, 200))

    start_game = font.render("Start Game", False, (64, 64, 64))
    start_game_rectangle = start_game.get_rect(center=(SCREEN_WIDTH/2, 500))

    instruction = font.render("Instructions", False, (64, 64, 64))
    instruction_rectangle = instruction.get_rect(center=(SCREEN_WIDTH/2, 600))

    highscore = font.render("Highscore", False, (64, 64, 64))
    highscore_rectangle = highscore.get_rect(center=(SCREEN_WIDTH/2, 700))

    sortie = font.render("Exit", False, (64, 64, 64))
    sortie_rectangle = sortie.get_rect(center=(SCREEN_WIDTH/2, 800))

    if choice == 0:
        start_game = font.render("Start Game", False, "Red")
        instruction = font.render("Instructions", False, (64, 64, 64))
        highscore = font.render("Highscore", False, (64, 64, 64))
        sortie = font.render("Exit", False, (64, 64, 64))
    if choice == -1:
        start_game = font.render("Start Game", False, (64, 64, 64))
        instruction = font.render("Instructions", False, "Red")
        highscore = font.render("Highscore", False, (64, 64, 64))
        sortie = font.render("Exit", False, (64, 64, 64))
    if choice == -2:
        start_game = font.render("Start Game", False, (64, 64, 64))
        instruction = font.render("Instructions", False, (64, 64, 64))
        highscore = font.render("Highscore", False, "Red")
        sortie = font.render("Exit", False, (64, 64, 64))
    if choice == -3:
        start_game = font.render("Start Game", False, (64, 64, 64))
        instruction = font.render("Instructions", False, (64, 64, 64))
        highscore = font.render("Highscore", False, (64, 64, 64))
        sortie = font.render("Exit", False, "Red")

    windows.fill("Yellow")
    windows.blit(start_game, start_game_rectangle)
    windows.blit(instruction, instruction_rectangle)
    windows.blit(title_surface, title_rectangle)
    windows.blit(highscore, highscore_rectangle)
    windows.blit(sortie, sortie_rectangle)


def flou(screen: pygame.Surface) -> pygame.Surface:
    """Applique un effet de flou à l'écran.

    Args:
        screen: Surface à flouter.

    Returns:
        pygame.Surface: Surface floutée.
    """
    screen_copy = screen.copy()

    small = pygame.transform.smoothscale(
        screen_copy,
        (screen.get_width() // 10, screen.get_height() // 10)
    )

    blurred = pygame.transform.smoothscale(
        small,
        screen.get_size()
    )

    return blurred


def highscore_screen(content: dict[str, Any]) -> None:
    """Affiche les meilleurs scores.

    Args:
        content: Dictionnaire contenant les scores.
    """
    cpt = 0
    highscore_backgroud_surf = pygame.Surface((800, 800))
    highscore_backgroud_rect = highscore_backgroud_surf.get_rect(center=(windows.get_width()/2, windows.get_height()/2))
    pygame.draw.rect(windows, "Black", highscore_backgroud_rect, border_radius=10)
    highscore_title_surf = h2_font.render("Highscore", False, "Yellow")
    highscore_title_rect = highscore_title_surf.get_rect(midtop=(windows.get_width()/2, windows.get_height()/2 - 390))
    windows.blit(highscore_title_surf, highscore_title_rect)
    quit_text = font_text.render("Press Q to exit", False, (64, 64, 64))
    quit_rect = quit_text.get_rect(midbottom=(windows.get_width()/2, windows.get_height()/2 + 390))
    timeing = pygame.time.get_ticks()
    if (timeing // 500) % 2 == 0:
        windows.blit(quit_text, quit_rect)
    try:
        with open(verif.highscore_filename, 'r') as f:
            content = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        pass
    if content == {}:
        no_score_recorded = font.render("No scores provided", False, "White")
        no_score_recorded_rect = no_score_recorded.get_rect(center=(windows.get_width()/2, windows.get_height()/2))
        windows.blit(no_score_recorded, no_score_recorded_rect)
    else:
        for i in content:
            cpt += 1
            if cpt > 10:
                break
            highscore_content_surf = font_text.render(f"{i} - {content[i]}", False, "White")
            highscore_content_rect = highscore_content_surf.get_rect(topleft=(windows.get_width()/2 - 70, windows.get_height()/2 - (230 - ((cpt * 50)))))
            windows.blit(highscore_content_surf, highscore_content_rect)
            if cpt == 1:
                windows.blit(gold_image, (windows.get_width()/2 - 130, windows.get_height()/2 - (230 - ((cpt * 50)))))
            elif cpt == 2:
                windows.blit(silver_image, (windows.get_width()/2 - 130, windows.get_height()/2 - (230 - ((cpt * 50)))))
            elif cpt == 3:
                windows.blit(bronze_image, (windows.get_width()/2 - 130, windows.get_height()/2 - (230 - ((cpt * 50)))))
            else:
                highscore_position_surf = font_text.render(f"{cpt}", False, "White")
                windows.blit(highscore_position_surf, (windows.get_width()/2 - 110, windows.get_height()/2 - (230 - ((cpt * 50)))))


def instruction_screen() -> None:
    """Affiche les instructions du jeu."""
    instruction_surf = pygame.image.load("image/instruction.png").convert_alpha()
    instruction_surf = pygame.transform.scale(instruction_surf, (800, 800))
    instruction_rect = instruction_surf.get_rect(center=(windows.get_width()/2, windows.get_height()/2))
    windows.blit(instruction_surf, instruction_rect)


def game_over_screen(blurred_background: pygame.Surface | None) -> pygame.Surface:
    """Affiche l'écran de défaite.

    Args:
        blurred_background: Arrière-plan déjà flouté ou pas.

    Returns:
        pygame.Surface: Arrière-plan flouté.
    """
    victory = pygame.image.load("image/game over.png").convert_alpha()
    if blurred_background is None:
        blurred_background = flou(windows)

    windows.blit(blurred_background, (0, 0))
    load_images_gameover_victory(victory, score, "Red")
    name_user_surf = font.render(f"{name_user}", False, (64, 64, 64))
    windows.blit(name_user_surf, (170, 450))
    if len(name_user) < 1 and pressed >= 1:
        error_message_surf = font_text.render("Please enter a minimum of 1 caracter", False, "Red")
        error_message_rect = error_message_surf.get_rect(center=(windows.get_width()/2, 600))
        windows.blit(error_message_surf, error_message_rect)
    pygame.display.update()
    return blurred_background


def victory_screen(blurred_background: pygame.Surface | None) -> pygame.Surface:
    """Affiche l'écran de défaite.

    Args:
        blurred_background: Arrière-plan déjà flouté ou pas.

    Returns:
        pygame.Surface: Arrière-plan flouté.
    """
    victory = pygame.image.load("image/victory.png").convert_alpha()
    if blurred_background is None:
        blurred_background = flou(windows)

    windows.blit(blurred_background, (0, 0))
    load_images_gameover_victory(victory, score, "Yellow")
    name_user_surf = font.render(f"{name_user}", False, (64, 64, 64))
    windows.blit(name_user_surf, (170, 450))
    pygame.display.update()
    return blurred_background


def pause_screen(blurred_background: pygame.Surface | None) -> pygame.Surface:
    """Affiche le menu pause.

    Args:
        blurred_background: Arrière-plan déjà flouté ou pas.

    Returns:
        pygame.Surface: Arrière-plan flouté.
    """
    resume = font.render("Resume", False, "Yellow")
    resume_rectangle = resume.get_rect(center=(SCREEN_WIDTH/2, 480))

    stop_current_game = font.render("Main Menu", False, "Yellow")
    stop_current_game_rect = stop_current_game.get_rect(center=(SCREEN_WIDTH/2, 550))
    if blurred_background is None:
        blurred_background = flou(windows)
    if pause_choice == 0:
        resume = font.render("Resume", False, "Red")
        stop_current_game = font.render("Main Menu", False, "Yellow")
    if pause_choice == -1:
        resume = font.render("Resume", False, "Yellow")
        stop_current_game = font.render("Main Menu", False, "Red")
    windows.blit(blurred_background, (0, 0))
    windows.blit(resume, resume_rectangle)
    windows.blit(stop_current_game, stop_current_game_rect)
    pygame.display.update()
    return blurred_background


def load_images_gameover_victory(image: pygame.Surface, score: int, color: str) -> None:
    """Affiche les éléments de l'écran de fin.

    Args:
        image: Image de victoire ou de défaite.
        score: Score du joueur.
        color: Couleur du texte.
    """
    image = pygame.transform.scale(image, (900, 600))
    image_rect = image.get_rect(center=(windows.get_width()/2, 200))
    windows.blit(image, image_rect)
    score_surf = font_text.render(f"Your score: {score}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(windows.get_width()/2, 300))
    windows.blit(score_surf, score_rect)
    text_surf = font.render("Entrez votre nom:", False, color)
    text_rect = text_surf.get_rect(center=(windows.get_width()/2, 400))
    windows.blit(text_surf, text_rect)
    rectangle_surf = pygame.Surface((700, 100))
    rectangle_rect = rectangle_surf.get_rect(center=(windows.get_width()/2, 480))
    pygame.draw.rect(windows, color, rectangle_rect, 3, border_radius=10)
    confirm_surf = font_text.render("Press ENTER to confirm", False, (64, 64, 64))
    confirm_rect = confirm_surf.get_rect(center=(windows.get_width()/2, 560))
    windows.blit(confirm_surf, confirm_rect)
    exit_surf = font_text.render("Press ECHAP to skip", False, (64, 64, 64))
    exit_rect = exit_surf.get_rect(midbottom=(windows.get_width()/2, windows.get_height() - 10))
    time = pygame.time.get_ticks()

    if (time // 500) % 2 == 0:
        windows.blit(exit_surf, exit_rect)


def verif_config() -> Json:
    """Charge et valide la configuration.

    Raises:
        ValueError: Si le nombre d'arguments est incorrect.
        FileNotFoundError: Si le fichier est introuvable.
        json.JSONDecodeError: Si le fichier est invalide.

    Returns:
        Json: Configuration validée.
    """
    file = {}
    if len(sys.argv) != 2:
        raise ValueError("Trop ou trop peu d'arguments")
    name_file = sys.argv[1]
    with open(name_file, "r") as f:
        file = json.load(f)
    valid_file = Json(**file)
    return valid_file


def store_score(name_user: str) -> bool:
    """Enregistre le score du joueur.

    Args:
        name_user: Nom du joueur.

    Returns:
        bool: Indique si le jeu reste actif si le joueur a entrer un nom
              superieur a un caractere.
    """
    if len(name_user) >= 1:
        active_game = False
        try:
            with open(verif.highscore_filename, 'r') as f:
                content = json.load(f)
                if name_user in content.keys():
                    if score > content[name_user]:
                        content.update({name_user: score})
                else:
                    content.update({name_user: score})
                content = dict(sorted(content.items(), key=lambda x: x[1], reverse=True))
            with open(verif.highscore_filename, 'w') as f:
                json.dump(content, f, indent=4)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass
            # seulement si il arrive pas a ouvrir
            with open(verif.highscore_filename, 'w') as f:
                content = {name_user: score}
                json.dump(content, f, indent=4)
        except (Exception):
            pass
        return active_game
    else:
        return True


def show_superpacgum(pacgum: set[tuple[int, int]]) -> None:
    """Affiche les super pac-gums.

    Args:
        pacgum: Positions des super pac-gums.
    """
    for x, y in pacgum:
        center_x = x * CELL_SIZE + CELL_SIZE / 2
        center_y = y * CELL_SIZE + CELL_SIZE / 2

        objet = pygame.Surface((max(2, CELL_SIZE // 3), max(2, CELL_SIZE // 3)))
        objet_rect = objet.get_rect(center=(center_x, center_y))

        pygame.draw.rect(windows, "Orange", objet_rect, border_radius=40)


def create_superpacgum() -> set[tuple[int, int]]:
    """Crée les super pac-gums.

    Returns:
        set[tuple[int, int]]: Positions des super pac-gums.
    """
    superpacgum: set[tuple[int, int]] = set()
    seed(None)

    superpacgum.add((0, 0))
    superpacgum.add((verif.width - 1, 0))
    superpacgum.add((0, verif.height - 1))
    superpacgum.add((verif.width - 1, verif.height - 1))

    return superpacgum


def create_pacgum(maze_grid: list[list[int]]) -> set[tuple[int, int]]:
    """Crée les pac-gums dans le labyrinthe.

    Args:
        maze_grid: Grille du labyrinthe.

    Returns:
        set[tuple[int, int]]: Positions des pac-gums.
    """
    pacgum: set[tuple[int, int]] = set()
    seed(None)
    superpacgum = create_superpacgum()

    while len(pacgum) != verif.pacgum:
        width = randint(0, verif.width - 1)
        height = randint(0, verif.height - 1)
        if maze_grid[height][width] != 15 and (width, height) not in superpacgum:
            pacgum.add((width, height))
        continue

    return pacgum


def show_pacgum(pacgum: set[tuple[int, int]]) -> None:
    """Affiche les pac-gums.

    Args:
        pacgum: Positions des pac-gums.
    """
    for x, y in pacgum:
        center_x = x * CELL_SIZE + CELL_SIZE / 2
        center_y = y * CELL_SIZE + CELL_SIZE / 2

        objet = pygame.Surface((max(2, CELL_SIZE // 10), max(2, CELL_SIZE // 10)))
        objet_rect = objet.get_rect(center=(center_x, center_y))

        pygame.draw.rect(windows, "Orange", objet_rect, border_radius=40)


def show_maze() -> None:
    """Affiche le labyrinthe."""
    surface_pos_x = 0
    surface_pos_y = 0
    for _ in range(len(wall[0])):
        horizontal_wall.fill("White")
        windows.blit(horizontal_wall, (surface_pos_x, surface_pos_y))
        surface_pos_x += CELL_SIZE
    surface_pos_x = 0
    for _ in range(len(wall)):
        vertical_wall.fill("White")
        windows.blit(vertical_wall, (surface_pos_x, surface_pos_y))
        surface_pos_y += CELL_SIZE
    surface_pos_y = CELL_SIZE
    for i in wall:
        surface_pos_x = 0
        for element in i:
            if ((element >> 1) & 1) != 0:
                vertical_wall.fill("White")
                windows.blit(vertical_wall, (surface_pos_x + CELL_SIZE, surface_pos_y - CELL_SIZE))
            if ((element >> 2) & 1) != 0:
                horizontal_wall.fill("White")
                windows.blit(horizontal_wall, (surface_pos_x, surface_pos_y))
            surface_pos_x += CELL_SIZE
        surface_pos_y += CELL_SIZE


try:
    verif = verif_config()
except json.decoder.JSONDecodeError:
    print("Le fichier n'est pas en format json ou est complement vide")
    exit()
except FileNotFoundError:
    print("Le fichier config n'existe pas")
    exit()
except ValueError:
    print("Il y a trop ou trop peu d'argument")
    exit()
CELL_SIZE = SCREEN_WIDTH // verif.width
maze = MazeGenerator((verif.width, verif.height))
maze.generate()
wall = maze.maze
pygame.init()
windows = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
vertical_wall = pygame.Surface((1, CELL_SIZE))
horizontal_wall = pygame.Surface((CELL_SIZE, 1))
vertical_wall.fill("White")
horizontal_wall.fill("White")
font = pygame.font.Font("police/Pixeltype.ttf", 100)
h1_font = pygame.font.Font("police/Pixeltype.ttf", 300)
h2_font = pygame.font.Font("police/Pixeltype.ttf", 250)
font_text = pygame.font.Font("police/Pixeltype.ttf", 50)
time_font = pygame.font.Font("police/Pixeltype.ttf", 500)

gold_image = pygame.image.load("image/gold_medal.png").convert_alpha()
gold_image = pygame.transform.scale(gold_image, (50, 50))

silver_image = pygame.image.load("image/silver_medal.png").convert_alpha()
silver_image = pygame.transform.scale(silver_image, (50, 50))

bronze_image = pygame.image.load("image/bronze_medal.png").convert_alpha()
bronze_image = pygame.transform.scale(bronze_image, (50, 50))

run = True
score = 0
sprite = 1
count = 0
clock = pygame.time.Clock()
next_dir = 0
pacgum: set[tuple[int, int]] = create_pacgum(wall)
superpacgum: set[tuple[int, int]] = create_superpacgum()
active_game = False
exit_game = False
choice = 0
pause = False
level = 1
start_time = int(time())
pause_start_time = 0
time_inv = 0
pause_choice = 0
game_over = False
victory = False
blurred_background = None
initial_lives = verif.lives
name_user = ""
pressed = 0
highscore = False
instruction = False
cheat_mod = False
content: dict[str, int] = {}
cpt = 0
p1 = char.Pacman(460, 460, CELL_SIZE)
g1 = char.Ghost(960, 960, CELL_SIZE, "red")
g2 = char.Ghost(10, 960, CELL_SIZE, "pink")
g3 = char.Ghost(960, 10, CELL_SIZE, "blue")
g4 = char.Ghost(10, 10, CELL_SIZE, "orange")
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if not active_game:
                if not pause and not highscore and not instruction:
                    if choice == 0:
                        if event.key == pygame.K_DOWN:
                            choice = -1
                        if event.key == pygame.K_RETURN:
                            active_game = True
                    elif choice == -1:
                        if event.key == pygame.K_UP:
                            choice = 0
                        if event.key == pygame.K_DOWN:
                            choice = -2
                        if event.key == pygame.K_RETURN:
                            instruction = True
                    elif choice == -2:
                        if event.key == pygame.K_UP:
                            choice = -1
                        if event.key == pygame.K_DOWN:
                            choice = -3
                        if event.key == pygame.K_RETURN:
                            highscore = True
                    elif choice == -3:
                        if event.key == pygame.K_UP:
                            choice = -2
                        if event.key == pygame.K_RETURN:
                            pygame.quit()
                            exit()

                if instruction:
                    if event.key == pygame.K_q:
                        instruction = False

                if highscore:
                    if event.key == pygame.K_q:
                        highscore = False
            else:
                if not game_over and not victory and not pause:
                    if event.key == pygame.K_ESCAPE:
                        pause_start_time = int(time())
                        pause = True
                        pause_choice = 0
                        continue

                    if event.key == pygame.K_LCTRL:
                        cheat_mod = True
                        continue

            if pause:
                if pause_choice == 0:
                    if event.key == pygame.K_DOWN:
                        pause_choice = -1
                    if event.key == pygame.K_RETURN:
                        start_time += int(time()) - pause_start_time
                        pause = False
                        blurred_background = None
                elif pause_choice == -1:
                    if event.key == pygame.K_UP:
                        pause_choice = 0
                    if event.key == pygame.K_RETURN:
                        pause = False
                        blurred_background = None
                        active_game = False

            if game_over:
                if event.key == pygame.K_ESCAPE:
                    active_game = False
                    game_over = False
                    blurred_background = None

            if victory:
                if event.key == pygame.K_ESCAPE:
                    active_game = False
                    victory = False
                    blurred_background = None

            if victory or game_over:
                if event.key == pygame.K_BACKSPACE:
                    name_user = name_user[:-1]
                if len(name_user) < 10 and (event.unicode.isalnum() or event.unicode == ' '):
                    name_user += event.unicode

                if event.key == pygame.K_RETURN:
                    pressed += 1
                    active_game = store_score(name_user)

            if cheat_mod:
                if event.key == pygame.K_p:
                    for i in range(len(pacgum)):
                        score += verif.score_pacgum
                    for j in range(len(superpacgum)):
                        score += verif.score_superpacgum
                    pacgum = set()
                    superpacgum = set()
                if event.key == pygame.K_LCTRL:
                    cheat_mod = False

    if active_game:
        if pause:
            blurred_background = pause_screen(blurred_background)
            continue
        if game_over:
            blurred_background = game_over_screen(blurred_background)
            continue
        if victory:
            blurred_background = victory_screen(blurred_background)
            continue
        count += 1
        timer = verif.max_time + start_time - int(time())
        clock.tick(30)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            next_dir = 7
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            next_dir = 13
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            next_dir = 14
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            next_dir = 11
        if keys[pygame.K_t]:
            run = False
        p1.move(next_dir, wall)
        if int(time()) - g1.death_timer > 3 and g1.scared == 0:
            g1.move(p1.X, p1.Y, wall)
        elif g1.scared == 1:
            g1.flee(p1.X, p1.Y, wall)
        if int(time()) - g2.death_timer > 3 and g2.scared == 0:
            g2.move(p1.X, p1.Y, wall)
        elif g2.scared == 1:
            g2.flee(p1.X, p1.Y, wall)
        if int(time()) - g3.death_timer > 3 and g3.scared == 0:
            g3.move(p1.X, p1.Y, wall)
        elif g3.scared == 1:
            g3.flee(p1.X, p1.Y, wall)
        if int(time()) - g4.death_timer > 3 and g4.scared == 0:
            g4.move(p1.X, p1.Y, wall)
        elif g4.scared == 1:
            g4.flee(p1.X, p1.Y, wall)

        windows.fill((0, 0, 0))
        timer_surface = time_font.render(f"{timer}", False, (64, 64, 64))
        timer_rect = timer_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        timer_surface.set_alpha(128)  # rendre transparent du texte 128 moitie de 256 donc 50% de transparence
        windows.blit(timer_surface, timer_rect)
        show_maze()
        show_pacgum(pacgum)
        show_superpacgum(superpacgum)

        if (p1.X, p1.Y) in pacgum:
            score += verif.score_pacgum
            pacgum.remove((p1.X, p1.Y))
            show_pacgum(pacgum)

        if (p1.X, p1.Y) in superpacgum:
            score += verif.score_superpacgum
            g1.scared = 1
            g2.scared = 1
            g3.scared = 1
            g4.scared = 1
            time_inv = int(time())
            superpacgum.remove((p1.X, p1.Y))
            show_superpacgum(superpacgum)
        if int(time()) - time_inv == 5:
            g1.scared = 0
            g2.scared = 0
            g3.scared = 0
            g4.scared = 0
        if pacgum == set() and superpacgum == set():
            maze = MazeGenerator((verif.width, verif.height))
            maze.generate()
            wall = maze.maze
            p1.reset()
            g1.reset()
            g2.reset()
            g3.reset()
            g4.reset()
            next_dir = 0
            pacgum = create_pacgum(wall)
            superpacgum = create_superpacgum()
            level += 1
            start_time = int(time())
            if level - 1 == verif.level:
                victory = True
                continue

        if p1.rect.colliderect(g1.rect) and int(time()) - g1.death_timer > 3:
            if g1.scared == 0:
                verif.lives = verif.lives - 1
                if verif.lives == 0:
                    game_over = True
                    continue
                p1.reset()
                g1.reset()
                g2.reset()
                g3.reset()
                g4.reset()
                next_dir = 0
            else:
                score += verif.score_ghost
                g1.reset()
                g1.death_timer = int(time())
        if p1.rect.colliderect(g2.rect) and int(time()) - g2.death_timer > 3:
            if g2.scared == 0:
                verif.lives = verif.lives - 1
                if verif.lives == 0:
                    game_over = True
                    continue
                p1.reset()
                g1.reset()
                g2.reset()
                g3.reset()
                g4.reset()
                next_dir = 0
            else:
                score += verif.score_ghost
                g2.reset()
                g2.death_timer = int(time())
        if p1.rect.colliderect(g3.rect) and int(time()) - g3.death_timer > 3:
            if g3.scared == 0:
                verif.lives = verif.lives - 1
                if verif.lives == 0:
                    game_over = True
                    continue
                p1.reset()
                g1.reset()
                g2.reset()
                g3.reset()
                g4.reset()
                next_dir = 0
            else:
                score += verif.score_ghost
                g3.reset()
                g3.death_timer = int(time())
        if p1.rect.colliderect(g4.rect) and int(time()) - g4.death_timer > 3:
            if g4.scared == 0:
                verif.lives = verif.lives - 1
                if verif.lives == 0:
                    game_over = True
                    continue
                p1.reset()
                g1.reset()
                g2.reset()
                g3.reset()
                g4.reset()
                next_dir = 0
            else:
                score += verif.score_ghost
                g4.reset()
                g4.death_timer = int(time())
        if verif.lives == 0 or timer == 0:
            game_over = True
            continue
        windows.blit(p1.choose_dir(p1.frames[count % 4], p1.dir), (p1.x, p1.y))
        if int(time()) - g1.death_timer > 3:
            g1.show(count, windows)
        if int(time()) - g2.death_timer > 3:
            g2.show(count, windows)
        if int(time()) - g3.death_timer > 3:
            g3.show(count, windows)
        if int(time()) - g4.death_timer > 3:
            g4.show(count, windows)
        score_surface = font_text.render(f"{score}", False, (64, 64, 64))
        score_rect = score_surface.get_rect(bottomright=(990, 1050))
        windows.blit(score_surface, score_rect)
        life_text = font_text.render(f"Life: {verif.lives}", False, (64, 64, 64))
        life_rect = life_text.get_rect(midbottom=(SCREEN_WIDTH/2, 1050))
        windows.blit(life_text, life_rect)
        current_level = font_text.render(f"Level: {level}", False, (64, 64, 64))
        current_level_rect = current_level.get_rect(bottomleft=(5, 1050))
        windows.blit(current_level, current_level_rect)
        pygame.display.flip()
    else:
        maze = MazeGenerator((verif.width, verif.height))
        maze.generate(verif.seed)
        wall = maze.maze
        p1.reset()
        g1.reset()
        g2.reset()
        g3.reset()
        g4.reset()
        next_dir = 0
        pacgum = create_pacgum(wall)
        superpacgum = create_superpacgum()
        score = 0
        verif.lives = initial_lives
        level = 1
        start_time = int(time())
        victory = False
        game_over = False
        name_user = ""
        pressed = 0
        cheat_mod = False
        main_menu()
        if instruction:
            instruction_screen()
        if highscore:
            highscore_screen(content)
    pygame.display.update()
pygame.quit()
