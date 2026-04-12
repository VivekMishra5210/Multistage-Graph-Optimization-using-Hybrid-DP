#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <climits>
#include <chrono>

using namespace std;

struct Edge {
    int to;
    int weight;
};

struct Result {
    int cost;
    int nodesProcessed;
    int nodesPruned;
    double timeMs;
};

Result solve(
    int numNodes,
    int numLayers,
    vector<vector<Edge>>& adj,
    vector<vector<int>>& stageNodes,
    int src,
    int dst,
    double pruneFactor = 1.5
){
    auto t0 = chrono::high_resolution_clock::now();

    vector<int> cost(numNodes, INT_MAX / 2);
    vector<int> parent(numNodes, -1);

    cost[src] = 0;

    int processed = 0;
    int pruned = 0;

    for (int L = 0; L < numLayers - 1; L++) {

        for (int u : stageNodes[L]) {

            if (cost[u] == INT_MAX/2) continue;

            processed++;

            vector<Edge> edges = adj[u];

            sort(edges.begin(), edges.end(),
                [](const Edge& a, const Edge& b){
                    return a.weight < b.weight;
                });

            for (const Edge& e : edges) {

                int newCost = cost[u] + e.weight;

                if (newCost < cost[e.to]) {
                    cost[e.to] = newCost;
                    parent[e.to] = u;
                }
            }
        }

        const vector<int>& nextLayer = stageNodes[L+1];

        vector<double> reachable;

        for (int v : nextLayer)
            if (cost[v] < INT_MAX/2)
                reachable.push_back(cost[v]);

        if (reachable.size() >= 2) {

            double avg = accumulate(
                reachable.begin(),
                reachable.end(),
                0.0
            ) / reachable.size();

            double threshold = avg * pruneFactor;

            for (int v : nextLayer) {

                if (v == dst) continue;

                if (cost[v] < INT_MAX/2 && cost[v] > threshold) {

                    cost[v] = INT_MAX/2;
                    parent[v] = -1;
                    pruned++;
                }
            }
        }
    }

    auto t1 = chrono::high_resolution_clock::now();

    double ms =
        chrono::duration<double,milli>(t1 - t0).count();

    return {
        cost[dst] >= INT_MAX/2 ? -1 : cost[dst],
        processed,
        pruned,
        ms
    };
}

int main(){

    // Input format from Python:
    // n m layers src dst
    // stage per node
    // edges

    int n, m, layers, src, dst;
    cin >> n >> m >> layers >> src >> dst;

    vector<int> stage(n);

    for(int i=0;i<n;i++)
        cin >> stage[i];

    vector<vector<int>> stageNodes(layers);

    for(int i=0;i<n;i++)
        stageNodes[stage[i]].push_back(i);

    vector<vector<Edge>> adj(n);

    for(int i=0;i<m;i++){

        int u,v,w;
        cin >> u >> v >> w;

        adj[u].push_back({v,w});
    }

    Result r = solve(n, layers, adj, stageNodes, src, dst);

    cout << r.timeMs << " "
         << r.nodesProcessed << " "
         << r.nodesPruned << endl;
}