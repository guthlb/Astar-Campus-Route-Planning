import networkx as nx
import matplotlib.pyplot as plt
import random

# STEP 1: LOAD GRAPH
G = nx.read_graphml("mit_campus.graphml")

print(f"Original Nodes: {len(G.nodes)}")
print(f"Original Edges: {len(G.edges)}")


# STEP 2: PREPROCESS GRAPH
# Convert coordinates
for n in G.nodes:
    G.nodes[n]['x'] = float(G.nodes[n]['x'])
    G.nodes[n]['y'] = float(G.nodes[n]['y'])

# Fix edge weights
for u, v, d in G.edges(data=True):
    try:
        d['length'] = float(d.get('length', 1.0))
    except:
        d['length'] = 1.0

print("Coordinates and weights cleaned.")

# STEP 3: CONNECTED GRAPH
largest_cc = max(nx.connected_components(G.to_undirected()), key=len)
G = G.subgraph(largest_cc).copy()

print(f"Connected Nodes: {len(G.nodes)}")
print(f"Connected Edges: {len(G.edges)}")


# STEP 4: ASSIGN ALPHABET LABELS
def generate_label(index):
    label = ""
    while True:
        label = chr(ord('A') + (index % 26)) + label
        index = index // 26 - 1
        if index < 0:
            break
    return label

for i, node in enumerate(G.nodes):
    G.nodes[node]['label'] = generate_label(i)

print("Nodes labeled as A, B, ..., Z, AA, AB, ...")


# STEP 5: CLEAN GRAPH VISUALIZATION
pos = {n: (G.nodes[n]['x'], G.nodes[n]['y']) for n in G.nodes}

plt.figure(figsize=(10, 10))

# Draw base graph
nx.draw(
    G,
    pos,
    node_size=20,
    edge_color='gray',
    width=0.5,
    alpha=0.7
)

# Label ALL nodes (small font to avoid clutter)
labels = {n: G.nodes[n]['label'] for n in G.nodes}

nx.draw_networkx_labels(
    G,
    pos,
    labels,
    font_size=4
)

plt.title("Campus Graph Representation")

plt.savefig("clean_graph.png", dpi=300, bbox_inches='tight')
print("Clean graph saved as clean_graph.png")

plt.close()

# STEP 6: SAVE CLEAN DATASET
nx.write_graphml(G, "mit_clean.graphml")

print("Clean dataset saved as mit_clean.graphml")


# STEP 7: A* VISUALIZATION
def heuristic(n1, n2):
    x1, y1 = G.nodes[n1]['x'], G.nodes[n1]['y']
    x2, y2 = G.nodes[n2]['x'], G.nodes[n2]['y']
    return abs(x1 - x2) + abs(y1 - y2)

nodes = list(G.nodes)

start = random.choice(nodes)
goal = random.choice(nodes)

while start == goal:
    goal = random.choice(nodes)

path = nx.astar_path(G, start, goal, heuristic=heuristic, weight='length')
path_edges = list(zip(path, path[1:]))

plt.figure(figsize=(10, 10))

# Draw base graph
nx.draw(
    G,
    pos,
    node_size=5,
    edge_color='lightgray',
    width=0.5,
    alpha=0.6
)

# Draw path
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=path_edges,
    edge_color='red',
    width=2
)

# Highlight start and goal
nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color='green', node_size=80, label="Start")
nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color='blue', node_size=80, label="Goal")

# Labels
nx.draw_networkx_labels(G, pos, {start: "Start", goal: "Goal"}, font_size=8)

plt.title("Campus Route Planning using A* Algorithm")
plt.legend()

plt.savefig("astar_visualization.png", dpi=300, bbox_inches='tight')
print("A* visualization saved as astar_visualization.png")

plt.close()

print("\n--- FINAL SUMMARY ---")
print(f"Final Nodes: {len(G.nodes)}")
print(f"Final Edges: {len(G.edges)}")
print("Graph is clean, labeled, connected, and ready for team use.")