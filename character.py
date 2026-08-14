import pygame
from typing import Any
from pygame import Surface

SCREEN_WIDTH = 1001
SCREEN_HEIGHT = 1050


class Character():
    """Représente un personnage du jeu."""
    def __init__(self, x: float, y: float, CELL_SIZE: int):
        """Initialise le personnage.

        Args:
            x: Position horizontale.
            y: Position verticale.
            CELL_SIZE: Taille d'une cellule.
        """
        self.x = x
        self.y = y
        self.X = int(x / CELL_SIZE)
        self.Y = int(y / CELL_SIZE)
        self.speed = 5.0
        self.dir = 0
        self.reX = x % CELL_SIZE
        self.reY = y % CELL_SIZE
        self.CELL_SIZE = CELL_SIZE
        self.next_dir = 0
        self.start_x = x
        self.start_y = y

    def check(self, dir: int, wall: int) -> bool:
        """Vérifie si une direction est libre.

        Args:
            dir: Direction à vérifier.
            wall: Murs de la cellule.

        Returns:
            bool: True si la direction est libre.
        """
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

    def check_opposite(self, dir: int, next: int) -> bool:
        """Vérifie si deux directions sont opposées.

        Args:
            dir: Direction actuelle.
            next: Direction suivante.

        Returns:
            bool: True si les directions sont opposées.
        """
        if dir == 14 and next == 11:
            return True
        if dir == 11 and next == 14:
            return True
        if dir == 7 and next == 13:
            return True
        if dir == 13 and next == 7:
            return True
        return False

    def reset(self) -> None:
        """Réinitialise le personnage à sa position de départ."""
        self.x = self.start_x
        self.y = self.start_y
        self.X = int(self.start_x / self.CELL_SIZE)
        self.Y = int(self.start_y / self.CELL_SIZE)
        self.dir = 0
        self.reX = self.start_x % self.CELL_SIZE
        self.reY = self.start_y % self.CELL_SIZE
        self.CELL_SIZE = self.CELL_SIZE
        self.next_dir = 0


