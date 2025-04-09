# a_star_adapter.py
import heapq
import math

def reconstruct_path(predecessor, current):
    path = []
    while current in predecessor:
        path.append(current)
        current = predecessor[current]
    path.append(current)
    path.reverse()
    return path

def A_Star(g, src, dest, h):
    """
    Standard A* algorithm that returns the shortest path from src to dest
    using heuristic function h. The heuristic function h should be a callable
    that takes a node and returns a float.
    """
    openQueue = []
    heapq.heappush(openQueue, (1, src))
    predecessor = {}
    minCost = {node: float('inf') for node in g.adj}
    minCost[src] = 0
    predCost = {node: float('inf') for node in g.adj}
    predCost[src] = h(src)

    while openQueue:
        _, current = heapq.heappop(openQueue)
        if current == dest:
            return reconstruct_path(predecessor, current)
        for neighbour in g.adj.get(current, []):
            cost = g.w(current, neighbour)
            tentative_minCost = minCost[current] + cost
            if tentative_minCost < minCost[neighbour]:
                predecessor[neighbour] = current
                minCost[neighbour] = tentative_minCost
                predCost[neighbour] = tentative_minCost + h(neighbour)
                heapq.heappush(openQueue, (predCost[neighbour], neighbour))
    return None

class AStarAdapter:
    def __init__(self, graph):
        self.graph = graph
        
    def find_shortest_path(self, source, destination, heuristic_func):
        """
        Finds the shortest path using the A* algorithm.
        :param source: starting node
        :param destination: target node
        :param heuristic_func: a callable that takes a node and returns a float
        """
        return A_Star(self.graph, source, destination, heuristic_func)

# Sample heuristic functions:
def manhattan_heuristic(goal, node_positions):
    goal_lat, goal_lon = node_positions[goal]
    return lambda node: abs(goal_lat - node_positions[node][0]) + abs(goal_lon - node_positions[node][1])

def euclidean_heuristic(goal, node_positions):
    goal_lat, goal_lon = node_positions[goal]
    return lambda node: math.sqrt((goal_lat - node_positions[node][0])**2 + (goal_lon - node_positions[node][1])**2)

def diagonal_heuristic(goal, node_positions):
    goal_lat, goal_lon = node_positions[goal]
    return lambda node: max(abs(goal_lat - node_positions[node][0]), abs(goal_lon - node_positions[node][1]))
