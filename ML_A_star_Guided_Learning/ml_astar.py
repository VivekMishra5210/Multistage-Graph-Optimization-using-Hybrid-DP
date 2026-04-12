import heapq
import joblib
import time
import warnings
import os

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "rf_model.pkl")

# load model ONCE
MODEL = joblib.load(MODEL_PATH)


def extract_node_features(G, node):
    stage = G.nodes[node]['stage']
    neighbors = list(G.successors(node))

    out_degree = len(neighbors)

    if out_degree == 0:
        min_w = 0
        avg_w = 0
    else:
        weights = [G[node][v]['weight'] for v in neighbors]
        min_w = min(weights)
        avg_w = sum(weights) / len(weights)

    return [stage, out_degree, min_w, avg_w]


def precompute_heuristics(G):
    """Compute ML heuristic for all nodes in one batch"""

    nodes = list(G.nodes())
    feature_list = []

    for node in nodes:
        feature_list.append(extract_node_features(G, node))

    # Single vectorized prediction
    preds = MODEL.predict(feature_list)

    heuristic = {}
    for node, val in zip(nodes, preds):
        heuristic[node] = val

    return heuristic


def ml_astar_search(G, source, sink, heuristic):

    pq = []
    heapq.heappush(pq, (0, source))

    g_cost = {source: 0}
    parent = {}
    visited = set()

    nodes_expanded = 0

    while pq:

        f, node = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)
        nodes_expanded += 1

        if node == sink:
            break

        for neighbor in G.successors(node):

            weight = G[node][neighbor]['weight']

            new_g = g_cost[node] + weight

            if neighbor not in g_cost or new_g < g_cost[neighbor]:

                g_cost[neighbor] = new_g
                parent[neighbor] = node

                h = heuristic[neighbor]   # fast lookup

                heapq.heappush(pq, (new_g + h, neighbor))

    path = []

    node = sink
    while node != source:
        path.append(node)
        node = parent[node]

    path.append(source)
    path.reverse()

    return path, g_cost[sink], nodes_expanded, visited


def solve(G, source, sink):

    start = time.perf_counter()

    # compute heuristics once
    heuristic = precompute_heuristics(G)

    path, cost, nodes_expanded, visited = ml_astar_search(
        G, source, sink, heuristic
    )

    end = time.perf_counter()

    return {
        "algorithm": "ML Guided A*",
        "path": path,
        "path_cost": cost,
        "nodes_visited": nodes_expanded,
        "total_nodes": G.number_of_nodes(),
        "time": end - start,
        "visited_nodes": visited
    }