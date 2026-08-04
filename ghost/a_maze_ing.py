'''
Le fichier config s'ecrit sous la forme "KEY=VALUE"
les "KEY" obligatoire sont:
    WIDTH           (OBLIGATOIRE et doit etre un entier)
    HEIGHT          (OBLIGATOIRE et doit etre un entier)
    ENTRY           (OBLIGATOIRE et doit etre un tuple d'entier)
    EXIT            (OBLIGATOIRE et doit etre un tuple d'entier)
    OUTPUT_FILE     (OBLIGATOIRE et doit etre une string)
    PERFECT         (OBLIGATOIRE et doit etre un bool)

1. Importer la classe MazeGenerator
Avant de pouvoir utiliser le générateur, il est nécessaire d'importer la
 classe MazeGenerator.
from Maze import MazeGenerator
Si vous souhaitez également utiliser les couleurs proposées par le projet,
 importez la classe Color :
from Color import Color

2. Créer une instance du générateur
Une fois la classe importée, créez une instance de MazeGenerator.
maze = MazeGenerator()
Cette instance contient toutes les méthodes nécessaires pour générer et
 afficher un labyrinthe.

3. Générer le labyrinthe
Pour lancer la génération, appelez la méthode main().
cells = maze.main()
La méthode génère le labyrinthe et retourne l'ensemble des cellules qui le
 composent. Ces cellules sont stockées dans la variable cells.

4. Choisir une couleur d'affichage
Sélectionnez ensuite la couleur souhaitée pour l'affichage.
color = Color.WHITE
Vous pouvez remplacer Color.WHITE par toute autre couleur disponible dans la
 classe Color.

5. Afficher le labyrinthe
Pour afficher le labyrinthe généré, utilisez la méthode maze_show().
maze.maze_show(cells, color)
Cette méthode prend deux paramètres :
cells : les cellules du labyrinthe généré.
color : la couleur utilisée pour l'affichage.
Exemple complet
from Maze import MazeGenerator
from Color import Color

maze = MazeGenerator()
cells = maze.main()
color = Color.WHITE
maze.maze_show(cells, color)
'''
from random import randint, choice, seed
from math import ceil, floor
from typing import Any
import sys


class Color:
    '''
    Class of all colors we used
    '''
    RESET = "\033[0m"

    BLACK = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    BROWN = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    FD_BLACK = "\033[40m"
    FD_RED = "\033[41m"
    FD_GREEN = "\033[42m"
    FD_BROWN = "\033[43m"
    FD_BLUE = "\033[44m"
    FD_MAGENTA = "\033[45m"
    FD_CYAN = "\033[46m"
    FD_WHITE = "\033[47m"
    all = [RED, GREEN, BROWN, BLUE, MAGENTA, CYAN, WHITE]
    all_fd = [
        FD_BLACK, FD_BLUE, FD_CYAN, FD_GREEN, FD_MAGENTA, FD_RED, FD_BROWN]


