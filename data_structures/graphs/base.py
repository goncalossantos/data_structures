import operator
from collections import defaultdict, deque, namedtuple
from math import inf
from typing import List, Dict, Set

from data_structures.queues.priority_queue import MinHeap

# TODO: Build a builder for the Graph class
# TODO: Subclass the graph class to handle max nodes
# TODO: Handle construction of graph better better
# TODO: Subclass different types of graphs
# TODO: Krustal's MST beginning is a mess
# TODO: Read Union-Find by rank and understand difference
# TODO: These MST algos really belong in their own file, not inside the graph class

Edge = namedtuple("Edge", ["source", "destination", "weight"])


class Graph:
    """ This class represents a directed graph using adjacency
    list representation

    Interface:
        Graph(number_of_nodes) -> constructor
        build() -> build from list of lists
        add_edge(u,v,weight) -> add an edge between nodes u an v with weight

    """

    def __init__(self, vertices: int = None) -> None:
        """ Constructor

        :param vertices: Size of graph - This is optional
        """
        if vertices is not None:
            assert isinstance(vertices, int)
        self.v = vertices
        # Default dictionary to store graph
        self.graph = defaultdict(list)  # type: Dict[int, List]
        self._matrix = None

    def __len__(self):

        if self.v is not None:
            return self.v
        else:
            return len(self.graph)

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        """ Adds an edge to the graph from u to v

        :param weight:
        :param u: origin node
        :param v: destination node
        """
        # If the graph was constructed with a max number of edges we must check for this
        if self.v is not None and self.v < len(self.graph):
            raise Exception("Graph's max size reached")

        # Checks if edge already exists - This makes adding slow
        new_edge = Edge(source=u, destination=v, weight=weight)
        if new_edge not in self.graph[u]:
            self.graph[u].append(new_edge)

    def bfs(self, source_node: int) -> List[int]:
        """
        
        :param source_node: Source node for BFS
        :return order: Final order in which nodes were visited
        """

        # Store visited order in a list
        order = list()  # type: List[int]

        # Mark all the vertices as not visited
        visited = [False] * (len(self))  # type: List[bool]

        # Create queue for BFS
        queue = deque()  # type: deque[int]

        # Mark the source node as visited and enqueue it
        queue.append(source_node)
        visited[source_node] = True

        while queue:
            next_node = queue.popleft()
            order.append(next_node)
            for edge in self.graph[next_node]:
                # Check the edge object
                assert isinstance(edge, Edge)
                assert isinstance(edge.destination, int)
                adjacent_node = edge.destination
                if visited[adjacent_node] is False:
                    queue.append(adjacent_node)
                    visited[adjacent_node] = True
        return order

    def recursive_dfs_util(self, next_node: int, visited: List[int], order: List[int]) -> List[int]:
        """ Utility function for recursive Depth First

        :param order: order in which nodes are visited
        :param next_node: next_node to be considered
        :param visited: List of booleans signifying visited nodes
        """

        # Mark the current node as visited and print it
        visited[next_node] = True
        order.append(next_node)

        for edge in self.graph[next_node]:
            # Check the edge object
            assert isinstance(edge, Edge)
            assert isinstance(edge.destination, int)
            adjacent_node = edge.destination
            if visited[adjacent_node] is False:
                order = self.recursive_dfs_util(adjacent_node, visited, order)

        return order

    def recursive_dfs(self, source_node: int) -> List[int]:
        """ Performs a recursive version of Depth First Search

        :param source_node: Source node for DFS
        :return order: Final order in which nodes were visited
        """

        # Store visited order in a list
        order = list()  # type: List[int]

        # Mark all the vertices as not visited
        visited = [False] * (len(self))  # type: List[bool]
        return self.recursive_dfs_util(source_node, visited, order)

    #
    def find_parent(self, parents_array: List[int], node_index: int) -> int:
        """ A utility function to find the subset of an element node_index

        :param parents_array:
        :param node_index:
        :return: Returns the final index of the node's parent
        """
        if parents_array[node_index] == -1:
            return node_index
        if parents_array[node_index] != -1:
            return self.find_parent(parents_array, parents_array[node_index])

    def union(self, parents_array: List[int], x: int, y: int) -> None:
        """ A utility function to do union of two subsets

        :param parents_array: marks the parent of each node
        :param x: First node to join
        :param y: Second node to join
        """
        x_set = self.find_parent(parents_array, x)
        y_set = self.find_parent(parents_array, y)
        parents_array[x_set] = y_set

    def contains_cycle(self) -> bool:
        """ The main function to check whether a given graph contains cycle or not

        This function assumes that there are no self loops in the graph

        :return: Returns True if a cycle is found, False if it isn't
        """
        # Allocate memory for creating V subsets and
        # Initialize all subsets as single element sets
        init_value = -1  # type: int
        parents_array = [init_value] * (len(self))  # type: List[int]

        for i in self.graph:
            for edge in self.graph[i]:
                assert isinstance(edge, Edge)
                assert isinstance(edge.destination, int)
                j = edge.destination
                if i == j:
                    # Self loop found
                    raise Exception("Graph has self loop")
                parent_of_i = self.find_parent(parents_array, i)
                parent_of_j = self.find_parent(parents_array, j)
                if parent_of_i == parent_of_j:
                    # Cycle found
                    return True
                self.union(parents_array, parent_of_i, parent_of_j)
        return False

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def kruskal_mst(self) -> List[Edge]:
        """ Computes the minimum spanning tree with Kruskal's method

        :return: returns a list with the minimum spanning tree
        """
        init_value = -1
        edges_so_far = 0  # type:int
        parents_array = [init_value] * (len(self))  # type: List[int]
        target_number_edges = len(self) - 1  # type: int
        result = list()  # type: List[Edge]

        sorted_edges = self.sort_edges_by_weight()  # type: List[Edge]
        for edge in sorted_edges:
            source, destination, _ = edge
            parent_source = self.find_parent(parents_array, source)
            parent_destination = self.find_parent(parents_array, destination)
            if parent_source != parent_destination:
                result.append(edge)
                edges_so_far += 1
                if edges_so_far == target_number_edges:
                    break
                self.union(parents_array=parents_array, x=parent_source, y=parent_destination)

        return result

    def sort_edges_by_weight(self) -> List[Edge]:
        """
        
        :return: List  of edges sorted by weight
        """
        edges_list = [edge for node in self.graph for edge in self.graph[node]]
        edges_list.sort(key=lambda x: x.weight)
        return edges_list

    def prim_mst(self):
        """ Computes the MST by Prim's algorithm

        This method uses the adjacency lists but works as if the graph was represented through adjacency matrix
        Time Complexity: O(N^2)


        :return:
        """

        # Set with all vertices in graph
        vertices = set(self.graph.keys())  # type: Set[int]

        # set that keeps track of vertices in mst
        mst_set = set()  # type: Set[int]
        # Assign a key value to all vertices in the input graph.
        # Initial value is inf for all but the first one
        keys = [inf] * len(self)  # type: List[float]
        keys[0] = 0.0

        result = set()  # type: Set[Edge]

        while mst_set != vertices:
            min_index = self.get_vertice_with_min_weight(keys, mst_set)  # O(2N) = O(N)
            mst_set.add(min_index)

            for edge in self.graph[min_index]:  # A node has at most V-1 Edges, so O(V)
                source, destination, weight = edge
                if weight < keys[destination]:
                    keys[destination] = float(weight)  # float to make it  consistent
                    result.add(edge)

        return result

    def prim_mst_with_heap(self):
        """ Computes the MST by Prim's algorithm

        This method uses the adjacency lists but works as if the graph was represented through adjacency matrix
        Time Complexity: O((V + E)log(V))


        :return:
        """

        # set that keeps track of vertices in mst
        mst_set = set()  # type: Set[int]
        # Assign a key value to all vertices in the input graph.
        # Initial value is inf for all but the first one
        keys = [inf] * len(self)  # type: List[float]
        keys[0] = 0.0
        priority_queue = MinHeap.build([(i, priority) for i, priority in enumerate(keys)])

        result = set()  # type: Set[Edge]

        while priority_queue:  # Priority queue has O(V) elements
            min_index = priority_queue.pop()  # O(log(V))
            mst_set.add(min_index)

            for edge in self.graph[min_index]:  # A graph has at most 2E Edges in adjacency list, so O(E)
                source, destination, weight = edge
                if priority_queue.contains_item(destination) and weight < keys[destination]:  # O(1)
                    keys[destination] = weight
                    priority_queue.push(item=destination, priority=weight)  # O(log(V))
                    result.add(edge)

        return result

    @property
    def adjacency_matrix(self):
        if not self._matrix:
            self._matrix = [[inf for item in range(len(self))] for item in range(len(self))]
            for i in range(len(self)):
                self._matrix[i][i] = 0.0
            for i in range(len(self)):
                for edge in self.graph[i]:
                    source, destination, weight = edge
                    self._matrix[source][destination] = weight
        return self._matrix



    @staticmethod
    def get_vertice_with_min_weight(keys: List[float], mst_set: Set[int]) -> int:
        """ Returns a vertix that isn't yet in mst_set and that has minimum weight in the keys list

        :param keys:
        :param mst_set:
        :return:
        """
        min_index, _ = min([i for i in enumerate(keys) if i[0] not in mst_set], key=operator.itemgetter(1))
        return min_index

    def __str__(self) -> str:
        """ Prints the graph by printing nodes and and their respective adjacent nodes

        """
        return str(self.adjacency_matrix)

    @classmethod
    def build(cls, adjacency_matrix):

        g = cls(len(adjacency_matrix))
        for row_index, column in enumerate(adjacency_matrix):
            for column_index, weight in enumerate(column):
                if weight != 0:
                    g.add_edge(row_index, column_index, weight)
        return g
