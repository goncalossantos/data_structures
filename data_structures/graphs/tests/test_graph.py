from math import inf
from unittest import TestCase

from data_structures.graphs.algorithms import dijkstra_shortest_path, floyd_warshall
from data_structures.graphs.base import Graph, Edge


def graph_for_transversal():
    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(4, 4)
    g.add_edge(2, 4)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(2, 3)
    g.add_edge(3, 3)
    g.add_edge(5, 5)
    g.add_edge(1, 5)
    return g


class TestGraph(TestCase):
    def test_prim_mst_with_heap(self):
        expected = set()
        expected.update([
            Edge(source=0, destination=1, weight=2),
            Edge(source=1, destination=2, weight=3),
            Edge(source=0, destination=3, weight=6),
            Edge(source=1, destination=4, weight=5),
        ])

        g = Graph(5)
        g.add_edge(0, 1, 2)
        g.add_edge(0, 3, 6)
        g.add_edge(1, 2, 3)
        g.add_edge(1, 3, 8)
        g.add_edge(2, 4, 7)
        g.add_edge(3, 4, 9)
        g.add_edge(1, 4, 5)

        assert g.prim_mst_with_heap() == expected

    def test_prim_mst(self):
        expected = set()
        expected.update([
            Edge(source=0, destination=1, weight=2),
            Edge(source=1, destination=2, weight=3),
            Edge(source=0, destination=3, weight=6),
            Edge(source=1, destination=4, weight=5),
        ])

        g = Graph(5)
        g.add_edge(0, 1, 2)
        g.add_edge(0, 3, 6)
        g.add_edge(1, 2, 3)
        g.add_edge(1, 3, 8)
        g.add_edge(2, 4, 7)
        g.add_edge(3, 4, 9)
        g.add_edge(1, 4, 5)
        # This symmetry is needed for adjacency matrix version
        g.add_edge(1, 0, 2)
        g.add_edge(3, 0, 6)
        g.add_edge(2, 1, 3)
        g.add_edge(3, 1, 8)
        g.add_edge(4, 2, 7)
        g.add_edge(4, 3, 9)
        g.add_edge(4, 1, 5)

        assert g.prim_mst() == expected

    def test_kruskal_mst(self):
        g = Graph(4)
        g.add_edge(0, 1, 10)
        g.add_edge(0, 2, 6)
        g.add_edge(0, 3, 5)
        g.add_edge(1, 3, 15)
        g.add_edge(2, 3, 4)
        expected = [
            Edge(source=2, destination=3, weight=4),
            Edge(source=0, destination=3, weight=5),
            Edge(source=0, destination=1, weight=10)
        ]
        assert g.kruskal_mst() == expected

    def test_cycle(self):
        """ Tests if the union-find algorithm for finding cycles is working

        :return:
        """
        g = Graph(3)
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        # g.add_edge(0, 0)
        assert g.contains_cycle() is False
        g.add_edge(1, 2)
        assert g.contains_cycle() is True

    def test_bfs(self):
        g = graph_for_transversal()
        assert g.bfs(0) == [0, 1, 2, 5, 4, 3]

    def test_recursive_dfs(self):
        g = graph_for_transversal()
        assert g.recursive_dfs(0) == [0, 1, 2, 4, 3, 5]


class TestDijkstraShortestPath(TestCase):
    matrix = [
        [0, 4, 0, 0, 0, 0, 0, 8, 0],
        [4, 0, 8, 0, 0, 0, 0, 11, 0],
        [0, 8, 0, 7, 0, 4, 0, 0, 2],
        [0, 0, 7, 0, 9, 14, 0, 0, 0],
        [0, 0, 0, 9, 0, 10, 0, 0, 0],
        [0, 0, 4, 14, 10, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 1, 6],
        [8, 11, 0, 0, 0, 0, 1, 0, 7],
        [0, 0, 2, 0, 0, 0, 6, 7, 0],
    ]

    def test_dijkstra_shortest_path(self):
        g = Graph.build(self.matrix)
        assert dijkstra_shortest_path(g, 0) == [0.0, 4.0, 12.0, 19.0, 21.0, 11.0, 9.0, 8.0, 15.0]


class TestFloydWarshall(TestCase):
    input_matrix = [
        [0.0, 5.0, inf, 10.0],
        [inf, 0.0, 3.0, inf],
        [inf, inf, 0.0, 1.0],
        [inf, inf, inf, 0.0],
    ]

    expected = [
        [0.0, 5.0, 8.0, 9.0],
        [inf, 0.0, 3.0, 4.0],
        [inf, inf, 0.0, 1.0],
        [inf, inf, inf, 0.0],
    ]

    def test_floyd_warshall(self):
        g = Graph.build(self.input_matrix)
        assert floyd_warshall(g.adjacency_matrix) == self.expected
