import networkx as nx
import matplotlib.pyplot as plt
import scipy

"""
https://networkx.github.io/documentation/latest/reference/generators.html
"""
def practice():
    Peterson = nx.petersen_graph()
    tutte = nx.tutte_graph()
    maze = nx.sedgewick_maze_graph()
    tet = nx.tetrahedral_graph()
    G = nx.random_tree(20)



    nx.draw(G, pos=nx.spring_layout(G), with_labels=True)
    #nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

    plt.show()

def movie_map_example():
    G = nx.balanced_tree(3, 3)  # (splits per node, height h)
    nx.draw(G, pos=nx.spring_layout(G), with_labels=True)

def main():
    practice()

main()
