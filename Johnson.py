from Dijkstra_BellmanFord import *

def johnsons(G):

    G.adj[-1] = []
    for node in G.adj:
        if node != -1:
            G.adj[-1].append(node)
            G.weights[(-1,node)] = 0 

    distances, _ = bellman_ford(G, -1, G.number_of_nodes()-1)
    if distances is None:
        return "Negative Cycle"
    
    h = distances
    
    weightP = {}
    for  (u,v), w in G.weights.items():
        if u != -1:
            weightP[(u,v)] = w + h[u] - h[v]

    distance_matrix = {}
    for u in range(G.number_of_nodes() -1):
        dijkstra_dist, _ = dijkstra(G, u, G.number_of_nodes()-1)
        distance_matrix[u] = {
            v: dijkstra_dist[v] + h[v] - h[u] for v in dijkstra_dist
        }

    del G.adj[-1]
    for node in G.adj:
        G.adj[node] = [n for n in G.adj[node] if n != -1]
    del G.weights

    if -1 in distance_matrix:
        del distance_matrix[-1]
    for u in distance_matrix:
        if -1 in distance_matrix[u]:
            del distance_matrix[u][-1]

    return distance_matrix



def test_johnsons():
    G = create_random_directed_graph(10,15,25)
    
    shortest_paths = johnsons(G)
    
    print("Shortest Paths using Johnson's Algorithm:")
    for u in shortest_paths:
        for v in shortest_paths[u]:
            print(f"Distance from {u} to {v}: {shortest_paths[u][v]}")

test_johnsons()