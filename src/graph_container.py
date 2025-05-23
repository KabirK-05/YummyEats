"""
This file represents the Graph data structure this project will use
"""
from __future__ import annotations
import math
from typing import Any, Union

import python_ta


class _Vertex:
    item: Any
    kind: str
    neighbours: dict[_Vertex, Union[int, float]]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'restaurant', 'location', 'rest_type', 'cuisines', 'approx_cost', 'other', 'user'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def cosine_similarity(self, other: _Vertex) -> float:
        """
        Compute the cosine similarity between this vertex and another
        see this link for cosine similarity formula:
        https://en.wikipedia.org/wiki/Cosine_similarity
        """
        intersect_set = {x for x in self.neighbours if x in other.neighbours}
        numerator = sum([self.neighbours[x] * other.neighbours[x] for x in intersect_set])
        den_a = math.sqrt(sum([self.neighbours[x] ** 2 for x in self.neighbours]))
        den_b = math.sqrt(sum([other.neighbours[x] ** 2 for x in other.neighbours]))

        return numerator / (den_a * den_b)


class Graph:
    """A graph used to represent a restaurant network.
    """
    # Private Instance Attributes:
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        Preconditions:
            - kind in {'restaurant', 'location', 'rest_type', 'cuisines', 'approx_cost', 'other', 'user'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def add_edge(self, item1: Any, item2: Any, weight: Union[int, float] = 5) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 are not in this graph

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.
        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'restaurant', 'location', 'rest_type', 'cuisines', 'approx_cost', 'other', 'user'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def get_weight(self, item1: Any, item2: Any) -> Union[int, float]:
        """Return the weight of the edge between the given items.

        Return 0 if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, 0)

    def average_weight(self, item: Any) -> float:
        """Return the average weight of the edges adjacent to the vertex corresponding to item.

        Raise ValueError if item does not corresponding to a vertex in the graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return sum(v.neighbours.values()) / len(v.neighbours)
        else:
            raise ValueError

    def total_weights(self, item: Any) -> float:
        """
        Return the combinations of all the weights connected to given vertex
        """
        total = 0
        for value in self.get_neighbours(item):
            total += self.get_weight(item, value)
        return total

    def get_similarity_score(self, item1: Any, item2: Any) -> float:
        """
        return the cosine similarity between two verticies
        """

        if item1 not in self._vertices or item2 not in self._vertices:
            raise ValueError

        v1 = self._vertices[item1]
        v2 = self._vertices[item2]

        return v1.cosine_similarity(v2)

    def get_degree(self, item) -> int:
        """
        Return the degree of the given item
        """
        if item not in self._vertices:
            raise ValueError
        v = self._vertices[item]
        return v.degree()


if __name__ == "__main__":
    python_ta.check_all(config={
        'extra-imports': ['annotations', 'math', 'Any', 'Union'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
