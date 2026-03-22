from astar import *

G = load_graph()
G = preprocess_graph(G)
G = get_connected_graph(G)
G = label_nodes(G)

pos = get_positions(G)

label_to_node, _ = create_label_mappings(G)

start = label_to_node["A"]
goal = label_to_node["M"]

path = compute_astar_path(G, start, goal)

visualize_path(G, pos, path, start, goal)