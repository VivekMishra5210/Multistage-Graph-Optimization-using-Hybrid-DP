import networkx as nx
import matplotlib.pyplot as plt
import random


def visualize_graph(G, path=None, visited=None, title="Graph"):
    pos = {}
    stages = nx.get_node_attributes(G, "stage")
    stage_groups = {}
    for node, s in stages.items():
        stage_groups.setdefault(s, []).append(node)

    for s, nodes in stage_groups.items():
        for i, node in enumerate(nodes):
            pos[node] = (s * 2, -i * 0.6)

    plt.figure(figsize=(12,6))

    edges = list(G.edges())
    sample_size = int(len(edges) * 0.15) 
    edges_sample = random.sample(edges, sample_size)

    nx.draw_networkx_edges(G, pos, edgelist=edges_sample, alpha=0.3)

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=40,
        node_color="lightgray"
    )

    if visited:
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=visited,
            node_color="orange",
            node_size=100,
            label="Visited"
        )

    if path:
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=path,
            node_color="red",
            node_size=150,
            label="Optimal Path"
        )

        edges = list(zip(path, path[1:]))

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edges,
            edge_color="red",
            width=2
        )

    plt.title(title)
    plt.legend()
    plt.axis("off")
    plt.show()