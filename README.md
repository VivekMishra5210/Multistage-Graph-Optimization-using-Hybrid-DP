# Multistage Graph Optimization using Hybrid DP 🚀

A complete implementation and comparison of **Dynamic Programming, ML-Guided A*, and Greedy Pruning (C++)** for solving multistage graph optimization problems.

This project demonstrates both:

* ⚙️ **Algorithmic strength (core DAA concepts)**
* 🌍 **Real-world usability (city-based routing with UI)**

---

## 📌 Features

* ✅ Classic **Multistage Graph DP**
* ✅ **ML-Guided A*** (Random Forest heuristic)
* ✅ **DP + Greedy Pruning (C++ optimized)**
* ✅ Performance comparison (time + nodes visited)
* ✅ Synthetic graph testing (~500 nodes)
* ✅ Interactive **Streamlit UI with city selection**
* ✅ Halt-based routing (user-defined intervals)
* ✅ Graph visualization with path + halts

---

## 📁 Project Structure

```
DAA Project/
│
├── main.py                         # Synthetic graph testing (~500 nodes)
├── app.py                          # Streamlit UI (city-based routing)
├── requirements.txt
│
├── DP_Classic/
│   └── multistage_dp.py           # Classic DP solution
│
├── ML_A_star_Guided_Learning/
│   ├── dataset_builder.py
│   ├── train_model.py
│   ├── ml_astar.py                # ML-guided A*
│   └── rf_model.pkl               # Trained model
│
├── dp_greedy.cpp                  # C++ optimized DP + pruning
├── dp_greedy.exe                  # Compiled executable
│
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

---

### 🔹 Option 1: Synthetic Graph (Algorithm Testing)

Runs all algorithms on a generated multistage graph (~500 nodes)

```bash
python main.py
```

✔ Outputs:

* Execution time comparison
* Nodes visited
* Best performing algorithm

---

### 🔹 Option 2: GUI (Real-world City Routing)

```bash
streamlit run app.py
```

✔ Features:

* Select **source & destination cities**
* Define **halt distance (km)**
* Run all algorithms
* View:

  * Optimal path
  * Halt locations
  * Performance comparison
  * Graph visualization

---

## 🧠 Algorithms Used

### 1. Dynamic Programming (DP)

* Solves multistage graph optimally
* Works in **backward stage order**
* Time complexity: **O(E)**

---

### 2. ML-Guided A*

* Uses **Random Forest** to predict remaining cost
* Heuristic replaces traditional A* heuristic
* Reduces unnecessary exploration

---

### 3. DP + Greedy Pruning (C++)

* Optimized version of DP
* Prunes high-cost nodes dynamically
* Extremely fast due to:

  * C++ execution
  * Reduced search space

---

## 🤖 Machine Learning Component

Pipeline:

```
dataset_builder.py → dataset.csv → train_model.py → rf_model.pkl
```

* Features:

  * stage
  * out_degree
  * min_edge_weight
  * avg_edge_weight
* Target:

  * Optimal remaining cost (from DP)

Used as heuristic in A*.

---

## ⚡ C++ Integration (IMPORTANT)

The file `dp_greedy.cpp` is compiled into an executable:

```bash
g++ -O2 -std=c++17 dp_greedy.cpp -o dp_greedy.exe
```

### How it works:

1. Python creates a graph input file (`graph_input.txt`)
2. Python calls:

   ```
   dp_greedy.exe graph_input.txt
   ```
3. C++ program:

   * Reads graph
   * Runs optimized DP + pruning
   * Outputs:

     ```
     time nodes_processed nodes_pruned
     ```
4. Python captures output and adds it to comparison

👉 This allows combining:

* Python flexibility
* C++ performance

---

## 📊 Output Example

| Algorithm         | Time (s) | Nodes Visited |
| ----------------- | -------- | ------------- |
| DP Classic        | 0.0109   | 521/522       |
| ML Guided A*      | 6.61     | 267/522       |
| DP + Greedy (C++) | 0.0006   | 500/522       |

---

## 🗺️ Visualization

* 🔵 Blue → Optimal path
* 🔴 Red → Halt points
* 🟢 Green → Path nodes
* ⚪ Grey → Full graph

---

## 🎯 Key Insight

This project shows:

> **Combining classical algorithms + machine learning + optimization techniques leads to powerful hybrid solutions.**

---

## ⚠️ Notes

* Requires **Python 3.10+**
* Requires **C++ compiler (g++)** for `.exe`
* ML model is pre-trained (`rf_model.pkl`)

---

## 🚀 Future Improvements

* Interactive zoomable map
* Live path animation
* Better heuristic models
* Real road network integration

---

## ⭐ Final Thought

This project bridges:

```
Theory (DP, A*)
+
Optimization (Greedy Pruning)
+
Machine Learning
+
Real-world UI
```

👉 A complete **Hybrid Algorithm System**
