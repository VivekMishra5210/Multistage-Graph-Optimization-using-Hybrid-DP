# Multistage Graph Optimization using Hybrid Dynamic Programming

This project explores multiple approaches to solve the **Multistage Graph Shortest Path Problem** and compares their efficiency using classical algorithms, machine learning, and heuristic pruning.

The goal is to demonstrate how **algorithmic optimization and ML-guided search can improve performance when solving large multistage graphs.**

---

# Problem Overview

A **multistage graph** is a directed graph where nodes are divided into ordered stages.

Edges only exist from stage `i` to stage `i+1`.

The task is to compute the **minimum cost path from a source node to a sink node**.

Example structure:

```
Stage 0     Stage 1     Stage 2     Stage 3
   ●            ●            ●            ●
    \          / \          /
     ●        ●   ●        ●
      \      /     \      /
       ●            ●
```

Multistage graphs commonly appear in:

- Dynamic programming problems
- Scheduling problems
- Routing and optimization tasks

---

# Algorithms Implemented

This project compares **three approaches**:

## 1. Classic Dynamic Programming (Python)

Baseline solution using **backward dynamic programming**.

Features:

- Guarantees optimal solution
- Explores almost the entire graph
- Simple and deterministic approach

---

## 2. ML-Guided A* Search (Python + Random Forest)

A **Random Forest model** predicts the remaining cost from any node to the sink.

This prediction is used as a **heuristic function in the A* search algorithm**.

Benefits:

- Guides search toward promising nodes
- Reduces exploration of unnecessary nodes
- Demonstrates integration of **Machine Learning with algorithm design**

---

## 3. Greedy Pruned Dynamic Programming (C++ Optimized)

This optimized solver applies **cost-based pruning**:

Nodes with cost significantly higher than the average cost in a stage are pruned.

Advantages:

- Extremely fast
- Implemented in **C++ for high performance**
- Avoids exploring weak candidate nodes

---

# Project Structure

```
Multistage-Graph-Optimization-using-Hybrid-DP

│
├── main.py
├── visualizer.py
│
├── DP_Classic
│   └── multistage_dp.py
│
├── ML_A_star_Guided_Learning
│   ├── ml_astar.py
│   ├── dataset_builder.py
│   ├── train_model.py
│   └── rf_model.pkl
│
├── dp_greedy.cpp
├── dp_greedy.exe
│
└── README.md
```

---

# Visualization

The project includes a visualization module that displays:

- The generated multistage graph
- Nodes explored by ML-guided A*
- Optimal path from source to sink

Color Legend:

| Color | Meaning |
|------|--------|
| Grey | All nodes in the graph |
| Orange | Nodes explored by ML A* |
| Red | Optimal shortest path |

This visualization helps illustrate how **different algorithms explore the graph.**

---

# Example Output

```
Synthetic Multistage Graph
Nodes: 522
Edges: 19280
Stages: 15

Algorithm Comparison
------------------------------------------------------------
Algorithm                Time (s)       Nodes Visited
------------------------------------------------------------
DP Classic               0.011          521/522
ML Guided A*             6.61           267/522
DP + Greedy (C++)        0.0006         500/522
------------------------------------------------------------

Best Algorithm: DP + Greedy (C++)
```

---

# Exploration Efficiency

```
DP Classic: ~100% of graph explored
ML Guided A*: ~50% of graph explored
DP + Greedy (C++): ~96% of graph explored
```

This demonstrates how **ML-guided search can significantly reduce exploration of the graph.**

---

# Technologies Used

- Python
- C++
- NetworkX
- Scikit-learn
- Matplotlib
- Heap-based A* search
- Hybrid algorithm optimization

---

# How to Run

Clone the repository:

```bash
git clone https://github.com/VivekMishra5210/Multistage-Graph-Optimization-using-Hybrid-DP.git
```

Move into the project folder:

```bash
cd Multistage-Graph-Optimization-using-Hybrid-DP
```

Run the project:

```bash
python main.py
```

This will:

1. Generate a synthetic multistage graph
2. Run all algorithms
3. Compare performance
4. Display a graph visualization

---

# Key Learning Outcomes

This project demonstrates:

- Dynamic Programming on graphs
- Heuristic search using A*
- ML-based cost estimation
- Hybrid algorithm optimization
- Cross-language integration (Python + C++)
- Performance benchmarking
- Graph visualization techniques

---

# Author

**Vivek Mishra**  
B.Tech Computer Science  
IIIT Nagpur