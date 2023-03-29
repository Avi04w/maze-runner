"""DOCSTRING"""

from maze import Maze
import window

if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['random', 'a3_network', 'a3_part1'],
        'disable': ['unused-import']
    })

    maze = Maze(40)  # Change this value to set the size of the maze (n x n)

    window.run(maze)
