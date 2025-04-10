import csv
import math
import time
from A_Star import A_Star, manhattan_heuristic, euclidean_heuristic, diagonal_heuristic
from London_Dijkstra import dijkstra
from Draw_plot import draw_plot

def load_stations(file):
    stations = {}
    with open(file, newline='') as f:
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
    with open(file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            connections.append({
                'station1': row['station1'],
                'station2': row['station2'],
                'line': row['line']
            })
    return connections

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  #earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def build_graph(stations, connections):
    graph = {sid: {} for sid in stations}
    for conn in connections:
        s1, s2, line = conn['station1'], conn['station2'], conn['line']
        dist = haversine(stations[s1]['lat'], stations[s1]['lon'],
                         stations[s2]['lat'], stations[s2]['lon'])
        graph[s1][s2] = {'distance': dist, 'line': line}
        graph[s2][s1] = {'distance': dist, 'line': line}
    return graph

def make_heuristic(stations, goal_id, heuristic_type):
    node_positions = {sid: (data['lat'], data['lon']) for sid, data in stations.items()}
    
    if heuristic_type == 'manhattan':
        heuristic = manhattan_heuristic(goal_id, node_positions)
        return heuristic
    elif heuristic_type == 'euclidean':
        heuristic = euclidean_heuristic(goal_id, node_positions)
        return heuristic
    elif heuristic_type == 'diagonal':
        heuristic = diagonal_heuristic(goal_id, node_positions)
        return heuristic
    else:
        raise ValueError("Unknown heuristic type")

def count_line_changes(path, graph, stations):
    changes = 0
    previous_line = None
    
    valid_path = [node for node in path if node in stations]
    if len(valid_path) < 2:
        return 0
    
    for i in range(1, len(valid_path)):
        current = valid_path[i-1]
        next_node = valid_path[i]
        
        if next_node not in graph.get(current, {}):
            continue
            
        current_line = graph[current][next_node]['line']
        if current_line != previous_line:
            changes += 1
            previous_line = current_line
            
    return changes

def compare_algorithms(station_file, connection_file):
    stations = load_stations(station_file)
    connections = load_connections(connection_file)
    graph = build_graph(stations, connections)
    station_ids = list(stations.keys())

    results = []
    for i in range(len(station_ids)):
        for j in range(i + 1, len(station_ids)):
            src = station_ids[i]
            dst = station_ids[j]
            heuristic = make_heuristic(stations, dst, 'euclidean') #select a heuristic type manually

            start = time.time()
            path_a = A_Star(graph, src, dst, heuristic)
            time_a = time.time() - start

            k = 4 #set k manually, though not necessary
            start = time.time()
            _, paths_d = dijkstra(graph, src, k)
            path_d = paths_d.get(dst, [])
            time_d = time.time() - start

            results.append({
                'src': stations[src]['name'],
                'dst': stations[dst]['name'],
                'a_star_time': time_a,
                'dijkstra_time': time_d,
                'a_star_path': path_a,
                'dijkstra_path': path_d,
                'a_star_lines': count_line_changes(path_a, graph, stations),
                'dijkstra_lines': count_line_changes(path_d, graph, stations)
            })

    a_star_times = [r['a_star_time'] for r in results]
    dijkstra_times = [r['dijkstra_time'] for r in results]

    draw_plot({
        "A*": a_star_times,
        "Dijkstra": dijkstra_times
    }, "London Subway Station Pairs")

    for r in results:
        print(f"{r['src']} -> {r['dst']}")
        print(f"  A* Time: {r['a_star_time']:.5f}s, Lines: {r['a_star_lines']}")
        print(f"  Dijkstra Time: {r['dijkstra_time']:.5f}s, Lines: {r['dijkstra_lines']}")
        print()

    return results

compare_algorithms('london_stations.csv', 'london_connections.csv')