class MazeGenerator:
    def __init__(self) -> None:
        self.WIDTH: int = 11
        self.HEIGHT: int = 11
        self.START: tuple[int, int] = (0, 0)
        self.END: tuple[int, int] = (0, 0)
        self.OUTPUT_FILE: str = "maze.txt"
        self.PERFECT: bool = True
        self.SEED: Any = None

    @staticmethod
    def to_hex(value: int) -> str:
        """Convert a decimal integer to its hexadecimal representation.

        Args:
            value: The decimal integer to convert.

        Returns:
            The hexadecimal representation of the given integer as an
            uppercase string.
        """
        digits = "0123456789ABCDEF"
        if value == 0:
            return "0"
        result = ""
        while value > 0:
            result = digits[value % 16] + result
            value //= 16
        return result

    def output(
            self,
            cells: dict[tuple[int, int], list[int]],
            path: list[tuple[int, int]]
            ) -> None:
        """Write the generated maze and its solution to the output file.

        The maze is stored using hexadecimal values to represent the walls
        of each cell. The file also contains the entry and exit coordinates,
        followed by the solution path encoded with the cardinal directions
        ('N', 'E', 'S', 'W').

        Args:
            cells: Dictionary containing the maze cells and their wall data.
            path: Ordered list of cell coordinates representing the solution
                path from the entrance to the exit.
        """
        with open(self.OUTPUT_FILE, 'w') as f:
            for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    f.write(self.to_hex(cells[(x, y)][1]))
                f.write("\n")
            f.write("\n")
            f.write("\n")
            f.write(str(self.START).strip("(").strip(")") + "\n")
            f.write(str(self.END).strip("(").strip(")") + "\n")
            directions = [
                (0, -1),   # NORTH
                (1, 0),    # EAST
                (0, 1),    # SOUTH
                (-1, 0),   # WEST
            ]
            for i in range(len(path) - 1):
                if path[i + 1][0] == path[i][0] + directions[0][0] \
                        and path[i + 1][1] == path[i][1] + directions[0][1]:
                    f.write("N")
                if path[i + 1][0] == path[i][0] + directions[1][0] \
                        and path[i + 1][1] == path[i][1] + directions[1][1]:
                    f.write("E")
                if path[i + 1][0] == path[i][0] + directions[2][0] \
                        and path[i + 1][1] == path[i][1] + directions[2][1]:
                    f.write("S")
                if path[i + 1][0] == path[i][0] + directions[3][0] \
                        and path[i + 1][1] == path[i][1] + directions[3][1]:
                    f.write("W")

    def solve_maze(
            self,
            cells: dict[tuple[int, int], list[int]]
            ) -> list[tuple[int, int]]:
        """Find the shortest path from the maze entrance to the exit.

        This method uses a Breadth-First Search (BFS) algorithm to explore
        the maze while avoiding walls and blocked cells. It reconstructs and
        returns the shortest path once the exit is reached.

        Args:
            cells: Dictionary containing the maze cells and their wall data.

        Returns:
            An ordered list of cell coordinates representing the shortest
            path from the entrance to the exit.
        """
        directions = [
            (1, 0, -1),   # NORTH
            (2, 1, 0),    # EAST
            (4, 0, 1),    # SOUTH
            (8, -1, 0),   # WEST
        ]
        ft_logo = self.create_ft()
        to_visit: list[tuple[int, int]] = [self.START]
        index_to_visit = 0
        parents_children: dict[tuple[int, int], tuple[int, int] | None] = {}
        parents_children[self.START] = None
        voisin: tuple[int, int]
        visited: set[tuple[int, int]] = {self.START}

        while index_to_visit < len(to_visit):
            x, y = to_visit[index_to_visit]
            index_to_visit += 1

            if (x, y) == self.END:
                break

            current_walls = cells[x, y][1]
            for wall, x_dir, y_dir in directions:
                nw_x = x + x_dir
                nw_y = y + y_dir

                voisin = (nw_x, nw_y)

                if voisin in visited:
                    continue

                if current_walls & wall:
                    continue

                if not (0 <= nw_x < self.WIDTH and 0 <= nw_y < self.HEIGHT):
                    continue

                if (nw_x, nw_y) in ft_logo:
                    continue

                visited.add(voisin)
                parents_children[voisin] = (x, y)
                to_visit.append(voisin)

        path: list[tuple[int, int]] = []
        current_position: tuple[int, int] | None = self.END
        while current_position is not None:
            path.append(current_position)
            current_position = parents_children[current_position]
        path.reverse()
        return path

    def imperfect_gen(
        self,
        cells: dict[tuple[int, int], list[int]]
       ) -> None:
        """Transform a perfect maze into an imperfect maze.

        This method removes dead ends by opening additional passages between
        adjacent cells while preserving the forbidden cells defined by the
        FT logo.

        Args:
            cells: Dictionary containing the maze cells and their wall data.
        """
        ft = self.create_ft()
        deadend_check = [7, 11, 13, 14]
        for x in range(0, self.WIDTH):
            for y in range(0, self.HEIGHT):
                if cells[(x, y)][1] in deadend_check and (x, y) not in ft:
                    possibility = [1, 2, 3, 4]
                    while cells[(x, y)][1] in deadend_check and len(
                            possibility) != 0:
                        z = choice(possibility)
                        if z == 1 and x > 0 and cells[(x, y)][1] != 7 and (
                                x - 1, y) not in ft:  # west
                            cells[(x, y)][1] = cells[(x, y)][1] - 8
                            cells[(x - 1, y)][1] = cells[(x - 1, y)][1] - 2

                        if z == 2 and y < self.HEIGHT - 1 and cells[(
                                x, y)][1] != 11 and (x, y + 1) not in ft:
                            cells[(x, y)][1] = cells[(x, y)][1] - 4
                            cells[(x, y + 1)][1] = cells[(x, y + 1)][1] - 1

                        if z == 3 and x < self.WIDTH - 1 and cells[(
                                x, y)][1] != 13 and (x + 1, y) not in ft:
                            cells[(x, y)][1] = cells[(x, y)][1] - 2
                            cells[(x + 1, y)][1] = cells[(x + 1, y)][1] - 8

                        if z == 4 and y > 0 and cells[(x, y)][1] != 14 and (
                                x, y - 1) not in ft:  # north
                            cells[(x, y)][1] = cells[(x, y)][1] - 1
                            cells[(x, y - 1)][1] = cells[(x, y - 1)][1] - 4
                        possibility.remove(z)
        for x in range(0, self.WIDTH - 3):  # ajout gestion gros trou
            for y in range(0, self.HEIGHT - 3):
                if (cells[(x, y)][1] >> 3) & 1 == 0 \
                    and (cells[(x + 1, y)][1] >> 3) & 1 == 0\
                    and (cells[(x + 2, y)][1] >> 3) & 1 == 0\
                    and (cells[(x, y + 1)][1] >> 3) & 1 == 0 \
                    and (cells[(x + 1, y + 1)][1] >> 3) & 1 == 0\
                    and (cells[(x + 2, y + 1)][1] >> 3) & 1 == 0\
                    and cells[(x, y + 1)][1] & 1 == 0 \
                    and cells[(x + 1, y + 1)][1] & 1 == 0\
                   and cells[(x + 2, y + 1)][1] & 1 == 0:
                    cells[(x + 1, y)][1] = cells[(x + 1, y)][1] + 4
                    cells[(x + 1, y + 1)][1] = cells[(x + 1, y + 1)][1] + 1
                if (cells[(x, y)][1] >> 2) & 1 == 0 \
                    and (cells[(x, y + 1)][1] >> 2) & 1 == 0\
                    and (cells[(x, y + 2)][1] >> 2) & 1 == 0\
                    and (cells[(x + 1, y)][1] >> 2) & 1 == 0 \
                    and (cells[(x + 1, y + 1)][1] >> 2) & 1 == 0\
                    and (cells[(x + 1, y + 2)][1] >> 2) & 1 == 0\
                    and (cells[(x, y)][1] >> 1) & 1 == 0 \
                    and (cells[(x, y + 1)][1] >> 1) & 1 == 0\
                   and (cells[(x, y + 2)][1] >> 1) & 1 == 0:
                    cells[(x, y + 1)][1] = cells[(x, y + 1)][1] + 2
                    cells[(x + 1, y + 1)][1] = cells[(x + 1, y + 1)][1] + 8

    def maze_gen(self) -> dict[tuple[int, int], list[int]]:
        """Generate a perfect maze using randomized cell connections.

        The method progressively connects neighboring cells that belong to
        different groups until all accessible cells form a single connected
        structure. Cells occupied by the FT logo remain blocked.

        Returns:
            A dictionary mapping each cell coordinate to a list containing
            its group identifier and its wall value.
        """
        seed(self.SEED)
        ft = self.create_ft()
        cells: dict[tuple[int, int], list[int]] = {}
        i = 1
        for x in range(0, self.WIDTH):
            for y in range(0, self.HEIGHT):
                cells[(x, y)] = [i, 15]
                i += 1
        while all(v[0] == 1 for v in cells.values()) is not True:
            x = randint(0, self.WIDTH - 1)
            y = randint(0, self.HEIGHT - 1)
            if (x, y) not in ft:
                check = 0
                possibility = [1, 2, 3, 4]
                while check != 1 and len(possibility) != 0:
                    z = choice(possibility)
                    if z == 1 and x > 0:  # west
                        if cells[(x, y)][0] != cells[(x - 1, y)][0] and (
                                x - 1, y) not in ft:
                            cells[(x, y)][1] = cells[(x, y)][1] - 8
                            cells[(x - 1, y)][1] = cells[(x - 1, y)][1] - 2
                            check = 1
                            reg = min(cells[(x, y)][0], cells[(x - 1, y)][0])
                            to_change = max(
                                cells[(x, y)][0], cells[(x - 1, y)][0]
                                )
                            cells[(x, y)][0] = reg
                            cells[(x - 1, y)][0] = reg
                            for k in cells:
                                if cells[k][0] == to_change:
                                    cells[k][0] = reg
                    if z == 2 and y < self.HEIGHT - 1:  # south
                        if cells[(x, y)][0] != cells[(x, y + 1)][0] and (
                                x, y + 1) not in ft:
                            cells[(x, y)][1] = cells[(x, y)][1] - 4
                            cells[(x, y + 1)][1] = cells[(x, y + 1)][1] - 1
                            check = 1
                            reg = min(cells[(x, y)][0], cells[(x, y + 1)][0])
                            to_change = max(
                                cells[(x, y)][0], cells[(x, y + 1)][0]
                                )
                            cells[(x, y)][0] = reg
                            cells[(x, y + 1)][0] = reg
                            for k in cells:
                                if cells[k][0] == to_change:
                                    cells[k][0] = reg
                    if z == 3 and x < self.WIDTH - 1:  # east
                        if cells[(x, y)][0] != cells[(x + 1, y)][0] and (
                                x + 1, y) not in ft:
                            cells[(x, y)][1] = cells[(x, y)][1] - 2
                            cells[(x + 1, y)][1] = cells[(x + 1, y)][1] - 8
                            check = 1
                            reg = min(cells[(x, y)][0], cells[(x + 1, y)][0])
                            to_change = max(
                                cells[(x, y)][0], cells[(x + 1, y)][0]
                                )
                            cells[(x, y)][0] = reg
                            cells[(x + 1, y)][0] = reg
                            for k in cells:
                                if cells[k][0] == to_change:
                                    cells[k][0] = reg
                    if z == 4 and y > 0:  # north
                        if cells[(x, y)][0] != cells[(x, y - 1)][0] and (
                                x, y - 1) not in ft:
                            cells[(x, y)][1] = cells[(x, y)][1] - 1
                            cells[(x, y - 1)][1] = cells[(x, y - 1)][1] - 4
                            check = 1
                            reg = min(cells[(x, y)][0], cells[(x, y - 1)][0])
                            to_change = max(
                                cells[(x, y)][0], cells[(x, y - 1)][0]
                                )
                            cells[(x, y)][0] = reg
                            cells[(x, y - 1)][0] = reg
                            for k in cells:
                                if cells[k][0] == to_change:
                                    cells[k][0] = reg
                    possibility.remove(z)
            else:
                cells[(x, y)][0] = 1
        return cells

    def create_ft(self) -> list[tuple[int, int]]:
        """Create the coordinates of the centered FT logo.

        The logo is generated only if the maze dimensions are large enough
        to contain it. Otherwise, an empty list is returned.

        Returns:
            A list of cell coordinates forming the FT logo.
        """
        ft: list[tuple[int, int]] = []
        if self.WIDTH < 9 or self.HEIGHT < 7:
            return ft
        x = floor(self.WIDTH / 2 - 3)
        y = ceil(self.HEIGHT / 2 - 3)
        moves = [
            (0, 0), (0, 1), (0, 1), (1, 0), (1, 0),
            (0, 1), (0, 1), (4, 0), (-1, 0), (-1, 0),
            (0, -1), (0, -1), (1, 0), (1, 0), (0, -1), (0, -1),
            (-1, 0), (-1, 0),
        ]
        for dx, dy in moves:
            x += dx
            y += dy
            ft.append((x, y))
        return ft

    def verif_config(self) -> None:
        """Validate the maze configuration.

        This method checks that the maze dimensions are valid and ensures
        that the entrance and exit are distinct and do not overlap the FT
        logo.

        Raises:
            ValueError: If the maze dimensions are invalid, the entrance and
                exit are identical, or either position belongs to the FT
                logo.
        """
        if self.WIDTH < 1 or self.HEIGHT < 1:
            raise ValueError(
                "La largeur et la hauteur doivent etre superieur a 0."
                            )
        if self.START == self.END:
            raise ValueError("L'entrée et la sortie doivent etre differentes.")

        ft = self.create_ft()
        if self.START in ft:
            raise ValueError("L'entrée ne peut pas être dans le logo 42.")
        if self.END in ft:
            raise ValueError("La sortie ne peut pas être dans le logo 42.")

    def new_config(self) -> None:
        """Load and validate the maze configuration from a file.

        This method reads the configuration file provided as a command-line
        argument, parses its key-value pairs, and initializes the maze
        settings. It also validates the configuration by checking for
        duplicate keys, missing mandatory fields, and invalid values.

        Raises:
            ValueError: If the configuration file is invalid, contains
                duplicate or missing mandatory keys, invalid dimensions,
                out-of-bounds coordinates, or an incorrect number of
                command-line arguments.
        """
        prefix: str = ""
        seen: set[str] = set()
        mandatory = {
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
        }
        if len(sys.argv) != 2:
            raise ValueError("Trop ou trop peu d'arguments")
        name_file = sys.argv[1]

        with open(name_file, "r") as f:
            values = f.read().split("\n")
        for i in range(len(values)):
            if values[i].startswith("#"):
                continue
            index_start = values[i].find("=") + 1
            if index_start == -1:
                continue
            prefix = values[i][:index_start - 1]
            values[i] = values[i][index_start:]
            if prefix in seen:
                raise ValueError()
            if prefix == "WIDTH":
                self.WIDTH = int(values[i])
                seen.add(prefix)
            if prefix == "HEIGHT":
                self.HEIGHT = int(values[i])
                seen.add(prefix)
            if prefix == "ENTRY":
                x, y = values[i].split(",", 1)
                self.START = (int(x), int(y))
                if self.START[0] >= self.WIDTH \
                    or self.START[1] >= self.HEIGHT \
                    or self.START[0] < 0 \
                   or self.START[1] < 0:
                    raise ValueError(
                        "Les coordonnee d'entree doivent etre dans "
                        "le labyrinthe"
                        )
                seen.add(prefix)
            if prefix == "EXIT":
                x, y = values[i].split(",", 1)
                self.END = (int(x), int(y))
                if self.END[0] >= self.WIDTH \
                    or self.END[1] >= self.HEIGHT \
                    or self.END[0] < 0 \
                   or self.END[1] < 0:
                    raise ValueError(
                        "Les coordonnee de sortie doivent etre dans le "
                        "labyrinthe"
                        )
                seen.add(prefix)
            if prefix == "OUTPUT_FILE":
                self.OUTPUT_FILE = str(values[i])
                seen.add(prefix)
            if prefix == "PERFECT":
                self.PERFECT = values[i].strip().lower() == "true"
                seen.add(prefix)
            if prefix == "SEED":
                self.SEED = int(values[i])
                seen.add(prefix)
        missing = mandatory - seen
        if missing:
            raise ValueError("All mandatory part are not in the config file")

    def maze_show(
            self,
            cells: dict[tuple[int, int], list[int]],
            color: str,
            path: list[tuple[int, int]] | None = None
            ) -> None:
        """Display the maze and its optional solution path.

        The maze is displayed in the terminal using colored characters.
        The entrance, exit, FT logo, and solution path are represented with
        distinct colors when a path is provided.

        Args:
            cells: Dictionary containing the maze cells and their wall data.
            color: ANSI color code used to display the maze walls.
            path: Optional ordered list of coordinates representing the
                solution path.
        """
        if path is None:
            path = []
        if self.WIDTH < 9 or self.HEIGHT < 7:
            print("Too small to print 42 !!")
        ft = self.create_ft()
        for _ in range(self.WIDTH):
            print(f"{color}████", end="")
        print("██")
        for y in range(self.HEIGHT):
            print(f"{color}█", end="")
            for x in range(self.WIDTH):

                west = ((cells[(x, y)][1] >> 3) & 1) == 0
                east = ((cells[(x, y)][1] >> 1) & 1) == 0

                if west and (x - 1, y) in path:
                    left = f"{Color.FD_GREEN} "
                elif west:
                    left = f"{Color.RESET} "
                else:
                    left = f"{color}█"

                if east and (x + 1, y) in path:
                    right = f"{Color.FD_GREEN} "
                elif east:
                    right = f"{Color.RESET} "
                else:
                    right = f"{color}█"

                if (x, y) == self.START:
                    print(f"{left}{
                        Color.FD_BLUE}  ​{right}{Color.RESET}{color}",
                            end="")
                    continue
                elif (x, y) == self.END:
                    print(f"{left}{
                        Color.FD_BROWN}  ​{right}{Color.RESET}{color}",
                            end="")
                    continue

                if (x, y) in ft:
                    print(f"█{Color.BLUE}██{color}█", end="")
                elif (x, y) in path:
                    west = ((cells[(x, y)][1] >> 3) & 1) == 0
                    east = ((cells[(x, y)][1] >> 1) & 1) == 0

                    if west and (x - 1, y) in path:
                        left = f"{Color.FD_GREEN} "
                    elif west:
                        left = f"{Color.RESET} "
                    else:
                        left = f"{color}█"

                    if east and (x + 1, y) in path:
                        right = f"{Color.FD_GREEN} "
                    elif east:
                        right = f"{Color.RESET} "
                    else:
                        right = f"{color}█"

                    print(f"{left}{
                        Color.FD_GREEN}  ​{right}{Color.RESET}{color}",
                            end="")
                else:
                    west = ((cells[(x, y)][1] >> 3) & 1) == 0
                    east = ((cells[(x, y)][1] >> 1) & 1) == 0
                    left = " " if west else "█"
                    right = " " if east else "█"
                    print(f"{left}  ​{right}", end="")
            print("█")
            print("█", end="")
            for x in range(self.WIDTH):
                if ((cells[(x, y)][1] >> 2) & 1) == 0:
                    if (x, y) in path and (x, y + 1) in path:
                        print(f"{color}█{Color.FD_GREEN}  ​█{Color.RESET}",
                              end="")
                    else:
                        print(f"{color}█  ​█", end="")
                else:
                    print(f"{color}████", end="")
            print(f"{color}█{Color.RESET}")

    def main(self) -> dict[tuple[int, int], list[int]]:
        """Generate the maze from the loaded configuration.

        This method loads and validates the configuration, generates a
        perfect maze, optionally transforms it into an imperfect maze,
        solves it, writes the result to the output file, and returns the
        generated cells.

        Returns:
            A dictionary mapping each cell coordinate to its group identifier
            and wall value.
        """
        try:
            self.new_config()
            self.verif_config()
        except Exception as e:
            print(e)
            exit()
        cells: dict[tuple[int, int], list[int]] = self.maze_gen()
        if self.PERFECT is False:
            self.imperfect_gen(cells)
        self.output(cells, self.solve_maze(cells))
        return cells


