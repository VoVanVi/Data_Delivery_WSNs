
from libs import gentopo
from libs import node
import pdb
import queue

vertex_c = []
edge_c = []
T = 10 # L is length of time slot in a period




def create_List(r1, r2):
    return [item for item in range(r1, r2+1)]

def link(u, v):
    return (u, v)

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def layering(node_list):
    """

    :param node_list:
    :return:
    """

    N = len(node_list)
    node_list[0].layer = 0
    traversed = [0]
    remaining = [i for i in range(1, N)]
    current_layer = 0
    while len(remaining) > 0:
        traversing = set([])
        for i in traversed:
            if node_list[i].layer == current_layer:
                for k in remaining:
                    if k in node_list[i].neighborIDs:
                        node_list[i].next_layer_neighbors.append(k)
                        node_list[k].prev_layer_neighbors.append(i)
                        node_list[k].layer = current_layer + 1
                        traversing.add(k)
        traversed += list(traversing)
        remaining = [x for x in remaining if x not in traversing]
        current_layer += 1
    return node_list, current_layer

def find_mis(node_list):
    node_list, max_layer = layering(node_list)
    mis = []
    mis.append(0)
    """
    Create a queue to store nodes in next layers in order, then we can check nodes one by one from layer 0 to max layer
    """
    q = queue.Queue()
    for each_node in node_list[0].next_layer_neighbors:
        q.put(each_node)
    while q.empty() is False:
        current = q.get()
        """
        The temp variable t is a list:
            - t stores only value 0, then the node will be added to mis
            - t has value 1 in the list, it means that there is some neighboring node of the considering node. 
        """
        t = []
        for i in mis:
            for each_next_neighborID in node_list[current].next_layer_neighbors:
                if each_next_neighborID not in q.queue:
                    q.put(each_next_neighborID)
            if current in node_list[i].neighborIDs:
                t.append(1)
            else:
                t.append(0)
        if sum(t) == 0:
            mis.append(current)
    copy_mis = mis
    for each_i in copy_mis:
        for each_j in mis:
            if each_i in node_list[each_j].neighborIDs:
                print(each_i, "is a neighbor of", each_j)

    return mis, max_layer

def tree_construction_based_mis(node_list):
    #for each_node in range(0, len(node_list)):

    for each_neighbor in node_list[0].next_layer_neighbors:
        node_list[0].childrenIDs.append(each_neighbor)
        node_list[each_neighbor].parentID = 0

    blue_nodes = []
    white_nodes = []
    black_nodes, max_layer = find_mis(node_list)
    print("black nodes", black_nodes)
    q = queue.Queue()

    for i in range(1, max_layer+1):
        for each_node in range(0, len(node_list)):
            if node_list[each_node].layer == i:
                q.put(each_node)

    while q.empty() is False:
        current = q.get()
        if current in black_nodes:
            t = 100
            selected_parent = None
            for each_node in node_list[current].prev_layer_neighbors:
                if len(node_list[each_node].childrenIDs) <= t:
                    t = len(node_list[each_node].childrenIDs)
                    selected_parent = each_node
            node_list[current].parentID = selected_parent
            node_list[selected_parent].childrenIDs.append(current)
            if selected_parent not in blue_nodes:
                blue_nodes.append(selected_parent)
        else:
            prev_current_layer_neighbors = list(set(node_list[current].neighborIDs) - set(
                node_list[current].next_layer_neighbors))
            black_neighbors = intersection(black_nodes, prev_current_layer_neighbors)
            t = 100
            selected_parent = None
            for each_node in black_neighbors:
                if len(node_list[each_node].childrenIDs) <= t:
                    t = len(node_list[each_node].childrenIDs)
                    selected_parent = each_node
            node_list[current].parentID = selected_parent
            node_list[selected_parent].childrenIDs.append(current)

    for each_node in range(0, len(node_list)):
        if each_node not in black_nodes and each_node not in blue_nodes:
            white_nodes.append(each_node)

    print("length of all nodes", len(blue_nodes)+ len(black_nodes) +len(white_nodes))
    print("blue nodes", blue_nodes)

    return black_nodes, blue_nodes, white_nodes

def parent_node_list(node_list, children_list):
    parent_list =[]
    for each_node in children_list:
        if each_node not in parent_list:
            parent_list.append(node_list[each_node].parentID)
    return parent_list

def EDAS(node_list):
    black_nodes, blue_nodes, white_nodes = tree_construction_based_mis(node_list)
    parent_black_nodes = parent_node_list(node_list, black_nodes)
    parent_blue_nodes = parent_node_list(node_list, blue_nodes)
    parent_white_nodes = parent_node_list(node_list, white_nodes)

    ts = 0
    links_selection(node_list, white_nodes, parent_white_nodes, ts)


def links_selection(node_list, Vc, F_Vc, ts):
    while Vc:
        Sc = []
        for vb in F_Vc:
            va = select_one_child(node_list, vb)
            Sc.append(link(va, vb))
            Vc.remove(va)
        #Apply algorithm 3
    return 1

def select_one_child(node_list, parent_node):
    t = 1000
    for each_child in node_list[parent_node].childrenIDs:
        if each_child <= t:
            t = each_child
    return t

def link_schedule(node_list, candidate_links, ts, m):
    return 1
