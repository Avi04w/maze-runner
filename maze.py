"""Docstring"""

from __future__ import annotations
import random
from typing import Any


class _Vertex:
    """Docstring"""
    item: tuple[int, int]
    neighbours: set[_Vertex]

    def __init__(self, item: tuple[int, int], neighbours: set[_Vertex]) -> None:
        self.item = item
        self.neighbours = neighbours


class Maze:
    """Docstring"""
    _vertices: dict[Any, _Vertex]
    size: int

    def __init__(self, size: int) -> None:
        self._vertices = {}
        self.size = size

        # make 2-d grid of vertices
        for i in range(size):
            for j in range(size):
                self.add_vertex((i, j))

        # start point
        start = _Vertex((0, 0), set())

        # Generate paths
        self.make_maze(start, set())

    def make_maze(self, vertex: _Vertex, visited: set[_Vertex]) -> None:
        """docstring"""
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
        """
        DOCSTRING
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
        """docstring"""
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
        'extra-imports': ['random', 'a3_network', 'a3_part1'],
        'disable': ['unused-import']
    })