if __name__ == "__main__":
    Maze = MazeGenerator()
    cells = Maze.main()
    color = Color.WHITE
    Maze.maze_show(cells, color)
    show_path: bool = False
    while True:
        inp = None
        try:
            inp = input("1: regen\n2: change color\n3: show/hide path\n"
                        + "4: perfect/imperfect\n0: quit\nYour choice:")
        except (KeyboardInterrupt, EOFError):
            exit()
        if inp == "1":
            if show_path is True:
                cells = Maze.maze_gen()
                if Maze.PERFECT is False:
                    Maze.imperfect_gen(cells)
                Maze.output(cells, Maze.solve_maze(cells))
                Maze.maze_show(cells, color, Maze.solve_maze(cells))
            else:
                cells = Maze.maze_gen()
                if Maze.PERFECT is False:
                    Maze.imperfect_gen(cells)
                Maze.output(cells, Maze.solve_maze(cells))
                Maze.maze_show(cells, color)
        elif inp == "2":
            if color == Color.WHITE:
                color = Color.RED
            elif color == Color.RED:
                color = Color.CYAN
            elif color == Color.CYAN:
                color = Color.MAGENTA
            else:
                color = Color.WHITE

            if show_path is True:
                Maze.maze_show(cells, color, Maze.solve_maze(cells))
            else:
                Maze.maze_show(cells, color)
        elif inp == "3":
            if show_path is True:
                show_path = False
            else:
                show_path = True
            if show_path is True:
                Maze.maze_show(cells, color, Maze.solve_maze(cells))
            else:
                Maze.maze_show(cells, color)
        elif inp == "4":
            if Maze.PERFECT is True:
                Maze.PERFECT = False
            else:
                Maze.PERFECT = True
            if show_path is True:
                cells = Maze.maze_gen()
                if Maze.PERFECT is False:
                    Maze.imperfect_gen(cells)
                Maze.output(cells, Maze.solve_maze(cells))
                Maze.maze_show(cells, color, Maze.solve_maze(cells))
            else:
                cells = Maze.maze_gen()
                if Maze.PERFECT is False:
                    Maze.imperfect_gen(cells)
                Maze.output(cells, Maze.solve_maze(cells))
                Maze.maze_show(cells, color)
        elif inp == "0":
            break
        else:
            print("\nERROR: Wrong input\n")
