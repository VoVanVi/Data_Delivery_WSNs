"""@package docstring
Programmed by Dzung T. Nguyen @SKKU, Korea
For drawing the constructed tree


- 2017 April 24: Added histogram() function
"""

from libs import gentopo
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


def draw(node_list, show_edge=None, title=None):
    """

    :param node_list: the data structure of the whole network
    :param show_edge: set to False if we just display tree links, no communication edges
    :param title: title of the drawing
    :return: None
    """
    plt.clf()
    g = nx.Graph()
    node_id_list = [node.ID for node in node_list]
    g.add_nodes_from(node_id_list)
    solid_edges = []
    dotted_edges = []
    for each_node in node_id_list:
        for eachChildNodeID in node_list[each_node].childrenIDs:
            solid_edges.append((each_node, eachChildNodeID))
            pass
    for each_node in node_id_list:
        for eachNeighborID in node_list[each_node].neighborIDs:
            if not g.has_edge(each_node, eachNeighborID):
                if (each_node, eachNeighborID) not in solid_edges and (eachNeighborID, each_node) not in solid_edges:
                #g.add_edge(each_node, eachNeighborID)
                    dotted_edges.append((each_node, eachNeighborID))

    for_drawing = {node.ID : np.array([int(node.x), int(node.y)]) for node in node_list}
    #labels = {eachNode : str(eachNode.ID) for eachNode in node_list}
    #edge_labels = {edge : "%u,%u" %(node_list[edge[1]].rT, node_list[edge[1]].st) for edge in solid_edges}
    #for u, v in g.edges():
    #    edge_labels[(u,v)] = "%.2f" % node_list[u].linkToNeighbors[v]

    nx.draw_networkx_nodes(g, pos = for_drawing, node_color = 'y', with_labels = True,  node_size = 300)
    nx.draw_networkx_nodes(g, pos=for_drawing, nodelist=[0], node_color='r', with_labels=True, node_size=700)
    nx.draw_networkx_labels(g, pos = for_drawing, font_size = 8)
    nx.draw_networkx_edges(g, pos = for_drawing, edgelist= solid_edges, style = 'solid')
    if show_edge == 1:
        nx.draw_networkx_edges(g, pos = for_drawing, edgelist= dotted_edges, style = 'dotted')
    #nx.draw_networkx_edge_labels(g, pos = for_drawing, edge_labels = edge_labels, label_pos = 0.3, font_size = 11)
    #plt.grid(True)
    if title:
        plt.title(title)
    plt.show()


def nice_draw(node_list, show_edge=None, title=None):
    """
    Draw the network ignoring the real position in the field. Only the tree links are considered.
    :param node_list: the data structure of the whole network
    :param show_edge: set to False if we just display tree links, no communication edges
    :param title: title of the drawing
    :return: None
    """

    G = nx.DiGraph()
    node_ID_list = [node.ID for node in node_list]
    G.add_nodes_from(node_ID_list)
    for i in range(1, len(node_list)):
        G.add_edge(node_list[i].ID, node_list[i].parentID)

    #pos = nx.graphviz_layout(G)
    node_labels = {node: node for node in G.nodes()}
    #edge_labels = {edge: "%u,%u" % (node_list[edge[0]].rT, node_list[edge[0]].st) for edge in G.edges()}
    #edge_labels = {edge: "%u" % (node_list[edge[0]].rT) for edge in G.edges()}
    nx.draw_networkx_nodes(G, pos=graphviz_layout(G), node_color='y', with_labels=True, node_size=700)
    nx.draw_networkx_nodes(G, pos=graphviz_layout(G), nodelist=[0], node_color='r', node_size=1500)
    nx.draw_networkx_labels(G, pos=graphviz_layout(G), labels=node_labels)
    nx.draw_networkx_edges(G, pos=graphviz_layout(G), arrows=True)
    #nx.draw_networkx_edge_labels(G, pos=graphviz_layout(G), edge_labels = edge_labels, label_pos = 0.7, font_size = 11)
    plt.show()
    pass


def histogram_criticality(node_list, title = "Your title"):
    """
    Ploting the criticality histogram of a node_list. TREE CONSTRUCTED.
    :param node_list:
    :return:
    """
    gentopo.criticality_update_id_hc(node_list)
    bins = np.linspace(0.,1.,21)
    print(bins)
    values = [node_list[x].criticality for x in range(0, len(node_list))]
    plt.hist(values, bins=bins)
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.xlim((0, 1.0))
    plt.xticks(np.arange(0, 1, 0.05))
    plt.show()


def histogram_numchildren(node_list, title = "Your title"):
    """
    Ploting the criticality histogram of a node_list. TREE CONSTRUCTED.
    :param node_list:
    :return:
    """
    #gentopo.criticality_update_id_hc(node_list)
    #bins = np.linspace(0.,1.,21)
    #print bins
    values = [len(node_list[x].childrenIDs) for x in range(0, len(node_list))]
    maxval = max(values)
    bins = np.arange(0, maxval+1)
    plt.hist(values, bins=bins)
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.xlim((0, 1.0))
    plt.xticks(np.arange(0, maxval, 1))
    plt.show()