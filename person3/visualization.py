import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import math
from matplotlib.animation import FuncAnimation


# WINDOW 1: MOUSE INTERACTION


def interactive_route_selection(G, pos):

    fig, ax = plt.subplots(figsize=(10,10))

    state = {
        "start": None,
        "goal": None,
        "done": False
    }

    def find_nearest(x, y):
        best = None
        dist = float("inf")

        for n in G.nodes:
            nx_, ny_ = pos[n]
            d = math.sqrt((nx_ - x)**2 + (ny_ - y)**2)

            if d < dist:
                dist = d
                best = n

        return best

    def redraw():
        ax.clear()

        nx.draw(
            G.to_undirected(),
            pos,
            node_size=3,
            edge_color="#bbbbbb",
            width=0.6,
            ax=ax
        )

        if state["start"]:
            nx.draw_networkx_nodes(
                G, pos,
                nodelist=[state["start"]],
                node_color="green",
                node_size=120,
                ax=ax
            )

        if state["goal"]:
            nx.draw_networkx_nodes(
                G, pos,
                nodelist=[state["goal"]],
                node_color="red",
                node_size=120,
                ax=ax
            )

        ax.set_title("Click once -> Start | Click again -> Goal")
        plt.axis("off")
        plt.draw()

    def on_click(event):

        if event.inaxes != ax:
            return

        node = find_nearest(event.xdata, event.ydata)

        if state["start"] is None:
            state["start"] = node

        elif state["goal"] is None:
            state["goal"] = node
            state["done"] = True


        redraw()

    fig.canvas.mpl_connect("button_press_event", on_click)
    
    redraw()   #draw graph before waiting for clicks
    while not state["done"]:
        plt.pause(0.1)

    plt.close(fig)
    return state["start"], state["goal"]

    
 # WINDOW 2: A* ANIMATION   

def animate_path(G, pos, path):

    fig, ax = plt.subplots(figsize=(10,10))

    nx.draw(
        G.to_undirected(),
        pos,
        node_size=3,
        edge_color="#bbbbbb",
        width=0.6,
        ax=ax
    )

    ax.set_title("A* Route Navigation")
    ax.axis("off")

    drawn_edges = []

    for i in range(len(path)-1):
        edge = (path[i], path[i+1])
        drawn_edges.append(edge)

        nx.draw_networkx_edges(
            G.to_undirected(),
            pos,
            edgelist=drawn_edges,
            edge_color="blue",
            width=3,
            ax=ax
        )

        plt.pause(0.3)

    plt.show()

# WINDOW 3: FULL GRAPH + PATH COMPARISON

def visualize_comparison(G, pos,start,goal,astar_path,bfs_path,dfs_path):
   
    fig, axes = plt.subplots(1, 3, figsize=(18, 6)) 

    def draw(ax,path,title,color):
        nx.draw(
            G.to_undirected(),
            pos,
            node_size=3,
            edge_color="#bbbbbb",
            width =0.7,
            alpha=1,
            ax=ax
        )

        edges=list(zip(path, path[1:])) 
        nx.draw_networkx_edges(G.to_undirected(), 
                               pos,
                            edgelist=edges,
                            edge_color=color,
                            width=4,
                            alpha=0.7,
                            ax=ax)

        nx.draw_networkx_nodes(G, 
                           pos, 
                           nodelist=[start,goal], 
                           node_color=['green','red'], 
                           node_size=150, 
                           ax=ax)   
        
        ax.set_title(title)
        ax.axis('off') 

    draw(axes[0], astar_path, "A* Path", 'blue')
    draw(axes[1], bfs_path, "BFS Path", 'green')
    draw(axes[2], dfs_path, "DFS Path", 'orange')
    legend_handles = [mlines.Line2D([], [], color='blue', linewidth=4, label='A* Path'),
                      mlines.Line2D([], [], color='green', linewidth=4, label='BFS Path'),
                      mlines.Line2D([], [], color='orange', linewidth=4, label='DFS Path')]
    

    fig.legend(handles=legend_handles, loc='upper center',bbox_to_anchor=(0.5, 1.0), ncol=3,fontsize=11)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig("algorithm_comparison.png", dpi=300,bbox_inches="tight")
    plt.show()


# TESTING

if __name__ == "__main__":

    G = nx.read_graphml("person1/mit_clean.graphml")

    pos = {
        n: (float(G.nodes[n]['x']),
            float(G.nodes[n]['y']))
        for n in G.nodes
    }

    #------------------------------------WINDOW 1: USER INTERACTION------------------------------------
    start, goal = interactive_route_selection(G, pos)

    #------------------------------------RUN ALGORITHMS------------------------------------
    astar_path = nx.shortest_path(G, start, goal)                           # to be changed to actual A* path later
    bfs_path = astar_path[::-1]                                            # to be changed to actual BFS path later
    dfs_path = astar_path[:]                                                # to be changed to actual DFS path later


    #------------------------------------WINDOW 2: A* ANIMATION------------------------------------
    animate_path(G, pos, astar_path)    

    #------------------------------------WINDOW 3: FULL GRAPH + PATH COMPARISON------------------------------------
    visualize_comparison(G, pos, start, goal, astar_path, bfs_path, dfs_path)