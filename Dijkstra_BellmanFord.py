import heapq
import Draw_plot
import copy
import time
import random

class DirectedWeightedGraph:

    def __init__(self, nodes):
        self.adj = {}
        self.weights = {}
        for node in range(nodes):
            self.adj[node] = []

    def are_connected(self, node1, node2):
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]

    def number_of_nodes(self):
        return len(self.adj)
    

class UndirectedWeightedGraph:

    def __init__(self, nodes):
        self.adj = {}
        self.weights = {}
        for node in range(nodes):
            self.adj[node] = []

    def are_connected(self, node1, node2):
        return node2 in self.adj[node1]

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

        if node1 not in self.adj[node2]:
            self.adj[node2].append(node1)
        self.weights[(node2, node1)] = weight

    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]

    def number_of_nodes(self):
        return len(self.adj)
    
def create_random_undirected_graph(nodes, edges, max_weight):
    #too many edges
    if edges > (nodes*(nodes-1))//2:
        raise ValueError("Edges exceed the possible number for the given nodes")
    
    g = UndirectedWeightedGraph(nodes)
    #track edges to prevent duplicates
    edge_set = set() 

    while len(edge_set)< edges:
        node1,node2 = random.sample(range(nodes),2)
        weight = random.uniform(1, max_weight)

        if (node1,node2) not in edge_set and (node2,node1) not in edge_set:
            g.add_edge(node1,node2, weight)
            edge_set.add((node1,node2))

    return g

def create_random_directed_graph(nodes, edges, max_weight):
    if edges > nodes * (nodes - 1):
        raise ValueError("Edges exceed the possible number for the given nodes")

    g = DirectedWeightedGraph(nodes)
    edge_set = set()

    while len(edge_set) < edges:
        node1, node2 = random.sample(range(nodes), 2)
        weight = random.uniform(1, max_weight)

        if (node1, node2) not in edge_set:
            g.add_edge(node1, node2, weight)
            edge_set.add((node1, node2))

    return g

def dijkstra(G, source, k):
    N = G.number_of_nodes()

    pq = []
    heapq.heappush(pq, (0, source))

    distances = {node: float('inf') for node in G.adj}
    distances[source] = 0
    paths = {node: [] for node in G.adj}
    paths[source] = [source]

    relax_count = {node: 0 for node in G.adj}

    while pq:
        current_dist, u = heapq.heappop(pq)

        if current_dist > distances[u]:
            continue

        for v in G.adjacent_nodes(u):
            weight = G.w(u, v)
            if weight is None:
                continue

            if relax_count[v] >= k:
                continue

            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                paths[v] = paths[u] + [v]
                relax_count[v] += 1
                heapq.heappush(pq, (distances[v], v))

    return distances, paths

def bellman_ford(G, source, k):
    N = G.number_of_nodes()

    distances = {node: float('inf') for node in G.adj}
    distances[source] = 0
    paths = {node: [] for node in G.adj}
    paths[source] = [source]

    for _ in range(k):
        updated = False
        new_distances = distances.copy()

        for u in G.adj:
            if distances[u] == float('inf'):
                continue 

            for v in G.adjacent_nodes(u):
                weight = G.w(u, v)
                if weight is None:
                    continue

                if distances[u] + weight < new_distances[v]:
                    new_distances[v] = distances[u] + weight
                    paths[v] = paths[u] + [v]
                    updated = True

        if not updated:
            break  

        distances = new_distances 

    return distances, paths


def experiment():
    trials = 50
    nodes = 10
    edges = 45

    dijkstraTimes = []
    bellmanTimes = []

    for _ in range(trials):
        randGraph = create_random_undirected_graph(nodes,edges,25)
        randCopy = copy.copy(randGraph)

        source = random.choice(list(randGraph.adj.keys()))
        k = 2  #set relaxation limit

        start = time.time()
        dijkstra(randCopy,source,k)
        dijkstraTimes.append(time.time() - start)

        randCopy = copy.copy(randGraph)
        start = time.time()
        bellman_ford(randCopy,source,k)
        bellmanTimes.append(time.time() - start)

    Draw_plot.draw_plot({
            "Dijkstra": dijkstraTimes,
            "Bellman-Ford": bellmanTimes
        }, "Experiment 2.3")

    print("Dijkstra Output:", dijkstra(randCopy, source, k))
    print("Bellman-Ford Output:", bellman_ford(randCopy, source, k))

    return 0

experiment()