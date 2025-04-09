import heapq
import math

def A_Star(g, src, dest, h):
    openQueue = []
    heapq.heappush(openQueue, (1, src))
    
    predecessor = {}
    minCost = {node: float('inf') for node in g}
    minCost[src] = 0
    
    predCost = {node: float('inf') for node in g}
    predCost[src] = h(src)
    
    while openQueue:
        _, current = heapq.heappop(openQueue)
        
        if current == dest:
            return reconstruct_path(predecessor, current)
        
        for neighbour, connection_data in g[current].items():
            cost = connection_data['distance']
            tentative_minCost = minCost[current] + cost
            
            if tentative_minCost < minCost[neighbour]:
                predecessor[neighbour] = current
                minCost[neighbour] = tentative_minCost
                predCost[neighbour] = tentative_minCost + h(neighbour)
                
                heapq.heappush(openQueue, (predCost[neighbour], neighbour))
    
    return None

def reconstruct_path(predecessor, current):
    path = []
    while current in predecessor:
        path.append(current)
        current = predecessor[current]
    path.append(current)
    path.reverse()
    return path

def manhattan_heuristic(goal_node, node_positions):
    goal_lat, goal_lon = node_positions[goal_node]
    def heuristic(node_id):
        lat, lon = node_positions[node_id]
        return abs(goal_lat - lat) + abs(goal_lon - lon)
    return heuristic



def euclidean_heuristic(goal_node, node_positions):
    goal_lat, goal_lon = node_positions[goal_node]
    def heuristic(node_id):
        lat, lon = node_positions[node_id]
        return math.sqrt((goal_lat - lat) ** 2 + (goal_lon - lon) ** 2)
    return heuristic

def diagonal_heuristic(goal_node, node_positions):
    goal_lat, goal_lon = node_positions[goal_node]
    def heuristic(node_id):
        lat, lon = node_positions[node_id]
        dx = abs(goal_lat - lat)
        dy = abs(goal_lon - lon)
        return max(dx, dy)
    return heuristic
