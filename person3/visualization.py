import networkx as nx
import matplotlib.pyplot as plt

# LOAD GRAPH
G = nx.read_graphml("person1/mit_campus.graphml")

# CREATE POSITION DICTIONARY
pos = {}

for node, data in G.nodes(data=True):
    x = float(data['x'])
    y = float(data['y'])
    pos[node] = (x, y)

# SELECT START & GOAL (temporary testing)
nodes = list(G.nodes)
start = nodes[0] 
goal = nodes[len(nodes)-1] 

# DRAW GRAPH
plt.figure(figsize=(10,10))

nx.draw(
    G,
    pos,
    node_size=5,
    edge_color="gray",
    alpha=0.5
)

nx.draw(G,pos,node_size=5,edge_color="gray",alpha=0.5)

#highlight start and goal nodes
nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color='green', node_size=120, label='Start')
nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color='red', node_size=120, label='Goal')



plt.title("Campus Graph Start & Goal Visualization")
plt.legend()
plt.show()