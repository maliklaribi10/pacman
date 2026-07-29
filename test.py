import pygame
from mazegenerator import MazeGenerator


def show_maze():
    surface_pos_x = 0
    surface_pos_y = 0
    for _ in range(len(maze_grid[0])):
        horizontal_wall.fill("White")
        screen.blit(horizontal_wall, (surface_pos_x, surface_pos_y))
        surface_pos_x += 20
    surface_pos_x = 0
    for _ in range(len(maze_grid)):
        vertical_wall.fill("White")
        screen.blit(vertical_wall, (surface_pos_x, surface_pos_y))
        surface_pos_y += 20
    surface_pos_y = 20
    for i in maze_grid:
        surface_pos_x = 0
        for element in i:
            if ((element >> 1) & 1) != 0:
                vertical_wall.fill("White")
                screen.blit(vertical_wall, (surface_pos_x + 20, surface_pos_y - 20))
            if ((element >> 2) & 1) != 0:
                horizontal_wall.fill("White")
                screen.blit(horizontal_wall, (surface_pos_x, surface_pos_y))
            surface_pos_x += 20
        surface_pos_y += 20


pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
vertical_wall = pygame.Surface((1, 20))
horizontal_wall = pygame.Surface((20, 1))
vertical_wall.fill("White")
horizontal_wall.fill("White")
maze_gen = MazeGenerator((200, 200))
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
