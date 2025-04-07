#Part 4

#Part 4.1

import heapq

class Graph():
    def __init__(self):
        self.adj = {}
        self.weights = {}

    def add_edge(self, u, v, weight):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append(v)
        self.weights[(u, v)] = weight

def reconstruct_path(predecessor, current):
    path = []
    while current in predecessor:
        path.append(current)
        current = predecessor[current]
    path.append(current)
    path.reverse()
    return path

def A_Star(g, src, dest, h):
    openQueue = []
    heapq.heappush(openQueue, (1, src)) 

    predecessor = {}

    minCost = {node: float('inf') for node in g.adj}
    minCost[src] = 0

    predCost = {node: float('inf') for node in g.adj}
    predCost[src] = h[src]

    while openQueue:
        _, current = heapq.heappop(openQueue)
        if current == dest:
            return predecessor, reconstruct_path(predecessor, current)
        
        for neighbour in g.adj.get(current, []):
            cost = minCost[current] + g.weights[(current, neighbour)]
            if cost < minCost.get(neighbour, float('inf')):
                predecessor[neighbour] = current
                minCost[neighbour] = cost
                predCost[neighbour] = cost + h[neighbour]
                heapq.heappush(openQueue, (predCost[neighbour], neighbour))   

    return predecessor, [] 

#Testing

g = Graph()
g.add_edge(0, 1, 5)
g.add_edge(0, 2, 4)
g.add_edge(2, 3, 4)
g.add_edge(3, 4, 4)
g.add_edge(2, 5, 1)
g.add_edge(5, 3, 1)

h = {0: 5.0, 1: 3.9, 2: 3.0, 3: 2.1, 4: 0.0, 5: 2.5}

result = A_Star(g, 0, 4, h)

print(result)

#Part 4.2

#What issues with Dijkstra’s algorithm is A* trying to address?

#Djikstra's algorithm is uninformed and therefore explores all paths equally without any prioritization, which makes it less efficient in many cases. A* algorithm is informed and uses a heuristic function to prioritize its search, improving efficiency. The heuristic function estimates the cost from any node to the destination, allowing the algorithm to search paths with lower estimated costs first.

#How would you empirically test Dijkstra’s vs A*?

#You could set up an experiment with a 100x100 grid and a heuristic function that uses Euclidean distance. To guarantee a fair experiment, you could use the same grid and the same source and destination nodes for both A* and Djikstra’s algorithm. You could then run both algorithms and measure correctness, execution time, number of explore nodes and memory usage. This experiment would be run 1000 times with varying source and destination nodes, but still ensuring the experiments are identical for both algorithms by only modifying the configuration after having tested both on the same source and destination nodes. Finally, you would the mean average of the results and compare the two algorithms.

#If you generated an arbitrary heuristic function (like randomly generating weights), how would Dijkstra’s algorithm compare to A*?

#In this case, Djikstra’s algorithm would perform better than A* on average as if the heuristic function overestimates the true cost, the path A* returns may no longer be optimal and search efficiency would decrease. This means Djikstra’s algorithm would be the only algorithm that guaranteed correctness, thus making it the better performing out of the two.

#What applications would you use A* instead of Dijkstra’s?

#You would use A* over Djikstra’s when the distance between any node and the goal can be accurately estimated by the heuristic function. It also valuable in application where a low execution time is important as that is the primary goal of A*. For example, you would use A* in GPS applications as speed is important and a heuristic function for distance is easy to calculate.