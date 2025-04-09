# graph.py

class Graph:
    def __init__(self):
        self.adj = {}      # Dictionary: node -> list of adjacent nodes
        self.weights = {}  # Dictionary: (node1, node2) -> weight

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        self.add_node(node1)
        self.add_node(node2)
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def adjacent_nodes(self, node):
        return self.adj.get(node, [])

    def w(self, node1, node2):
        if node2 in self.adj.get(node1, []):
            return self.weights.get((node1, node2), None)
        return None

    def number_of_nodes(self):
        return len(self.adj)


class DirectedWeightedGraph(Graph):
    # Inherits everything from Graph without change.
    pass


class UndirectedWeightedGraph(Graph):
    def add_edge(self, node1, node2, weight):
        # For undirected graph, we add edges both ways.
        self.add_node(node1)
        self.add_node(node2)
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        if node1 not in self.adj[node2]:
            self.adj[node2].append(node1)
        self.weights[(node1, node2)] = weight
        self.weights[(node2, node1)] = weight
