import networkx as nx
import matplotlib.pyplot as plt
import math
import os

# =========================
# LOAD GRAPH
# =========================
def load_graph():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "mit_campus.graphml")
    G = nx.read_graphml(file_path)
    return G


# =========================
# PREPROCESS GRAPH
# =========================
def preprocess_graph(G):
    for n in G.nodes:
        G.nodes[n]['x'] = float(G.nodes[n]['x'])
        G.nodes[n]['y'] = float(G.nodes[n]['y'])

    for u, v, d in G.edges(data=True):
        try:
            d['length'] = float(d.get('length', 1.0))
        except:
            d['length'] = 1.0

    return G


# =========================
# CONNECT GRAPH
# =========================
def get_connected_graph(G):
    largest_cc = max(nx.connected_components(G.to_undirected()), key=len)
    return G.subgraph(largest_cc).copy()


# =========================
# LABEL GENERATION
# =========================
def generate_label(index):
    label = ""
    while True:
        label = chr(ord('A') + (index % 26)) + label
        index = index // 26 - 1
        if index < 0:
            break
    return label


def label_nodes(G):
    for i, node in enumerate(G.nodes):
        G.nodes[node]['label'] = generate_label(i)
    return G


# =========================
# POSITION MAPPING
# =========================
def get_positions(G):
    return {n: (G.nodes[n]['x'], G.nodes[n]['y']) for n in G.nodes}


# =========================
# SAVE CLEAN GRAPH
# =========================
def save_graph(G, filename="mit_clean.graphml"):
    nx.write_graphml(G, filename)


# =========================
# VISUALIZE GRAPH
# =========================
def visualize_graph(G, pos, filename="clean_graph.png"):
    plt.figure(figsize=(10, 10))

    nx.draw(
        G,
        pos,
        node_size=20,
        edge_color='gray',
        width=0.5,
        alpha=0.7
    )

    labels = {n: G.nodes[n]['label'] for n in G.nodes}

    nx.draw_networkx_labels(
        G,
        pos,
        labels,
        font_size=4
    )

    plt.title("Campus Graph Representation")
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()


# =========================
# LABEL ↔ NODE MAPPING
# =========================
def create_label_mappings(G):
    label_to_node = {}
    node_to_label = {}

    for n in G.nodes:
        label = G.nodes[n]['label']
        label_to_node[label] = n
        node_to_label[n] = label

    return label_to_node, node_to_label


# =========================
# HEURISTIC FUNCTION
# =========================
def heuristic(G, n1, n2):
    x1, y1 = G.nodes[n1]['x'], G.nodes[n1]['y']
    x2, y2 = G.nodes[n2]['x'], G.nodes[n2]['y']
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


# =========================
# A* PATH
# =========================
def compute_astar_path(G, start, goal):
    return nx.astar_path(G, start, goal,
                         heuristic=lambda a, b: heuristic(G, a, b),
                         weight='length')


# =========================
# VISUALIZE PATH
# =========================
def visualize_path(G, pos, path, start, goal, filename="astar_visualization.png"):
    path_edges = list(zip(path, path[1:]))

    plt.figure(figsize=(10, 10))

    nx.draw(
        G,
        pos,
        node_size=5,
        edge_color='lightgray',
        width=0.5,
        alpha=0.6
    )

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=path_edges,
        edge_color='red',
        width=2
    )

    nx.draw_networkx_nodes(
        G, pos,
        nodelist=[start],
        node_color='green',
        node_size=80
    )

    nx.draw_networkx_nodes(
        G, pos,
        nodelist=[goal],
        node_color='blue',
        node_size=80
    )

    nx.draw_networkx_labels(
        G,
        pos,
        {start: "Start", goal: "Goal"},
        font_size=8
    )

    plt.title("Campus Route Planning using A* Algorithm")
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()