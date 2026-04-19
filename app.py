import streamlit as st
import networkx as nx
import math
import subprocess
import os
import matplotlib.pyplot as plt

from DP_Classic.multistage_dp import solve as dp_solve
from ML_A_star_Guided_Learning.ml_astar import solve as ml_solve

st.title("Multistage Graph Optimization (Hybrid DP + ML A*)")

# ---------- CITY LIST ----------
cities = [
    "Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Solapur",
    "Kolhapur", "Amravati", "Jalgaon", "Latur", "Akola", "Dhule",
    "Ahmednagar", "Chandrapur", "Parbhani", "Nanded", "Beed",
    "Osmanabad", "Satara", "Sangli", "Wardha", "Buldhana",
    "Yavatmal", "Gondia", "Washim", "Hingoli", "Ratnagiri",
    "Sindhudurg", "Palghar", "Thane", "Raigad", "Panvel",
    "Ulhasnagar", "Kalyan", "Dombivli", "Bhiwandi", "Malegaon",
    "Baramati", "Karad", "Miraj", "Ichalkaranji", "Pandharpur",
    "Shirdi", "Shegaon", "Ballarpur", "Warora", "Wani",
    "Udgir", "Tuljapur", "Pusad", "Achalpur", "Malkapur"
]

# ---------- GRAPH BUILD ----------
def build_city_graph(cities):
    import osmnx as ox

    G = nx.DiGraph()
    coords = {}

    # Get coordinates
    for city in cities:
        loc = ox.geocode(city + ", Maharashtra, India")
        coords[city] = (loc[0], loc[1])
        G.add_node(city, pos=(loc[1], loc[0]))  # (lon, lat)

    # Connect nearby cities
    for c1 in cities:
        for c2 in cities:
            if c1 == c2:
                continue

            lat1, lon1 = coords[c1]
            lat2, lon2 = coords[c2]

            dist = math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111

            if dist < 250:  # threshold
                G.add_edge(c1, c2, weight=dist)

    return G


# ---------- STAGE ASSIGN ----------
def assign_stages(G, source):
    stage_map = nx.single_source_shortest_path_length(G, source)

    for node in G.nodes():
        G.nodes[node]["stage"] = stage_map.get(node, 0)

    return G


# ---------- C++ SOLVER ----------
def run_cpp_solver(G, source, sink):

    stages = nx.get_node_attributes(G, "stage")
    unique = sorted(set(stages.values()))
    mapping = {s: i for i, s in enumerate(unique)}

    for node in G.nodes():
        G.nodes[node]["stage"] = mapping[stages[node]]

    num_layers = len(unique)

    nodes_list = list(G.nodes())
    node_index = {node: i for i, node in enumerate(nodes_list)}

    n = len(nodes_list)
    m = G.number_of_edges()

    lines = []
    lines.append(f"{n} {m} {num_layers} {node_index[source]} {node_index[sink]}")

    # stages
    for node in nodes_list:
        lines.append(str(G.nodes[node]["stage"]))

    # edges
    for u, v, data in G.edges(data=True):
        w = data.get("weight", 1)
        lines.append(f"{node_index[u]} {node_index[v]} {int(w)}")

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
        st.error("C++ solver failed")
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


# ---------- VISUALIZATION ----------
def visualize_graph(G, path=None, halts=None):

    pos = nx.get_node_attributes(G, 'pos')

    plt.figure(figsize=(16, 10))  # 👈 BIGGER

    # Draw base graph (light & thin)
    nx.draw_networkx_edges(
        G,
        pos,
        edge_color="lightgray",
        width=0.5,
        alpha=0.5
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=150,
        node_color="skyblue"
    )

    # Draw labels (BIGGER + clearer)
    nx.draw_networkx_labels(
        G,
        pos,
        font_size=8,   # 👈 increase (try 9–10 if needed)
        font_weight="bold"
    )

    # Highlight path
    if path:
        edges = list(zip(path, path[1:]))

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edges,
            edge_color="blue",
            width=3
        )

        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=path,
            node_color="green",
            node_size=250
        )

    # Highlight halts
    if halts:
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=halts,
            node_color="red",
            node_size=350
        )

    plt.title("City Route Visualization", fontsize=16)
    plt.axis("off")

    st.pyplot(plt)


# ---------- UI ----------
source_city = st.selectbox("Source City", cities)
dest_city = st.selectbox("Destination City", cities)

halt_km = st.slider("Halt every (km)", 50, 300, 100)

run_btn = st.button("Run Algorithms")

# ---------- MAIN ----------
if run_btn:

    if source_city == dest_city:
        st.error("Choose different cities")
        st.stop()

    with st.spinner("Building graph..."):
        G = build_city_graph(cities)
        G = assign_stages(G, source_city)

    st.write("Nodes:", G.number_of_nodes())
    st.write("Edges:", G.number_of_edges())

    results = []

    # DP
    dp_result = dp_solve(G, source_city, dest_city)
    results.append(dp_result)

    # ML A*
    ml_result = ml_solve(G, source_city, dest_city)
    results.append(ml_result)

    # C++
    cpp_result = run_cpp_solver(G, source_city, dest_city)
    if cpp_result:
        results.append(cpp_result)

    # ---------- RESULTS ----------
    st.subheader("Algorithm Comparison")

    table = []
    for r in results:
        table.append({
            "Algorithm": r["algorithm"],
            "Time (s)": f"{r['time']:.8f}",
            "Nodes Visited": f"{r['nodes_visited']}/{r['total_nodes']}"
        })

    st.table(table)

    # ---------- HALTS ----------
    st.subheader("Halts")

    path = ml_result["path"]

    halts = []
    dist = 0

    for u, v in zip(path, path[1:]):
        dist += G[u][v]["weight"]

        if dist >= halt_km:
            halts.append(v)
            dist = 0

    st.write("Halt Cities:", halts)

    # ---------- VISUAL ----------
    st.subheader("Visualization")
    visualize_graph(G, path, halts)