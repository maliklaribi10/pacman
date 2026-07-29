import pygame
from mazegenerator import MazeGenerator

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
WIDTH = 20
HEIGHT = 20
RECTANGLE = SCREEN_WIDTH / WIDTH


def show_maze():
    surface_pos_x = 0
    surface_pos_y = 0
    for _ in range(len(maze_grid[0])):
        horizontal_wall.fill("White")
        screen.blit(horizontal_wall, (surface_pos_x, surface_pos_y))
        surface_pos_x += RECTANGLE
    surface_pos_x = 0
    for _ in range(len(maze_grid)):
        vertical_wall.fill("White")
        screen.blit(vertical_wall, (surface_pos_x, surface_pos_y))
        surface_pos_y += RECTANGLE
    surface_pos_y = RECTANGLE
    for i in maze_grid:
        surface_pos_x = 0
        for element in i:
            if ((element >> 1) & 1) != 0:
                vertical_wall.fill("White")
                screen.blit(vertical_wall, (surface_pos_x + RECTANGLE, surface_pos_y - RECTANGLE))
            if ((element >> 2) & 1) != 0:
                horizontal_wall.fill("White")
                screen.blit(horizontal_wall, (surface_pos_x, surface_pos_y))
            surface_pos_x += RECTANGLE
        surface_pos_y += RECTANGLE


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
vertical_wall = pygame.Surface((1, RECTANGLE))
horizontal_wall = pygame.Surface((RECTANGLE, 1))
maze_gen = MazeGenerator((WIDTH, HEIGHT))
maze_grid = maze_gen.maze
shortest_path = maze_gen.shortest_path
print(maze_grid)

show_maze()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
    clock.tick(60)
