import pygame
from pygame.locals import QUIT, RESIZABLE
from mazegenerator import MazeGenerator
from math import ceil
from typing import Any
from random import randint


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


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
WIDTH = 20
HEIGHT = 20
CELL_SIZE = SCREEN_WIDTH / WIDTH
PACGUM = 5


def verif_config():
    global PACGUM
    if PACGUM >= WIDTH * HEIGHT - 18:
        PACGUM = WIDTH * HEIGHT - 18


def create_pacgum(maze_grid: list[list[int]]):
    pacgum: set[tuple[int, int]] = set()

    while len(pacgum) != PACGUM:
        width = randint(0, WIDTH - 1)
        height =  randint(0, HEIGHT - 1)
        if maze_grid[height][width] != 15:
            pacgum.add((width, height))

    return pacgum

def show_pacgum(pacgum: set[tuple[int, int]]):
    for x, y in pacgum:
        center_x = x * CELL_SIZE + CELL_SIZE / 2
        center_y = y * CELL_SIZE + CELL_SIZE / 2

        objet = pygame.Surface((5,5))
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


maze = MazeGenerator((WIDTH, HEIGHT))
maze.generate()
wall = maze.maze
print(wall)
pygame.init()
windows = pygame.display.set_mode((1010, 1010), RESIZABLE)
vertical_wall = pygame.Surface((1, CELL_SIZE))
horizontal_wall = pygame.Surface((CELL_SIZE, 1))
vertical_wall.fill("White")
horizontal_wall.fill("White")
# show_maze()
# background = pygame.image.load("laby.png").convert()

# frames = [
#     pygame.image.load("d/pac0.png").convert_alpha(),
#     pygame.image.load("d/pac1.png").convert_alpha(),
#     pygame.image.load("d/pac2.png").convert_alpha(),
#     pygame.image.load("d/pac3.png").convert_alpha()
#     ]
frames = []
for i in range(4):
    frame = pygame.image.load(f"d/pac{i}.png").convert_alpha()
    frames.append(frame)
# player = frames[0]
player_x = 10
X = int(player_x / 20 - 1)
player_y = 10
Y = int(player_y / 20 - 1)
vitesse = 5


run = True
sprite = 1
count = 0
clock = pygame.time.Clock()
next_dir = 0
reste_x = 0
reste_y = 0
verif_config()
pacgum = create_pacgum(wall)
while run:
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
    count += 1
    # player = frames[count % 4]
    player = choose_dir(frames[count % 4], dir)
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
    X = int(ceil(player_x / CELL_SIZE - 1))
    Y = int(ceil(player_y / CELL_SIZE - 1))
    reste_x = player_x % CELL_SIZE
    reste_y = player_y % CELL_SIZE
    # windows.blit(background, (0, 0))
    # pygame.display.flip()
    # print(f"X={X} Y={Y}")
    print(f"X={player_x} Y={player_y} X={X} Y={Y} resteX={reste_x} restY= {reste_y} dir= {dir} cell= {wall[Y][X]}")
    windows.fill((0, 0, 0))
    show_maze()
    show_pacgum(pacgum)
    if (X, Y) in pacgum:
        pacgum.remove((X, Y))
        show_pacgum(pacgum)
    if pacgum == set():
        pygame.quit()
        exit()
    windows.blit(player, (player_x, player_y))
    pygame.display.flip()
pygame.quit()
