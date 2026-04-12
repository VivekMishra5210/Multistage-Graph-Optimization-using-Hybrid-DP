import networkx as nx
import random
import subprocess
import os
from visualizer import visualize_graph
from DP_Classic.multistage_dp import solve as dp_solve
from ML_A_star_Guided_Learning.ml_astar import solve as ml_solve
from DP_Classic.multistage_dp import build_multistage_graph


def fetch_graph():
    print("\nGenerating synthetic multistage graph...\n")
    num_stages = 15
    nodes_per_stage = 40
    G, stages, source, sink = build_multistage_graph(
        num_stages=num_stages,
        nodes_per_stage=nodes_per_stage,
        seed=random.randint(0, 1000)
    )
    for stage_idx, nodes in enumerate(stages):
        for node in nodes:
            G.nodes[node]["stage"] = stage_idx
    print("Synthetic Multistage Graph")
    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())
    print("Stages:", num_stages)
    print("Nodes per stage:", nodes_per_stage)
    print("Source:", source)
    print("Sink:", sink)
    return G, source, sink


def normalize_stages(G):
    stages = nx.get_node_attributes(G, "stage")
    unique = sorted(set(stages.values()))
    mapping = {s: i for i, s in enumerate(unique)}
    for node in G.nodes():
        G.nodes[node]["stage"] = mapping[stages[node]]
    return len(unique)


def run_cpp_solver(G, source, sink):
    num_layers = normalize_stages(G)
    stages = nx.get_node_attributes(G, "stage")
    n = G.number_of_nodes()
    m = G.number_of_edges()
    lines = []
    lines.append(f"{n} {m} {num_layers} {source} {sink}")
    for i in range(n):
        lines.append(str(stages[i]))
    for u, v, data in G.edges(data=True):
        w = data.get("weight", 1)
        lines.append(f"{u} {v} {w}")
    input_data = "\n".join(lines)
    file_path = "graph_input.txt"
    with open(file_path, "w") as f:
        f.write(input_data)
    exe_path = os.path.join(os.getcwd(), "dp_greedy.exe")
    process = subprocess.run(
        [exe_path, file_path],
        capture_output=True,
        text=True
    )
    if process.returncode != 0:
        print("C++ solver crashed:", process.stderr)
        return None
    output = process.stdout.strip().split()
    time_ms = float(output[0])
    nodes_processed = int(output[1])
    return {
        "algorithm": "DP + Greedy (C++)",
        "time": time_ms / 1000,
        "nodes_visited": nodes_processed,
        "total_nodes": n
    }


def print_results(results):
    print("\nAlgorithm Comparison")
    print("-" * 60)
    print(
        f"{'Algorithm':<25}"
        f"{'Time (s)':<15}"
        f"{'Nodes Visited':<20}"
    )
    print("-" * 60)
    for r in results:
        print(
            f"{r['algorithm']:<25}"
            f"{r['time']:<15.6f}"
            f"{r['nodes_visited']}/{r['total_nodes']:<20}"
        )
    print("-" * 60)
    best = min(results, key=lambda x: x["time"])
    print(f"\nBest Algorithm: {best['algorithm']}")
    print(f"Fastest Time: {best['time']:.6f} seconds")
    print("\nExploration Efficiency:")
    for r in results:
        pct = (r["nodes_visited"] / r["total_nodes"]) * 100
        print(f"{r['algorithm']}: {pct:.1f}% of graph explored")


def main():
    print("Working dir:", os.getcwd())
    G, source, sink = fetch_graph()
    results = []
    dp_result = dp_solve(G, source, sink)
    results.append(dp_result)
    ml_result = ml_solve(G, source, sink)
    results.append(ml_result)
    cpp_result = run_cpp_solver(G, source, sink)
    if cpp_result:
        results.append(cpp_result)
    print_results(results)
    print("\nVisualization legend:")
    print("Grey  → all nodes")
    print("Orange → nodes explored by ML A*")
    print("Red   → optimal path")
    visualize_graph(
        G,
        path=ml_result["path"],
        visited=ml_result["visited_nodes"],
        title="ML Guided A* Exploration"
    )


if __name__ == "__main__":
    main()