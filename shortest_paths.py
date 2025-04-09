# shortest_paths.py
import heapq

def dijkstra(G, source, k):
    """
    Modified Dijkstra’s algorithm that allows at most k relaxations per node.
    G should be an instance of Graph (or a subclass).
    """
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
    """
    Modified Bellman-Ford algorithm with at most k iterations.
    """
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

def johnsons(G):
    """
    Johnson’s algorithm for computing all-pairs shortest paths.
    This function assumes G is a directed graph.
    """
    # Add a temporary node (-1) connected with zero-weight edges.
    G.adj[-1] = []
    for node in list(G.adj.keys()):
        if node != -1:
            G.adj[-1].append(node)
            G.weights[(-1, node)] = 0

    distances, _ = bellman_ford(G, -1, G.number_of_nodes() - 1)
    if distances is None:
        return "Negative Cycle"
    h = distances

    weightP = {}
    for (u, v), w in G.weights.items():
        if u != -1:
            weightP[(u, v)] = w + h[u] - h[v]

    distance_matrix = {}
    for u in list(G.adj.keys()):
        if u == -1:
            continue
        dijkstra_dist, _ = dijkstra(G, u, G.number_of_nodes() - 1)
        distance_matrix[u] = {v: dijkstra_dist[v] + h[v] - h[u] for v in dijkstra_dist}

    # Clean up the temporary node.
    del G.adj[-1]
    for node in G.adj:
        if -1 in G.adj[node]:
            G.adj[node].remove(-1)
    if -1 in distance_matrix:
        del distance_matrix[-1]
    for u in distance_matrix:
        if -1 in distance_matrix[u]:
            del distance_matrix[u][-1]

    return distance_matrix
