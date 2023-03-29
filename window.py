"""
This python module is responsible for the visual and interactive aspect of our project.

The simulation begins by calling create_window with a valid maze, and then the user can interact with
the window using the arrow keys to control their player around the maze with the goal of reaching the
bottom right corner.

If at any point the player wants to give up and see the correct solution for the maze, they can do so
by pressing the spacebar.
"""

import sys
import pygame

from main import Maze


def create_window(maze: Maze) -> None:
    """
    function that creates the pygame window and handles the main game loop that allows for player movement
    through the maze as well as showing the correct path when necessary.
    """
    # PLAYER DATA
    # player and trail color
    pcolor = (255, 0, 0)
    # flag representing if we are currently dispalaying the correct path
    displaying_answer = False
    # position of player
    x, y = 0, 0
    # list of cells the player has visited to draw path from start
    trail = []

    # precompute correct the path so that we can display it to the user when needed
    correct_path = maze.solve_maze()

    # setup pygame window
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Maze Runner')

    # main game loop (runs until the window is closed)
    while True:
        for event in pygame.event.get():
            # end process if the window is closed
            if event.type == pygame.QUIT:
                sys.exit(0)
            # if the player presses space, take away control and start displaying correct path
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                displaying_answer = True

                # reset position and trail to start, set player color to blue
                pcolor = (0, 0, 255)
                trail.clear()
                x, y = 0, 0
            # otherwise update player's position through movement
            elif not displaying_answer and event.type == pygame.KEYDOWN:
                x, y = update_position(event, x, y, maze)

            # if the player moved, add current position to the trail
            if len(trail) == 0 or trail[-1] != (x, y):
                trail.append((x, y))
            # if the player backtracks, delete last two steps of path
            if len(trail) >= 3 and trail[-1] == trail[-3]:
                trail.pop()
                trail.pop()

            # if the player reaches the end, stop controlling and set color to green
            if not displaying_answer and x == maze.size - 1 and y == maze.size - 1:
                pcolor = (0, 245, 0)
                displaying_answer = True

        # now that the game state is updated, draw the maze and player
        draw_maze(screen, maze, trail, pcolor)
        # display next frame to user
        pygame.display.update()

        # if showing answer add the next position to the trail
        if displaying_answer and len(trail) < len(correct_path):
            x, y = correct_path[len(trail)][0], correct_path[len(trail)][1]
            trail.append(correct_path[len(trail)])


def update_position(event: pygame.event.Event, x: int, y: int, maze: Maze) -> tuple[int, int]:
    """
    Check if movement keys have been pressed and update the player's position accordingly.
    This function returns the player's updated position as a tuple (x, y)

    Preconditions
     - (x, y) corresponds to a vertex in maze
     - event.type == pygame.KEYDOWN
    """
    if event.key == pygame.K_LEFT:
        # try moving left
        if (x - 1, y) in maze.get_neighbours((x, y)):
            x -= 1
    if event.key == pygame.K_RIGHT:
        # try moving right
        if (x + 1, y) in maze.get_neighbours((x, y)):
            x += 1
    if event.key == pygame.K_UP:
        # try moving up
        if (x, y - 1) in maze.get_neighbours((x, y)):
            y -= 1
    if event.key == pygame.K_DOWN:
        # try moving down
        if (x, y + 1) in maze.get_neighbours((x, y)):
            y += 1
    # return updated position
    return (x, y)


def draw_maze(screen: pygame.Surface, maze: Maze, trail: list[tuple[int, int]], pcolor: tuple[int, int, int]) -> None:
    """
    Draws all aspects of the maze onto the screen for the user to see.
    Specifically, this function draws the maze's walls, the player's trail, and highlights the ending cell.
    pcolor is a tuple that specifies the RGB color used to draw the player's trail.
    """
    # size of each grid square; larger mazes need smaller cell sizes to fit on the screen comfortably
    gsize = 500 / maze.size
    # x and y offsets from top left so that maze is centered in the window
    xo, yo = 150, 150

    # clear the screen (fill with white)
    screen.fill((255, 255, 255))

    # draw a yellow glow at ending cell
    pygame.draw.rect(screen, (250, 250, 0),
                     pygame.Rect(xo + (maze.size - 1) * gsize, yo + (maze.size - 1) * gsize, gsize, gsize))

    # draw a circle at every cell visited by trail (creates rounded corners effect)
    for cell in trail:
        pygame.draw.circle(screen, pcolor,
                           (xo + (cell[0] + 0.5) * gsize + 1, yo + (cell[1] + 0.5) * gsize + 1), 6)
    # draw lines connecting visited cells
    for i in range(1, len(trail)):
        pygame.draw.line(screen, pcolor,
                         (xo + (trail[i - 1][0] + 0.5) * gsize, yo + (trail[i - 1][1] + 0.5) * gsize),
                         (xo + (trail[i][0] + 0.5) * gsize, yo + (trail[i][1] + 0.5) * gsize), 12)
    # draw maze
    for i in range(0, maze.size):
        for j in range(0, maze.size):
            neighbours = maze.get_neighbours((i, j))

            # draw right wall if needed
            if (i + 1, j) not in neighbours:
                pygame.draw.line(screen, (0, 0, 0), (xo + (i + 1) * gsize, yo + j * gsize),
                                 (xo + (i + 1) * gsize, yo + (j + 1) * gsize), 4)
            # draw left wall if needed
            if (i - 1, j) not in neighbours:
                pygame.draw.line(screen, (0, 0, 0), (xo + i * gsize, yo + j * gsize),
                                 (xo + i * gsize, yo + (j + 1) * gsize), 4)
            # draw upper wall if needed
            if (i, j - 1) not in neighbours:
                pygame.draw.line(screen, (0, 0, 0), (xo + i * gsize, yo + j * gsize),
                                 (xo + (i + 1) * gsize, yo + j * gsize), 4)
            # draw lower wall if needed
            if (i, j + 1) not in neighbours:
                pygame.draw.line(screen, (0, 0, 0), (xo + i * gsize, yo + (j + 1) * gsize),
                                 (xo + (i + 1) * gsize, yo + (j + 1) * gsize), 4)
