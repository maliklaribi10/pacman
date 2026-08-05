import pygame
from pygame.locals import QUIT, RESIZABLE
from mazegenerator import MazeGenerator
from typing import Any, Self
from random import randint, seed
import sys
import json
from time import time
from pydantic import Field, BaseModel, model_validator, ValidationError


class Json(BaseModel):
    highscore_filename: str = Field(min_length=1, default="score.json")
    level: int = Field(ge=10, default=10)
    width: int = Field(ge=10, default=20)
    height: int = Field(ge=10, default=20)
    lives: int = Field(ge=1, default=3)
    pacgum: int = Field(ge=1)
    score_pacgum: int = Field(ge=1, default=10)
    score_superpacgum: int = Field(ge=1, default=50)
    score_ghost: int = Field(ge=1, default=200)
    seed: int = Field(ge=1, default=42)
    max_time: int = Field(ge=90, default=90)

    @model_validator(mode="after")
    def filename_validator(self) -> Self:
        if not self.highscore_filename.endswith(".json"):
            raise ValueError("Votre fichier doit absolument etre un .json")
        return self

    @model_validator(mode="after")
    def pacgum_validator(self) -> Self:
        if self.pacgum > self.width * self.height - 22:
            raise ValueError("Le nombre de pacgum est trop grand pour un labyrinthe de cette taille")
        return self


def chase(
        p_coor: tuple[int, int],
        g_coor: tuple[int, int],
        maze: list[list[int]]
        ) -> int:
    directions = [
        (1, 0, -1),   # NORTH
        (2, 1, 0),    # EAST
        (4, 0, 1),    # SOUTH
        (8, -1, 0),   # WEST
    ]
    if p_coor == g_coor:
        return 0
    to_visit: list[tuple[int, int]] = [g_coor]
    index_to_visit = 0
    parents_children: dict[tuple[int, int], tuple[int, int] | None] = {}
    parents_children[g_coor] = None
    voisin: tuple[int, int]
    visited: set[tuple[int, int]] = {g_coor}

    while index_to_visit < len(to_visit):
        x, y = to_visit[index_to_visit]
        index_to_visit += 1

        if (x, y) == p_coor:
            break

        current_walls = maze[y][x]
        for wall, x_dir, y_dir in directions:
            nw_x = x + x_dir
            nw_y = y + y_dir

            voisin = (nw_x, nw_y)

            if voisin in visited:
                continue

            if current_walls & wall:
                continue

            if not (0 <= nw_x < 20 and 0 <= nw_y < 20):  # a change avec width et height modulable
                continue

            # if (nw_x, nw_y) in ft_logo:
            #     continue

            visited.add(voisin)
            parents_children[voisin] = (x, y)
            to_visit.append(voisin)

    path: list[tuple[int, int]] = []
    current_position: tuple[int, int] | None = p_coor
    while current_position is not None:
        path.append(current_position)
        current_position = parents_children[current_position]
    path.reverse()
    if path[1][0] == g_coor[0] and path[1][1] == g_coor[1] - 1:
        return 14
    if path[1][0] == g_coor[0] + 1 and path[1][1] == g_coor[1]:
        return 13
    if path[1][0] == g_coor[0] and path[1][1] == g_coor[1] + 1:
        return 11
    if path[1][0] == g_coor[0] - 1 and path[1][1] == g_coor[1]:
        return 7


def check(dir: int, wall: int) -> bool:
    if dir == 0:
        return False
    if (dir >> 0) & 1 == 0 and (wall >> 0) & 1 == 0:
        return True
    if (dir >> 1) & 1 == 0 and (wall >> 1) & 1 == 0:
        return True
    if (dir >> 2) & 1 == 0 and (wall >> 2) & 1 == 0:
        return True
    if (dir >> 3) & 1 == 0 and (wall >> 3) & 1 == 0:
        return True
    return False


def check_opposite(dir: int, next: int) -> bool:
    if dir == 14 and next == 11:
        return True
    if dir == 11 and next == 14:
        return True
    if dir == 7 and next == 13:
        return True
    if dir == 13 and next == 7:
        return True
    return False


def choose_dir(frame: Any, dir: int) -> Any:
    if dir == 7:
        frame = pygame.transform.rotate(frame, 180)
    if dir == 11:
        frame = pygame.transform.rotate(frame, 270)
    if dir == 13 or dir == 0:
        frame = frame
    if dir == 14:
        frame = pygame.transform.rotate(frame, 90)
    return frame


SCREEN_WIDTH = 1001
SCREEN_HEIGHT = 1050