class Pacman(Character):
    """Représente le personnage Pac-Man."""
    def __init__(self, x: int, y: int, CELL_SIZE: int):
        """Initialise Pac-Man.

        Args:
            x: Position horizontale.
            y: Position verticale.
            CELL_SIZE: Taille d'une cellule.
        """
        super().__init__(x, y, CELL_SIZE)
        self.frames = [
            pygame.image.load("pacman/pac0.png").convert_alpha(),
            pygame.image.load("pacman/pac0.png").convert_alpha(),
            pygame.image.load("pacman/pac1.png").convert_alpha(),
            pygame.image.load("pacman/pac1.png").convert_alpha(),
            pygame.image.load("pacman/pac2.png").convert_alpha(),
            pygame.image.load("pacman/pac2.png").convert_alpha(),
            pygame.image.load("pacman/pac3.png").convert_alpha(),
            pygame.image.load("pacman/pac3.png").convert_alpha()
            ]
        self.sprite = self.frames[0]
        self.rect = pygame.Rect(
            self.x, self.y, self.sprite.get_width(), self.sprite.get_height())

    @staticmethod
    def choose_dir(frame: Any, dir: int) -> Any:
        """Oriente le sprite selon la direction.

        Args:
            frame: Image du sprite.
            dir: Direction du personnage.

        Returns:
            Any: Sprite orienté.
        """
        if dir == 7:
            frame = pygame.transform.rotate(frame, 180)
        if dir == 11:
            frame = pygame.transform.rotate(frame, 270)
        if dir == 13 or dir == 0:
            frame = frame
        if dir == 14:
            frame = pygame.transform.rotate(frame, 90)
        return frame

    def move(self, next_dir: int, wall: list[list[int]]) -> None:
        """Déplace Pac-Man dans le labyrinthe.

        Args:
            next_dir: Direction souhaitée.
            wall: Murs du labyrinthe.
        """
        self.next_dir = next_dir
        if self.check_opposite(self.dir, self.next_dir):
            self.dir = self.next_dir
        if self.check(self.next_dir, wall[self.Y][self.X])\
                and self.reX == 10 and self.reY == 10:
            self.dir = self.next_dir
        if self.dir == 7 and self.x > 10:
            if (wall[self.Y][self.X] >> 3) & 1 == 1\
                    and self.reX == 10 and self.reY == 10:
                pass
            else:
                self.x -= self.speed
        if self.dir == 13 and self.x < SCREEN_WIDTH - self.CELL_SIZE + 10:
            if (wall[self.Y][self.X] >> 1) & 1 == 1\
                    and self.reX == 10 and self.reY == 10:
                pass
            else:
                self.x += self.speed
        if self.dir == 14 and self.y > 10:
            if (wall[self.Y][self.X] >> 0) & 1 == 1\
                    and self.reX == 10 and self.reY == 10:
                pass
            else:
                self.y -= self.speed
        if self.dir == 11 and self.y < SCREEN_HEIGHT - self.CELL_SIZE + 10:
            if (wall[self.Y][self.X] >> 2) & 1 == 1\
                    and self.reX == 10 and self.reY == 10:
                pass
            else:
                self.y += self.speed
        self.X = int(self.x // self.CELL_SIZE)
        self.Y = int(self.y // self.CELL_SIZE)
        self.reX = self.x % self.CELL_SIZE
        self.reY = self.y % self.CELL_SIZE

    def collide(self, x: float, y: float) -> bool:
        return abs(self.y - y) < 20 and abs(self.x - x) < 20


class Ghost(Character):
    """Représente un fantôme du jeu."""
    def __init__(self, x: int, y: int, CELL_SIZE: int, color: str):
        """Initialise un fantôme.

        Args:
            x: Position horizontale.
            y: Position verticale.
            CELL_SIZE: Taille d'une cellule.
            color: Couleur du fantôme.
        """
        super().__init__(x, y, CELL_SIZE)
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(
                    f"ghost/{color}/f0.png").convert_alpha(), (32, 32)),
            pygame.transform.scale(
                pygame.image.load(
                    f"ghost/{color}/f1.png").convert_alpha(), (32, 32))
            ]
        self.sprite = self.frames[0]
        self.rect = pygame.Rect(
            self.x, self.y, self.sprite.get_width(), self.sprite.get_height())
        self.scared = 0
        self.scared_frames = [
            pygame.transform.scale(
                pygame.image.load(
                    "ghost/scared/f0.png").convert_alpha(), (32, 32)),
            pygame.transform.scale(
                pygame.image.load(
                    "ghost/scared/f1.png").convert_alpha(), (32, 32)),
            pygame.transform.scale(
                pygame.image.load(
                    "ghost/scared/f2.png").convert_alpha(), (32, 32)),
            pygame.transform.scale(
                pygame.image.load(
                    "ghost/scared/f3.png").convert_alpha(), (32, 32)),
            pygame.transform.scale(
                pygame.image.load(
                    "ghost/scared/f4.png").convert_alpha(), (32, 32)),
            pygame.transform.scale(
                pygame.image.load(
                    "ghost/scared/f5.png").convert_alpha(), (32, 32)),
            pygame.transform.scale(
                pygame.image.load(
                    "ghost/scared/f6.png").convert_alpha(), (32, 32)),
            pygame.transform.scale(
                pygame.image.load(
                    "ghost/scared/f7.png").convert_alpha(), (32, 32))
        ]
        self.death_timer = 0

    def chase(
        self,
        p_coor: tuple[int, int],
        g_coor: tuple[int, int],
        maze: list[list[int]]
         ) -> int:
        """Cherche le chemin vers Pac-Man.

        Args:
            p_coor: Position de Pac-Man.
            g_coor: Position du fantôme.
            maze: Grille du labyrinthe.

        Returns:
            int: Direction à suivre.
        """
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

                if not (0 <= nw_x < 20 and 0 <= nw_y < 20):
                    continue

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
        return 7

    def move(self, X: int, Y: int, wall: list[list[int]]) -> None:
        """Déplace le fantôme vers Pac-Man.

        Args:
            X: Position horizontale de Pac-Man.
            Y: Position verticale de Pac-Man.
            wall: Murs du labyrinthe.
        """
        if self.reX == 10 and self.reY == 10:
            self.speed = 5.0
        self.next_dir = self.chase((X, Y), (self.X, self.Y), wall)
        if self.check(self.next_dir, wall[self.Y][self.X])\
                and self.reX == 10 and self.reY == 10:
            self.dir = self.next_dir
        if self.dir == 7 and self.x > 10:
            if (wall[self.Y][self.X] >> 3) & 1 == 1\
                    and self.reX == 10 and self.reY == 10:
                pass
            else:
                self.x -= self.speed
        if self.dir == 13 and self.x < SCREEN_WIDTH - self.CELL_SIZE + 10:
            if (wall[self.Y][self.X] >> 1) & 1 == 1\
                    and self.reX == 10 and self.reY == 10:
                pass
            else:
                self.x += self.speed
        if self.dir == 14 and self.y > 10:
            if (wall[self.Y][self.X] >> 0) & 1 == 1\
                    and self.reX == 10 and self.reY == 10:
                pass
            else:
                self.y -= self.speed
        if self.dir == 11 and self.y < SCREEN_HEIGHT - self.CELL_SIZE + 10:
            if (wall[self.Y][self.X] >> 2) & 1 == 1\
                    and self.reX == 10 and self.reY == 10:
                pass
            else:
                self.y += self.speed
        self.X = int(self.x // self.CELL_SIZE)
        self.Y = int(self.y // self.CELL_SIZE)
        self.reX = self.x % self.CELL_SIZE
        self.reY = self.y % self.CELL_SIZE

    def flee(self, X: int, Y: int, wall: list[list[int]]) -> None:
        """Éloigne le fantôme de Pac-Man.

        Args:
            X: Position horizontale de Pac-Man.
            Y: Position verticale de Pac-Man.
            wall: Murs du labyrinthe.
        """
        self.speed = 2.5
        dir_pos = [7, 11, 13, 14]
        self.next_dir = self.chase((X, Y), (self.X, self.Y), wall)
        if self.next_dir == 0:
            return
        dir_pos.remove(self.next_dir)
        for next_dir in dir_pos:
            if self.check(next_dir, wall[self.Y][self.X])\
                    and self.reX == 10 and self.reY == 10:
                self.dir = next_dir
        if self.dir == 7 and self.x > 10:
            if (wall[self.Y][self.X] >> 3) & 1 == 1\
                    and self.reX == 10 and self.reY == 10:
                pass
            else:
                self.x -= self.speed
        if self.dir == 13 and self.x < SCREEN_WIDTH - self.CELL_SIZE + 10:
            if (wall[self.Y][self.X] >> 1) & 1 == 1\
                    and self.reX == 10 and self.reY == 10:
                pass
            else:
                self.x += self.speed
        if self.dir == 14 and self.y > 10:
            if (wall[self.Y][self.X] >> 0) & 1 == 1\
                    and self.reX == 10 and self.reY == 10:
                pass
            else:
                self.y -= self.speed
        if self.dir == 11 and self.y < SCREEN_HEIGHT - self.CELL_SIZE + 10:
            if (wall[self.Y][self.X] >> 2) & 1 == 1\
                    and self.reX == 10 and self.reY == 10:
                pass
            else:
                self.y += self.speed
        self.X = int(self.x // self.CELL_SIZE)
        self.Y = int(self.y // self.CELL_SIZE)
        self.reX = self.x % self.CELL_SIZE
        self.reY = self.y % self.CELL_SIZE

    def reset(self) -> None:
        """Réinitialise le fantôme à sa position de départ."""
        super().reset()
        self.scared = 0
        self.death_timer = 0

    def show(self, count: int, windows: Surface) -> None:
        """Affiche le fantôme.

        Args:
            count: Compteur d'animation.
            windows: Surface d'affichage.
        """
        if self.scared == 1:
            windows.blit(self.scared_frames[count % 8], (self.x, self.y))
        else:
            windows.blit(self.frames[count % 2], (self.x, self.y))
