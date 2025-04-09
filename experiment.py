# experiment.py
import csv
import math
import time
from graph import UndirectedWeightedGraph
from shortest_paths import dijkstra
from a_star_adapter import AStarAdapter, manhattan_heuristic
import Draw_plot

def load_stations(file):
    stations = {}
    with open("/Users/macbookair/Documents/2XC3/COMPSCI2XC3_FinalProject_Group-55/london_stations.csv", newline='') as f:
        reader = csv.DictReader(f)
        sorted_rows = sorted(reader, key=lambda x: int(x['id']))
        for row in sorted_rows:
            stations[row['id']] = {
                'name': row['name'],
                'lat': float(row['latitude']),
                'lon': float(row['longitude']),
            }
    return stations

def load_connections(file):
    connections = []
    with open("/Users/macbookair/Documents/2XC3/COMPSCI2XC3_FinalProject_Group-55/london_connections.csv", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            connections.append({
                'station1': row['station1'],
                'station2': row['station2'],
                'line': row['line']
            })
    return connections

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def build_graph(stations, connections):
    # Create an undirected graph instance.
    graph = UndirectedWeightedGraph(len(stations))
    for sid in stations:
        graph.add_node(sid)
    for conn in connections:
        s1, s2, _ = conn['station1'], conn['station2'], conn['line']
        dist = haversine(stations[s1]['lat'], stations[s1]['lon'],
                         stations[s2]['lat'], stations[s2]['lon'])
        graph.add_edge(s1, s2, dist)
    return graph

def count_line_changes(path, graph, stations, connections):
    # A placeholder function – if line changes are tracked, implement here.
    return 0

def compare_algorithms(station_file, connection_file):
    stations = load_stations(station_file)
    connections = load_connections(connection_file)
    graph = build_graph(stations, connections)
    
    station_ids = list(stations.keys())
    results = []
    # Prepare node positions for the heuristic.
    node_positions = {sid: (data['lat'], data['lon']) for sid, data in stations.items()}
    
    # Instantiate the A* adapter.
    a_star_adapter = AStarAdapter(graph)
    
    for i in range(len(station_ids)):
        for j in range(i + 1, len(station_ids)):
            src = station_ids[i]
            dst = station_ids[j]
            # Use Manhattan heuristic as an example.
            heuristic = manhattan_heuristic(dst, node_positions)
            
            start = time.time()
            a_star_path = a_star_adapter.find_shortest_path(src, dst, heuristic)
            time_a = time.time() - start
            
            k = 4  # Relaxation limit
            start = time.time()
            _, paths_d = dijkstra(graph, src, k)
            dijkstra_path = paths_d.get(dst, [])
            time_d = time.time() - start
            
            results.append({
                'src': stations[src]['name'],
                'dst': stations[dst]['name'],
                'a_star_time': time_a,
                'dijkstra_time': time_d,
                'a_star_path': a_star_path,
                'dijkstra_path': dijkstra_path,
                'a_star_lines': count_line_changes(a_star_path, graph, stations, connections),
                'dijkstra_lines': count_line_changes(dijkstra_path, graph, stations, connections)
            })
    
    for r in results:
        print(f"{r['src']} -> {r['dst']}")
        print(f"  A* Time: {r['a_star_time']:.5f}s, Lines: {r['a_star_lines']}")
        print(f"  Dijkstra Time: {r['dijkstra_time']:.5f}s, Lines: {r['dijkstra_lines']}")
        print()
    
    # Plot the runtime comparison.
    Draw_plot.draw_plot({
        "Dijkstra": [res['dijkstra_time'] for res in results],
        "A*": [res['a_star_time'] for res in results]
    }, "Experiment_2.3")
    
    return results

if __name__ == '__main__':
    compare_algorithms('london_stations.csv', 'london_connections.csv')