def main_menu():
    windows.fill("Yellow")
    windows.blit(start_game, start_game_rectangle)
    windows.blit(instruction, instruction_rectangle)
    windows.blit(title_surface, title_rectangle)
    windows.blit(highscore, highscore_rectangle)
    windows.blit(sortie, sortie_rectangle)
    if choice == 0:
        pygame.draw.rect(windows, "Red", start_game_rectangle, 1)
    if choice == -1:
        pygame.draw.rect(windows, "Red", start_game_rectangle, -1)
        pygame.draw.rect(windows, "Red", instruction_rectangle, 1)
    if choice == -2:
        pygame.draw.rect(windows, "Red", instruction_rectangle, -1)
        pygame.draw.rect(windows, "Red", highscore_rectangle, 1)
    if choice == -3:
        pygame.draw.rect(windows, "Red", highscore_rectangle, -1)
        pygame.draw.rect(windows, "Red", sortie_rectangle, 1)


def verif_config():
    file = {}
    if len(sys.argv) != 2:
        raise ValueError("Trop ou trop peu d'arguments")
    name_file = sys.argv[1]
    with open(name_file, "r") as f:
        file = json.load(f)
    valid_file = Json(**file)
    return valid_file


def create_superpacgum(maze_grid: list[list[int]]):
    superpacgum: set[tuple[int, int]] = set()
    seed(None)

    superpacgum.add((0, 0))
    superpacgum.add((verif.width - 1, 0))
    superpacgum.add((0, verif.height - 1))
    superpacgum.add((verif.width - 1, verif.height - 1))

    return superpacgum


