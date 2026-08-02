import pygame
from mazegenerator import MazeGenerator
from random import randint

SCREEN_WIDTH = 1001
SCREEN_HEIGHT = 1001
WIDTH = 20
HEIGHT = 20
CELL_SIZE = SCREEN_WIDTH / WIDTH
PACGUM = 4000


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

        pygame.draw.rect(screen, "Orange", objet_rect)


def show_maze():
    surface_pos_x = 0
    surface_pos_y = 0
    for _ in range(len(maze_grid[0])):
        horizontal_wall.fill("White")
        screen.blit(horizontal_wall, (surface_pos_x, surface_pos_y))
        surface_pos_x += CELL_SIZE
    surface_pos_x = 0
    for _ in range(len(maze_grid)):
        vertical_wall.fill("White")
        screen.blit(vertical_wall, (surface_pos_x, surface_pos_y))
        surface_pos_y += CELL_SIZE
    surface_pos_y = CELL_SIZE
    for i in maze_grid:
        surface_pos_x = 0
        for element in i:
            if ((element >> 1) & 1) != 0:
                vertical_wall.fill("White")
                screen.blit(vertical_wall, (surface_pos_x + CELL_SIZE, surface_pos_y - CELL_SIZE))
            if ((element >> 2) & 1) != 0:
                horizontal_wall.fill("White")
                screen.blit(horizontal_wall, (surface_pos_x, surface_pos_y))
            surface_pos_x += CELL_SIZE
        surface_pos_y += CELL_SIZE


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()
vertical_wall = pygame.Surface((1, CELL_SIZE))
horizontal_wall = pygame.Surface((CELL_SIZE, 1))
maze_gen = MazeGenerator((WIDTH, HEIGHT))
maze_grid = maze_gen.maze
verif_config()
pacgum = create_pacgum(maze_grid)

show_maze()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    show_pacgum(pacgum)
    pygame.display.update()
    clock.tick(60)
