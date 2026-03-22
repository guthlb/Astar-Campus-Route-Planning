import matplotlib
matplotlib.use('TkAgg')

import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import pandas as pd

# ---------------- LOAD GRAPH ----------------
G = nx.read_graphml("mit_campus.graphml")

print("Graph loaded")
print("Nodes:", len(G.nodes))
print("Edges:", len(G.edges))

# ---------------- PREPROCESS ----------------
for n in G.nodes:
    G.nodes[n]['x'] = float(G.nodes[n]['x'])
    G.nodes[n]['y'] = float(G.nodes[n]['y'])

for u, v, d in G.edges(data=True):
    try:
        d['length'] = float(d.get('length', 1.0))
    except:
        d['length'] = 1.0

largest_cc = max(nx.connected_components(G.to_undirected()), key=len)
G = G.subgraph(largest_cc).copy()

print("Graph cleaned")

# ---------------- BFS ----------------
def run_bfs(G, start, goal):
    try:
        return nx.shortest_path(G, start, goal)
    except:
        return []

# ---------------- DFS ----------------
def run_dfs(G, start, goal):
    visited = set()
    stack = [(start, [start])]

    while stack:
        node, path = stack.pop()

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)

            for neighbor in G.neighbors(node):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    return []

# ---------------- A* HEURISTIC ----------------
def heuristic(n1, n2):
    x1, y1 = G.nodes[n1]['x'], G.nodes[n1]['y']
    x2, y2 = G.nodes[n2]['x'], G.nodes[n2]['y']
    return abs(x1 - x2) + abs(y1 - y2)

# ---------------- PATH COST ----------------
def path_cost(path):
    if len(path) < 2:
        return 0
    cost = 0
    for i in range(len(path) - 1):
        edges = G[path[i]][path[i+1]]
        cost += min(e.get('length', 1.0) for e in edges.values())
    return cost

# ---------------- EXPERIMENTS ----------------
NUM_RUNS = 50
nodes = list(G.nodes)

results = []

astar_success = 0
bfs_success = 0
dfs_success = 0

print("\nRunning experiments...\n")

for i in range(NUM_RUNS):
    start = random.choice(nodes)
    goal = random.choice(nodes)

    while start == goal:
        goal = random.choice(nodes)

    # A*
    t0 = time.perf_counter()
    try:
        astar_path = nx.astar_path(G, start, goal, heuristic=heuristic, weight='length')
        astar_success += 1
    except:
        astar_path = []
    t_astar = (time.perf_counter() - t0) * 1000

    # BFS
    t0 = time.perf_counter()
    bfs_path = run_bfs(G, start, goal)
    if bfs_path:
        bfs_success += 1
    t_bfs = (time.perf_counter() - t0) * 1000

    # DFS
    t0 = time.perf_counter()
    dfs_path = run_dfs(G, start, goal)
    if dfs_path:
        dfs_success += 1
    t_dfs = (time.perf_counter() - t0) * 1000

    results.append({
        "astar_time": t_astar,
        "astar_cost": path_cost(astar_path),
        "astar_length": len(astar_path),

        "bfs_time": t_bfs,
        "bfs_cost": path_cost(bfs_path),
        "bfs_length": len(bfs_path),

        "dfs_time": t_dfs,
        "dfs_cost": path_cost(dfs_path),
        "dfs_length": len(dfs_path),
    })

print("Experiments finished")

# ---------------- RESULTS TABLE ----------------
df = pd.DataFrame(results)
print("\nResults Table:")
print(df)

# ---------------- AVERAGE RESULTS ----------------
avg_results = pd.DataFrame({
    "Algorithm": ["A*", "BFS", "DFS"],
    "Avg Time (ms)": [
        df["astar_time"].mean(),
        df["bfs_time"].mean(),
        df["dfs_time"].mean()
    ],
    "Avg Path Cost": [
        df["astar_cost"].mean(),
        df["bfs_cost"].mean(),
        df["dfs_cost"].mean()
    ],
    "Avg Path Length": [
        df["astar_length"].mean(),
        df["bfs_length"].mean(),
        df["dfs_length"].mean()
    ],
    "Success Rate (%)": [
        astar_success / NUM_RUNS * 100,
        bfs_success / NUM_RUNS * 100,
        dfs_success / NUM_RUNS * 100
    ]
})

print("\nAverage Results:")
print(avg_results)

# ---------------- GRAPHS ----------------
plt.figure()
plt.bar(avg_results["Algorithm"], avg_results["Avg Time (ms)"])
plt.title("Average Execution Time Comparison")
plt.ylabel("Time (ms)")
plt.xlabel("Algorithm")
plt.show()

plt.figure()
plt.bar(avg_results["Algorithm"], avg_results["Avg Path Cost"])
plt.title("Average Path Cost Comparison")
plt.ylabel("Cost")
plt.xlabel("Algorithm")
plt.show()

plt.figure()
plt.bar(avg_results["Algorithm"], avg_results["Avg Path Length"])
plt.title("Average Path Length Comparison")
plt.ylabel("Length")
plt.xlabel("Algorithm")
plt.show()

plt.figure()
df[["astar_time","bfs_time","dfs_time"]].boxplot()
plt.title("Execution Time Distribution")
plt.ylabel("Time (ms)")
plt.show()

