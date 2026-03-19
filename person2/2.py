import networkx as nx
import matplotlib.pyplot as plt
import math
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
# ---------------- LOAD GRAPH ----------------
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "mit_campus.graphml")

G = nx.read_graphml(file_path)

# ---------------- PREPROCESS ----------------
for n in G.nodes:
    G.nodes[n]['x'] = float(G.nodes[n]['x'])
    G.nodes[n]['y'] = float(G.nodes[n]['y'])

for u, v, d in G.edges(data=True):
    try:
        d['length'] = float(d.get('length', 1.0))
    except:
        d['length'] = 1.0

# Connected graph
largest_cc = max(nx.connected_components(G.to_undirected()), key=len)
G = G.subgraph(largest_cc).copy()

# Labels
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

pos = {n: (G.nodes[n]['x'], G.nodes[n]['y']) for n in G.nodes}

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

# ---------------- INTERACTION ----------------
state = {
    'start': None,
    'goal': None,
    'bfs': [],
    'dfs': []
}

def find_nearest(x, y):
    best = None
    dist = float('inf')
    for n in G.nodes:
        nx_, ny_ = pos[n]
        d = math.sqrt((nx_ - x)**2 + (ny_ - y)**2)
        if d < dist:
            dist = d
            best = n
    return best

def redraw():
    ax.clear()

    nx.draw(G, pos, node_size=10, edge_color='gray', alpha=0.5)

    # BFS path
    if state['bfs']:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=list(zip(state['bfs'], state['bfs'][1:])),
            edge_color='yellow',
            width=3
        )

    # DFS path
    if state['dfs']:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=list(zip(state['dfs'], state['dfs'][1:])),
            edge_color='blue',
            width=3
        )

    # Start / Goal
    if state['start']:
        nx.draw_networkx_nodes(G, pos, nodelist=[state['start']], node_color='green', node_size=100)

    if state['goal']:
        nx.draw_networkx_nodes(G, pos, nodelist=[state['goal']], node_color='red', node_size=100)

    # Stats
    if state['bfs'] and state['dfs']:
        bfs_len = len(state['bfs'])
        dfs_len = len(state['dfs'])

        ax.set_title(
            f"BFS: {bfs_len} nodes | DFS: {dfs_len} nodes",
            fontsize=12
        )

    plt.draw()

def on_click(event):
    if event.inaxes != ax:
        return

    node = find_nearest(event.xdata, event.ydata)

    if state['start'] is None:
        state['start'] = node
        print("Start:", G.nodes[node]['label'])

    elif state['goal'] is None:
        if node == state['start']:
            return

        state['goal'] = node
        print("Goal:", G.nodes[node]['label'])

        # RUN BFS & DFS
        state['bfs'] = run_bfs(G, state['start'], state['goal'])
        state['dfs'] = run_dfs(G, state['start'], state['goal'])

        print("\nBFS length:", len(state['bfs']))
        print("DFS length:", len(state['dfs']))

    else:
        # reset
        state['start'] = node
        state['goal'] = None
        state['bfs'] = []
        state['dfs'] = []

    redraw()

# ---------------- PLOT ----------------
fig, ax = plt.subplots(figsize=(10, 10))
fig.canvas.mpl_connect('button_press_event', on_click)

print("\nClick once → Start")
print("Click again → Goal")
print("Click again → Reset")

redraw()
plt.show()