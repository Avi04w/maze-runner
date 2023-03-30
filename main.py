"""CSC111 Winter 2023 Course Project: MazeRunner

===============================

This is the main module which can be used to run the main program that we created.
When run, it will create an n x n size maze and allow the user to play it.

Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Avi Walia, Alex Yao, Sarina Li, Anthony Nicholas Fetelya
"""
from maze import Maze
import window

if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['random', 'maze', 'window'],
        'disable': ['unused-import']
    })

    maze = Maze(30)  # Change this value to set the size of the maze (n x n)

    # maze = Maze(40)  # Creates large maze

    # maze = Maze(10)  # Creates small maze

    window.create_window(maze)
