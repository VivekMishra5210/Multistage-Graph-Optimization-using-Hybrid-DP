import csv
import random
import numpy as np
import networkx as nx
from DP_Classic.multistage_dp import build_multistage_graph, backward_dp


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


def build_dataset(num_graphs=300, filename="dataset.csv"):
    dataset = []
    for i in range(num_graphs):
        stages = random.randint(5, 10)
        nodes_per_stage = random.randint(3, 8)
        G, stage_list, source, sink = build_multistage_graph(
            num_stages=stages,
            nodes_per_stage=nodes_per_stage,
            seed=random.randint(0, 10000)
        )
        cost, policy, _ = backward_dp(G, stage_list, sink)
        for node in G.nodes():
            features = extract_node_features(G, node)
            target = cost[node]
            dataset.append(features + [target])
        print(f"Graph {i+1}/{num_graphs} processed")
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "stage",
            "out_degree",
            "min_edge_weight",
            "avg_edge_weight",
            "target_cost"
        ])
        writer.writerows(dataset)
    print(f"\nDataset saved to {filename}")


if __name__ == "__main__":
    build_dataset()