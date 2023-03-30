"""CSC111 Winter 2023 Course Project: MazeRunner

===============================

This module contains the functions neccessary to create the maze.

It also containes the functions neccessary to solve the maze and return the list of moves
of the shortest path to solve it.

Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Avi Walia, Alex Yao, Sarina Li, Anthony Nicholas Fetelya
"""

from __future__ import annotations
import random
from typing import Any


class _Vertex:
    """A vertex that represents a spoit in the maze.

        Instance Attributes
        - item:
            The location of this vertex, saved as a tuple (x, y)
        - neighbours:
            The vertices that are connected with the Vertex.
            2 connected vertices means that there exists a path between them.

        Representation Invariants:
        - self not in self.neighbours
        """
    item: tuple[int, int]
    neighbours: set[_Vertex]

    def __init__(self, item: tuple[int, int], neighbours: set[_Vertex]) -> None:
        self.item = item
        self.neighbours = neighbours


class Maze:
    """A Maze.

        Instance Attributes
        - size:
            The size of the maze (will be a square of size x size)

        Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
        """
    # Private Instance Attributes:
    #     - _vertices: A collection of the vertices contained in this graph.
    #                  Maps item to _Vertex instance.
    _vertices: dict[tuple[int, int], _Vertex]
    size: int

    def __init__(self, size: int) -> None:
        """Initialize a new maze.

        We capped the size of the maze (sidelength) to be 40 to stop recursion errors
        from occurring with too large and complex mazes.

        Preconditions:
            - size <= 40
        """
        self.size = size
        self._vertices = {}

        # make 2-d grid of vertices
        for i in range(size):
            for j in range(size):
                self.add_vertex((i, j))

        # start point
        start = _Vertex((0, 0), set())

        # Generate paths
        self.make_maze(start, set())

    def make_maze(self, vertex: _Vertex, visited: set[_Vertex]) -> None:
        """This functions creates a maze.

        Takes a list of unconnected vertices and creates a Minimum Spanning Tree.
        This ensures that every vertex is connected.
        This means that there is always a path to the end of the maze.

        Conceptually, every spot on the maze is surrounded by 4 walls, and by connecting 2 vertices,
        we are removing the wall between them, creating a path.

        Preconditions:
            - all(len(v.neighbours) == 0 for v in self._vertices)
            - The maze is solvable
        """
        visited.add(vertex)
        neighbours = self.in_bound_neighbours(vertex, visited)
        neighbour = None
        if neighbours:
            neighbour = random.choice(neighbours)
        while neighbour is not None:
            self.add_edge(vertex.item, neighbour.item)
            self.make_maze(neighbour, visited)
            neighbours = self.in_bound_neighbours(vertex, visited)
            neighbour = None
            if neighbours:
                neighbour = random.choice(neighbours)

    def solve_maze(self) -> list[tuple[int, int]]:
        """This functions solves the maze using a BFS algorithm.

        It returns a list of tuples which correspond to the path you must take to solve the maze.

        Preconditions:
            - vertex in self._vertices
            - The maze is solvable
        """
        queue = [[(0, 0)]]
        visited = set()
        while queue:
            path = queue.pop(0)
            node = path[-1]
            visited.add(node)
            if node == (self.size - 1, self.size - 1):
                return path
            for adj in self._vertices[node].neighbours:
                if adj.item not in visited:
                    new_path = list(path)
                    new_path.append(adj.item)
                    queue.append(new_path)

    def in_bound_neighbours(self, vertex: _Vertex, visited: set[_Vertex]) -> list[_Vertex]:
        """Returns a list of neighbouring vertices that may be potential neighbours to the given vertex.
        This incldues the vertices above, below, to the right, and to the left.

        If a potential neighbour is not in bounds or has already been visited,
        it is not included in the returned list.

        Preconditions:
            - vertex.item in self._vertices
        """
        address = vertex.item
        x_add = address[0]
        y_add = address[1]
        possible_neighbours = []

        # up direction
        if y_add > 0 and self._vertices[(x_add, y_add - 1)] not in visited:
            possible_neighbours.append(self._vertices[(x_add, y_add - 1)])
        # down direction
        if y_add < self.size - 1 and self._vertices[(x_add, y_add + 1)] not in visited:
            possible_neighbours.append(self._vertices[(x_add, y_add + 1)])
        # left direction
        if x_add > 0 and self._vertices[(x_add - 1, y_add)] not in visited:
            possible_neighbours.append(self._vertices[(x_add - 1, y_add)])
        # right direction
        if x_add < self.size - 1 and self._vertices[(x_add + 1, y_add)] not in visited:
            possible_neighbours.append(self._vertices[(x_add + 1, y_add)])

        return possible_neighbours

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph. The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        self._vertices[item] = _Vertex(item, set())

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.
        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['random'],
        'disable': ['unused-import']
    })