def show_superpacgum(pacgum: set[tuple[int, int]]):
    for x, y in pacgum:
        center_x = x * CELL_SIZE + CELL_SIZE / 2
        center_y = y * CELL_SIZE + CELL_SIZE / 2

        objet = pygame.Surface((max(2, CELL_SIZE // 3), max(2, CELL_SIZE // 3)))
        objet_rect = objet.get_rect(center=(center_x, center_y))

        pygame.draw.rect(windows, "Orange", objet_rect, border_radius=40)


def create_pacgum(maze_grid: list[list[int]]):
    pacgum: set[tuple[int, int]] = set()
    seed(None)
    superpacgum = create_superpacgum(maze_grid)

    while len(pacgum) != verif.pacgum:
        width = randint(0, verif.width - 1)
        height = randint(0, verif.height - 1)
        if maze_grid[height][width] != 15 and (width, height) not in superpacgum:
            pacgum.add((width, height))
        continue

    return pacgum


def show_pacgum(pacgum: set[tuple[int, int]]):
    for x, y in pacgum:
        center_x = x * CELL_SIZE + CELL_SIZE / 2
        center_y = y * CELL_SIZE + CELL_SIZE / 2

        objet = pygame.Surface((max(2, CELL_SIZE // 10), max(2, CELL_SIZE // 10)))
        objet_rect = objet.get_rect(center=(center_x, center_y))

        pygame.draw.rect(windows, "Orange", objet_rect)


def show_maze():
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


verif = verif_config()
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
font = pygame.font.Font("Pixeltype.ttf", 100)
h1_font = pygame.font.Font("Pixeltype.ttf", 300)
font_text = pygame.font.Font("Pixeltype.ttf", 50)
time_font = pygame.font.Font("Pixeltype.ttf", 500)

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

resume = font.render("Resume", False, (64, 64, 64))
resume_rectangle = resume.get_rect(center=(SCREEN_WIDTH/2, 480))

stop_current_game = font.render("Main Menu", False, (64, 64, 64))
stop_current_game_rect = stop_current_game.get_rect(center=(SCREEN_WIDTH/2, 550))

# show_maze()
# background = pygame.image.load("laby.png").convert()

# frames = [
#     pygame.image.load("d/pac0.png").convert_alpha(),
#     pygame.image.load("d/pac1.png").convert_alpha(),
#     pygame.image.load("d/pac2.png").convert_alpha(),
#     pygame.image.load("d/pac3.png").convert_alpha()
#     ]
ghost_x = 960
ghost_y = 960
ghost_frame = [
    pygame.transform.scale(pygame.image.load("ghost/f0.png").convert_alpha(), (32, 32)),
    pygame.transform.scale(pygame.image.load("ghost/f1.png").convert_alpha(), (32, 32))
    ]
# ghost_frame = pygame.transform.scale(pygame.image.load("ghost.gif").convert_alpha(), (32, 32))
g_vitesse = 5
g_X = int(ghost_x / CELL_SIZE)
g_Y = int(ghost_y / CELL_SIZE)

frames = []
for i in range(4):
    frame = pygame.image.load(f"d/pac{i}.png").convert_alpha()
    frames.append(frame)
# player = frames[0]
player_x = 460
X = int(player_x / CELL_SIZE)
player_y = 460
Y = int(player_y / CELL_SIZE)
vitesse = 5

run = True
score = 0
sprite = 1
count = 0
clock = pygame.time.Clock()
next_dir = 0
g_next_dir = 0
g_dir = 0
reste_x = 0
reste_y = 0
g_reste_x = 0
g_reste_y = 0
pacgum = create_pacgum(wall)
superpacgum = create_superpacgum(wall)
active_game = False
exit_game = False
choice = 0
pause = False
bot_dir = [7, 11, 13, 14]
life: int = 3
level = 1
actual_time = int(time())
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if choice == 0 and pause is False and active_game is False:
                if event.key == pygame.K_UP:
                    choice = 0
                if event.key == pygame.K_DOWN:
                    choice = -1
            elif choice == -1 and pause is False and active_game is False:
                if event.key == pygame.K_UP:
                    choice = 0
                if event.key == pygame.K_DOWN:
                    choice = -2
            elif choice == -2 and pause is False and active_game is False:
                if event.key == pygame.K_UP:
                    choice = -1
                if event.key == pygame.K_DOWN:
                    choice = -3
            elif choice == -3 and pause is False and active_game is False:
                if event.key == pygame.K_UP:
                    choice = -2
                if event.key == pygame.K_DOWN:
                    choice = -3
            if choice == 0 and event.key == pygame.K_RETURN and pause is False:
                active_game = True
            if choice == -3 and event.key == pygame.K_RETURN and pause is False:
                pygame.quit()
                exit()
            if event.key == pygame.K_ESCAPE:
                pause = True
                if pause:
                    choice = 0
                    continue
            if choice == 0 and pause is True:
                if event.key == pygame.K_UP:
                    choice = 0
                if event.key == pygame.K_DOWN:
                    choice = -1
            elif choice == -1 and pause is True:
                if event.key == pygame.K_UP:
                    choice = 0
                if event.key == pygame.K_DOWN:
                    choice = -1
            if choice == 0 and event.key == pygame.K_RETURN and pause is True:
                pause = False
            if choice == -1 and event.key == pygame.K_RETURN and pause is True:
                pause = False
                active_game = False
    if active_game:
        if pause:
            windows.fill("Blue")
            windows.blit(resume, resume_rectangle)
            windows.blit(stop_current_game, stop_current_game_rect)
            if choice == 0:
                pygame.draw.rect(windows, "Red", resume_rectangle, 1)
            if choice == -1:
                pygame.draw.rect(windows, "Red", resume_rectangle, -1)
                pygame.draw.rect(windows, "Red", stop_current_game_rect, 1)
            pygame.display.update()
            continue
        count += 1
        timer = verif.max_time + actual_time - int(time())
        player = choose_dir(frames[count % 4], dir)
        ghost = ghost_frame[count % 2]
        # ghost = ghost_frame
        player_rect = pygame.Rect(player_x, player_y, player.get_width(), player.get_height())
        ghost_rect = pygame.Rect(ghost_x, ghost_y, ghost.get_width(), ghost.get_height())
        clock.tick(30)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            # next_dir = "left"
            next_dir = 7
            # player = pygame.transform.rotate(frames[1], 180)
            # frames = ["a/pac0.png", "a/pac1.png", "a/pac2.png", "a/pac3.png"]
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            # next_dir = "right"
            next_dir = 13
            # frames = ["d/pac0.png", "d/pac1.png", "d/pac2.png", "d/pac3.png"]
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            # next_dir = "up"
            next_dir = 14
            # frames = ["w/pac0.png", "w/pac1.png", "w/pac2.png", "w/pac3.png"]
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            # next_dir = "down"
            next_dir = 11
            # frames = ["s/pac0.png", "s/pac1.png", "s/pac2.png", "s/pac3.png"]
        if keys[pygame.K_t]:
            run = False
        if check_opposite(dir, next_dir):
            dir = next_dir
        if check(next_dir, wall[Y][X]) and reste_x == 10 and reste_y == 10:
            dir = next_dir
        if dir == 7 and player_x > 10:
            if (wall[Y][X] >> 3) & 1 == 1 and reste_x == 10 and reste_y == 10:
                pass
            else:
                player_x -= vitesse
        if dir == 13 and player_x < SCREEN_WIDTH - CELL_SIZE + 10:
            if (wall[Y][X] >> 1) & 1 == 1 and reste_x == 10 and reste_y == 10:
                pass
            else:
                player_x += vitesse
        if dir == 14 and player_y > 10:
            if (wall[Y][X] >> 0) & 1 == 1 and reste_x == 10 and reste_y == 10:
                pass
            else:
                player_y -= vitesse
        if dir == 11 and player_y < SCREEN_HEIGHT - CELL_SIZE + 10:
            if (wall[Y][X] >> 2) & 1 == 1 and reste_x == 10 and reste_y == 10:
                pass
            else:
                player_y += vitesse

        g_next_dir = chase((X, Y), (g_X, g_Y), wall)
        if check(g_next_dir, wall[g_Y][g_X]) and g_reste_x == 10 and g_reste_y == 10:
            g_dir = g_next_dir
        if g_dir == 7 and ghost_x > 10:
            if (wall[g_Y][g_X] >> 3) & 1 == 1 and g_reste_x == 10 and g_reste_y == 10:
                pass
            else:
                ghost_x -= g_vitesse
        if g_dir == 13 and ghost_x < SCREEN_WIDTH - CELL_SIZE + 10:
            if (wall[g_Y][g_X] >> 1) & 1 == 1 and g_reste_x == 10 and g_reste_y == 10:
                pass
            else:
                ghost_x += g_vitesse
        if g_dir == 14 and ghost_y > 10:
            if (wall[g_Y][g_X] >> 0) & 1 == 1 and g_reste_x == 10 and g_reste_y == 10:
                pass
            else:
                ghost_y -= g_vitesse
        if g_dir == 11 and ghost_y < SCREEN_HEIGHT - CELL_SIZE + 10:
            if (wall[g_Y][g_X] >> 2) & 1 == 1 and g_reste_x == 10 and g_reste_y == 10:
                pass
            else:
                ghost_y += g_vitesse
        X = player_rect.centerx // CELL_SIZE
        Y = player_rect.centery // CELL_SIZE
        reste_x = player_x % CELL_SIZE
        reste_y = player_y % CELL_SIZE
        g_X = ghost_rect.centerx // CELL_SIZE
        g_Y = ghost_rect.centery // CELL_SIZE
        g_reste_x = ghost_x % CELL_SIZE
        g_reste_y = ghost_y % CELL_SIZE

        # windows.blit(background, (0, 0))
        # pygame.display.flip()
        # print(f"X={player_x} Y={player_y} X={X} Y={Y} resteX={reste_x} restY= {reste_y} dir= {dir} cell= {wall[Y][X]}")
        windows.fill((0, 0, 0))
        timer_surface = time_font.render(f"{timer}", False, (64, 64, 64))
        timer_rect = timer_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        timer_surface.set_alpha(128)  # rendre transparent du texte 128 moitie de 256 donc 50% de transparence
        windows.blit(timer_surface, timer_rect)
        show_maze()
        show_pacgum(pacgum)
        show_superpacgum(superpacgum)
        if (X, Y) in pacgum:
            score += verif.score_pacgum
            pacgum.remove((X, Y))
            show_pacgum(pacgum)
        if (X, Y) in superpacgum:
            score += verif.score_superpacgum
            superpacgum.remove((X, Y))
            show_superpacgum(superpacgum)
        if pacgum == set() and superpacgum == set():
            maze = MazeGenerator((verif.width, verif.height))
            maze.generate()
            wall = maze.maze
            ghost_x = 960
            ghost_y = 960
            g_X = int(ghost_x / CELL_SIZE)
            g_Y = int(ghost_y / CELL_SIZE)
            player_x = 460
            X = int(player_x / CELL_SIZE)
            player_y = 460
            Y = int(player_y / CELL_SIZE)
            vitesse = 5
            next_dir = 0
            g_next_dir = chase((X, Y), (g_X, g_Y), wall)
            g_dir = 0
            pacgum = create_pacgum(wall)
            superpacgum = create_superpacgum(wall)
            level += 1
            if level - 1 == verif.level:
                active_game = False  # a changer pour mettre lecran de victoire
        if X == g_X and Y == g_Y:
            player_x = 460
            player_y = 460
            ghost_x = 960
            ghost_y = 960
            g_dir = 0
            g_next_dir = 0
            dir = 0
            next_dir = 0
            verif.lives = verif.lives - 1
        if verif.lives == 0:
            active_game = False
        windows.blit(player, (player_x, player_y))
        windows.blit(ghost, (ghost_x, ghost_y))
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
        ghost_x = 960
        ghost_y = 960
        g_X = int(ghost_x / CELL_SIZE)
        g_Y = int(ghost_y / CELL_SIZE)
        player_x = 460
        X = int(player_x / CELL_SIZE)
        player_y = 460
        Y = int(player_y / CELL_SIZE)
        vitesse = 5
        next_dir = 0
        dir = 0
        g_next_dir = chase((X, Y), (g_X, g_Y), wall)
        g_dir = 0
        pacgum = create_pacgum(wall)
        superpacgum = create_superpacgum(wall)
        score = 0
        verif.lives = 3
        level = 1
        main_menu()
    pygame.display.update()
pygame.quit()
