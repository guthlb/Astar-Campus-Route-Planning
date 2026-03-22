import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import pandas as pd
import os
import sys

# Allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from person2.bfs_dfs import run_bfs, run_dfs
from person1.astar import (
    load_graph,
    preprocess_graph,
    get_connected_graph,
    compute_astar_path,
    compute_path_length
)

# ---------------- LOAD + PREPROCESS GRAPH ----------------
G = load_graph()
G = preprocess_graph(G)
G = get_connected_graph(G)

print("Graph loaded and cleaned")
print("Nodes:", len(G.nodes))
print("Edges:", len(G.edges))

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

    # -------- A* --------
    t0 = time.perf_counter()
    try:
        astar_path = compute_astar_path(G, start, goal)
        astar_time = (time.perf_counter() - t0) * 1000
        astar_cost = compute_path_length(G, astar_path)
        astar_len = len(astar_path)
        astar_success += 1
    except:
        astar_path = []
        astar_time = 0
        astar_cost = 0
        astar_len = 0

    # -------- BFS --------
    bfs_result = run_bfs(G, start, goal)
    if bfs_result:
        bfs_time = bfs_result["time"]
        bfs_cost = bfs_result["cost"]
        bfs_len = len(bfs_result["path"])
        bfs_success += 1
    else:
        bfs_time = 0
        bfs_cost = 0
        bfs_len = 0

    # -------- DFS --------
    dfs_result = run_dfs(G, start, goal)
    if dfs_result:
        dfs_time = dfs_result["time"]
        dfs_cost = dfs_result["cost"]
        dfs_len = len(dfs_result["path"])
        dfs_success += 1
    else:
        dfs_time = 0
        dfs_cost = 0
        dfs_len = 0

    # -------- STORE RESULTS --------
    results.append({
        "astar_time": astar_time,
        "astar_cost": astar_cost,
        "astar_length": astar_len,

        "bfs_time": bfs_time,
        "bfs_cost": bfs_cost,
        "bfs_length": bfs_len,

        "dfs_time": dfs_time,
        "dfs_cost": dfs_cost,
        "dfs_length": dfs_len,
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