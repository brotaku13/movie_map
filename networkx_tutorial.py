import networkx as nx

"""By definition, a Graph is a collection of nodes (vertices) along with identified pairs of nodes
(called edges, links, etc). In NetworkX, nodes can be any hashable
object e.g., a text string, an image, an XML object, another Graph, a customized node object, etc."""
G = nx.Graph()

"""Growing the Graph"""

#one node at a time
G.add_node(1)

#adding a list of nodes
G.add_nodes_from([0, 1, 2])

#add any iterable container of nodes.
H = nx.path_graph(10)
G.add_nodes_from(H)
# this means that the nodes of H are also the nodes of G

#could also add an entire list of nodes as a single node in G
G.add_node(H)

#this means you can create:
    #graphs of graphs
    #graphs of files
    #graphs of functions

#the graph can be grown by adding edges
G.add_edge(1, 2)
e = (2, 3)
G.add_edge(*e) # here the *e means to unpack the tuple

#adding a list of edges
l = [(4, 5), (5, 6)]
G.add_edges_from(l)

#adding an ebunch: an iterable container of edge tuples
#can be a 2-tuple of nodes or a 3-tuple with 2 nodes followed by an edge attribute dictionary,
G.add_edges_from(H.edges)

#clear graph using
G.clear()

#when adding new nodes and edges, networkx disregards any that are already present
G.add_edges_from([(1, 2), (1, 3)])
G.add_node(1)
G.add_edge(1, 2)
G.add_node("spam")  #adds node "spam"
G.add_nodes_from("spam")  #adds 4 nodes, 's', 'p'...
G.add_edge(3, 'm')

#this graph contains 8 nodes and 3 edges
# G.number_of_nodes() -> 8
# G.number_of_edges() -> 3

#graph reporting
#G.nodes, G.edges, G.adj, G.degree
    #set like views of nodes, edges, neighbors(adjacencies) and degrees of nodes in a graph
    #can iterate through data attributes using .items()
    #can specify container type (sets, lists, dicts, tuples)

list(G.nodes)  # ['a', 1, 2, 3, 'spam', 'm', 'p', 's']
list(G.edges)  #  [(1, 2), (1, 3), (3, 'm')]
list(G.adj[1])  # or list(G.neighbors(1))
                # [2, 3]
G.degree[1]  # the number of edges incident to 1
            # -> 2

#removing nodes
G.remove_node(2)
G.remove_nodes_from("spam")
list(G.nodes)  # [1, 3, 'spam']
G.remove_edge(1, 3)

# creating graph structure with data
G.add_edge(1, 2)
H = nx.DiGraph(G)  # creating a directional graph using the connections from G
list(H.edges())  # [(1, 2), (2, 1)]
edgelist = [(0, 1), (1, 2), (2, 3)]
H = nx.Graph(edgelist)

"""Node Objects"""

# nodes can be any hashable object (except None)
# an edge can be associated with any object x using
    # G.add_edge(n1, n2, object=x)

        # here, n1 and n2 could be protein objects
        # x could refer to an xml record of publications
        # if nodes are movies then the connections can be actor, director, etc

'''accessing edges and neighbors'''

# can use subscript notation
G[1]  # same as G.adj[1]  -> AtlasView({2: {}})

# can get and set attributes of an edge using subscript notation if the edge already
# exists
G.add_edge(1, 3)
G[1][3]['color'] = "blue"
G.edges[1, 2]['color'] = "red"

# fast examination of all(node, adjacency) pairs is achieved using G.adjacency() or G.adj.items()
FG = nx.Graph()
FG.add_weighted_edges_from([(1, 2, 0.125), (1, 3, 0.75), (2, 4, 1.2), (3, 4, 0.375)])
for n, nbrs in FG.adj.items():
    for nbr, eattr in nbrs.items():
        wt = eattr['weight']
        if wt < 0.5:
            print('(%d, %d, %.3f)' % (n, nbr, wt))

'''
(1, 2, 0.125)
(2, 1, 0.125)
(3, 4, 0.375)
(4, 3, 0.375)
'''

#access to edges is achieved with the edges property
for (u, v, wt) in FG.edges.data('weight'):
    if wt < 0.5: print('(%d, %d, %.3f)' % (u, v, wt))

'''
(1, 2, 0.125)
(3, 4, 0.375)
'''


'''Adding attributes to graphs, nodes and edges'''
#weights, labels, colors, or whatever python object you like can be attached to graphs, nodes, or edges
# each graph node and edge can hold key / value attribute pairs in an associated attribute dictionary
#empty by default
#attributes can be added or changed using add_edge, add_node, or direct manipulation
# of the attribute dictionaries named G.graph, G.nodes, and G.edges for a graph G

'''Graph attributes'''
# can assign graph attributes when creating a new graph
G = nx.Graph(day="friday")
G.graph # -> {'day': 'Friday'}

#modify attributes later
G.graph['day'] = "monday"
G.graph  # -> {'day': 'monday'}

'''Node attributes'''
# add node attributes using add_node(), add_nodes_from(), or G.nodes()
G.clear()
G.add_node(1, time='5pm')
G.add_nodes_from([3], time='2pm')
G.nodes[1]  # -> {'time': '5pm'}
G.nodes[1]['room'] = 714
G.nodes.data() # -> NodeDataView({1: {'room': 714, 'time': '5pm'}, 3: {'time': '2pm'}})

#adding a node to G.nodes does not add it to the graph

'''Edge Attributes'''
# add or change edge attributes using add_edge(), or add_edges_from()
# or even using subscript notation

G.add_edge(1, 2, weight=4.7)
G.add_edges_from([(3, 4), (4, 5)], color='red')
G.add_edges_from([(1, 2, {'color': 'blue'}), (2, 3, {'weight': 8})])
G[1][2]['weight'] = 4.7
G.edges[3, 4]['weight'] = 4.2

