import heapq

def dijkstra(G, source, k=None):
    pq = []
    heapq.heappush(pq, (0, source))
    
    distances = {node: float('inf') for node in G}
    distances[source] = 0
    
    paths = {node: [] for node in G}
    paths[source] = [source]
    
    relax_count = {node: 0 for node in G} if k else None
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        if current_dist > distances[u]:
            continue
            
        for v, edge_data in G[u].items():
            weight = edge_data['distance']
            
            if k and relax_count[v] >= k:
                continue
                
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                paths[v] = paths[u] + [v]
                if k:
                    relax_count[v] += 1
                heapq.heappush(pq, (distances[v], v))
    
    return distances, paths