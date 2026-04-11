import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

LAMBDA = 0.222

def build_cayley_lattice_4d(L=6):
    coords = np.array(np.meshgrid(*[range(L)]*4)).reshape(4, -1).T
    G = nx.Graph()
    for i in range(len(coords)):
        G.add_node(i, pos=coords[i])
    return G, coords

if __name__ == "__main__":
    print("Building Cayley Lattice (L=6)...")
    G, coords = build_cayley_lattice_4d(6)
    print(f"Nodes: {G.number_of_nodes()}")
    plt.figure(figsize=(10,10))
    nx.draw(G, pos={i: (coords[i,0], coords[i,1]) for i in range(len(coords))}, node_size=10, alpha=0.5)
    plt.title("Geodesic Map (Cayley Projection)")
    plt.savefig("geodesics_cayley.png")
    print("Map generated: geodesics_cayley.png")
