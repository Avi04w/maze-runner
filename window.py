"""DOCSTRING"""

import pygame
import sys
from maze import Maze

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

mode: bool
correct_path = []


def run(maze: Maze) -> None:
    """DOCSTRING"""
    cell_size = 500 / maze.size
    player_color = (255, 0, 0)

    # user is controlling the player
    displaying_answer = False

    # position of player
    x, y = 0, 0

    # x and y offsets to center the graph
    xo, yo = 150, 150

    # list of cells the player has visited to draw path from start
    trail = [(0, 0)]

    correct_path = maze.solve_maze()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Maze Runner')

    while True:
        # clear the screen
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            # end process if they close the window
            if event.type == pygame.QUIT:
                sys.exit(0)
            # handle user input
            if not displaying_answer and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # try moving left
                    if (x - 1, y) in maze.get_neighbours((x, y)):
                        x -= 1
                        trail.append((x, y))
                if event.key == pygame.K_RIGHT:
                    # try moving right
                    if (x + 1, y) in maze.get_neighbours((x, y)):
                        x += 1
                        trail.append((x, y))
                if event.key == pygame.K_UP:
                    # try moving up
                    if (x, y - 1) in maze.get_neighbours((x, y)):
                        y -= 1
                        trail.append((x, y))
                if event.key == pygame.K_DOWN:
                    # try moving down
                    if (x, y + 1) in maze.get_neighbours((x, y)):
                        y += 1
                        trail.append((x, y))

                # if the player presses space, take away control and start displaying correct path
                if event.key == pygame.K_SPACE:
                    displaying_answer = True

                    # reset position and trail to start, set player color to blue
                    x, y = 0, 0
                    trail.clear()
                    player_color = (0, 0, 255)

                # if the player backtracks, delete last two steps of path
                if len(trail) >= 3 and trail[-1] == trail[-3]:
                    trail.pop()
                    trail.pop()

        # if the player reaches the end, stop controlling
        if x == maze.size - 1 and y == maze.size - 1:
            player_color = (0, 255, 0)
            displaying_answer = True

        # keep updating players position along the correct path when showing answer
        if displaying_answer and len(trail) < len(correct_path):
            x, y = correct_path[len(trail)][0], correct_path[len(trail)][1]
            trail.append(correct_path[len(trail)])

        # draw yellow square at end cell

        pygame.draw.rect(screen, (250, 250, 0),
                         pygame.Rect(xo + (maze.size - 1) * cell_size, yo + (maze.size - 1) * cell_size, cell_size,
                                     cell_size))

        # draw trail
        for i in range(0, len(trail)):
            pygame.draw.circle(screen, player_color,
                               (xo + (trail[i][0] + 0.5) * cell_size + 1, yo + (trail[i][1] + 0.5) * cell_size + 1), 6)
        for i in range(1, len(trail)):
            pygame.draw.line(screen, player_color,
                             (xo + (trail[i - 1][0] + 0.5) * cell_size, yo + (trail[i - 1][1] + 0.5) * cell_size),
                             (xo + (trail[i][0] + 0.5) * cell_size, yo + (trail[i][1] + 0.5) * cell_size), 12)
        # draw player
        pygame.draw.circle(screen, player_color, (xo + (x + 0.5) * cell_size, yo + (y + 0.5) * cell_size),
                           int(cell_size * 0.3))

        # draw maze
        for i in range(0, maze.size):
            for j in range(0, maze.size):
                neighbours = maze.get_neighbours((i, j))

                # draw right wall if needed
                if (i + 1, j) not in neighbours:
                    pygame.draw.line(screen, (0, 0, 0), (xo + (i + 1) * cell_size, yo + j * cell_size),
                                     (xo + (i + 1) * cell_size, yo + (j + 1) * cell_size), 4)
                # draw left wall if needed
                if (i - 1, j) not in neighbours:
                    pygame.draw.line(screen, (0, 0, 0), (xo + i * cell_size, yo + j * cell_size),
                                     (xo + i * cell_size, yo + (j + 1) * cell_size), 4)
                # draw upper wall if needed
                if (i, j - 1) not in neighbours:
                    pygame.draw.line(screen, (0, 0, 0), (xo + i * cell_size, yo + j * cell_size),
                                     (xo + (i + 1) * cell_size, yo + j * cell_size), 4)
                # draw lower wall if needed
                if (i, j + 1) not in neighbours:
                    pygame.draw.line(screen, (0, 0, 0), (xo + i * cell_size, yo + (j + 1) * cell_size),
                                     (xo + (i + 1) * cell_size, yo + (j + 1) * cell_size), 4)

        pygame.display.update()


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['random', 'a3_network', 'a3_part1'],
        'disable': ['unused-import']
    })
