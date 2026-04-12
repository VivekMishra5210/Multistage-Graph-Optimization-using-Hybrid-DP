import random
import numpy as np
import networkx as nx
import time


def build_multistage_graph(num_stages=5, nodes_per_stage=4, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    G = nx.DiGraph()
    stages = []
    node_id = 0
    for s in range(num_stages):
        if s == 0 or s == num_stages - 1:
            count = 1
        else:
            count = nodes_per_stage
        stage_nodes = list(range(node_id, node_id + count))
        for n in stage_nodes:
            G.add_node(n, stage=s)
        stages.append(stage_nodes)
        node_id += count
    for i in range(num_stages - 1):
        for u in stages[i]:
            for v in stages[i + 1]:
                w = random.randint(1, 20)
                G.add_edge(u, v, weight=w)
    source = stages[0][0]
    sink = stages[-1][0]
    return G, stages, source, sink


def backward_dp(G, stages, sink):
    cost = {n: float('inf') for n in G.nodes()}
    policy = {n: None for n in G.nodes()}
    cost[sink] = 0
    nodes_visited = 0
    for stage_idx in range(len(stages) - 2, -1, -1):
        for v in stages[stage_idx]:
            nodes_visited += 1
            best_cost = float('inf')
            best_next = None
            for w in G.successors(v):
                edge_w = G[v][w]['weight']
                total = edge_w + cost[w]
                if total < best_cost:
                    best_cost = total
                    best_next = w
            cost[v] = best_cost
            policy[v] = best_next
    return cost, policy, nodes_visited


def extract_optimal_path(policy, source, sink):
    path = [source]
    node = source
    while node != sink:
        node = policy[node]
        if node is None:
            break
        path.append(node)
    return path


def compute_stages(G):
    stages = {}
    for node, data in G.nodes(data=True):
        stage = data.get("stage", 0)
        if stage not in stages:
            stages[stage] = []
        stages[stage].append(node)
    ordered_stages = [stages[k] for k in sorted(stages.keys())]
    return ordered_stages


def solve(G, source, sink):
    start_time = time.perf_counter()
    stages = compute_stages(G)
    cost, policy, nodes_visited = backward_dp(G, stages, sink)
    path = extract_optimal_path(policy, source, sink)
    end_time = time.perf_counter()
    total_nodes = G.number_of_nodes()
    return {
        "algorithm": "DP Classic",
        "path": path,
        "path_cost": cost[source],
        "nodes_visited": nodes_visited,
        "total_nodes": total_nodes,
        "time": end_time - start_time
    }


if __name__ == "__main__":
    G, stages, source, sink = build_multistage_graph(
        num_stages=5,
        nodes_per_stage=3,
        seed=42
    )
    result = solve(G, source, sink)
    print("\nDP Classic Result\n")
    print("Path:", result["path"])
    print("Cost:", result["path_cost"])
    print("Nodes visited:", result["nodes_visited"], "/", result["total_nodes"])
    print("Time:", result["time"])