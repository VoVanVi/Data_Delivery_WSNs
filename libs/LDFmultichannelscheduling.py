
from libs import main_test
from libs import node
import queue
import sys

vertex_c = []
edge_c = []
L = 4 # L is length of time slot in a period
#I = []
#I_prime = []
#global total_working_period


INFINITY = sys.maxsize - 1

def create_List(r1, r2):
    return [item for item in range(r1, r2+1)]

Sch = create_List(1,10000) # Sch is the set of given channels

def constraint_graph_construction(node_list, debug = False):
    for i in range(0, len(node_list)):
        if node_list[i].childrenIDs != []:
            vertex_c.append(node_list[i].ID)
    # pdb.set_trace()
    if debug:
        print("Vertex in RCG", vertex_c)

    list_intersection = []
    for each_id_i in vertex_c:
        if debug:
            print("-------------------------------------------------------------------------------")
        #print("i in vertex_c:", each_id_i)
        for each_id_j in vertex_c:
            if node_list[each_id_j].ID != node_list[each_id_i].ID:
                #list_intersection = []
                if debug:
                    print("value of node at i:", each_id_i)
                    print("Value of node at j", each_id_j)
                    print("node_list[i].neighbors:", node_list[each_id_i].neighborIDs)
                    print("node_list[j].childrenIDs:", node_list[each_id_j].childrenIDs)
                    print("node_list[i].childrenIDs", node_list[each_id_i].childrenIDs)
                    print("node_list[j].neighbors", node_list[each_id_j].neighborIDs)
                if list(set(node_list[each_id_i].neighborIDs).intersection(set(node_list[each_id_j].childrenIDs))) != []\
                        or list(set(node_list[each_id_i].childrenIDs).intersection(set(node_list[each_id_j].neighborIDs))) != []:
                    node_list[each_id_i].neighborIDs_gc.append(each_id_j)

                    if (node_list[each_id_j].ID, node_list[each_id_i].ID) not in edge_c:
                        edge_c.append((node_list[each_id_j].ID, node_list[each_id_i].ID))
                #print("Neighbors of node i:", node_list[each_id_i].neighborIDs_gc)
                #list_intersection = list(set(node_list[each_id_i].neighborIDs).intersection(set(node_list[each_id_j].neighborIDs)))
                """
                for each_child_i in node_list[each_id_i].childrenIDs:
                    for each_child_j in node_list[each_id_j].childrenIDs:
                        if each_child_i in node_list[each_id_j].neighborIDs or each_child_j in node_list[each_id_i].neighborIDs:
                            node_list[each_id_i].neighborIDs_gc.append(each_id_j)

                            if (node_list[each_id_j].ID, node_list[each_id_i].ID) not in edge_c:
                                edge_c.append((node_list[each_id_j].ID, node_list[each_id_i].ID))
                """

            """            
                print("list intersection:", list_intersection)
                if list_intersection != []:
                    t = 0
                    for each_id in list_intersection:
                        if each_id in vertex_c:
                            t = t + 1
                    if t != 0:
                        node_list[each_id_i].neighborIDs_gc.append(each_id_j)
            """



        if debug:
            print("edge_c:", edge_c)

    """
    for each_id_i in vertex_c:
        for each_id_j in vertex_c:
            if node_list[each_id_j].ID in node_list[each_id_i].neighborIDs and node_list[each_id_j].ID != node_list[each_id_i].ID:
                node_list[each_id_i].neighborIDs_gc.append(each_id_j)
    """

def topo_example():
    node_list = []

    root = node.Node(0, 0, 0)
    node1 = node.Node(1, 1, 1)
    node2 = node.Node(2, 2, 2)
    node3 = node.Node(3, 3, 3)
    node4 = node.Node(4, 4, 4)
    node5 = node.Node(5, 5, 5)
    node6 = node.Node(6, 6, 6)
    node7 = node.Node(7, 7, 7)
    node8 = node.Node(8, 8, 8)
    node9 = node.Node(9, 9, 9)
    node10 = node.Node(10, 10, 10)
    node11 = node.Node(11, 11, 11)
    node12 = node.Node(12, 12, 12)
    node13 = node.Node(13, 13, 13)
    node14 = node.Node(14, 14, 14)
    node15 = node.Node(15, 15, 15)
    node16 = node.Node(16, 16, 16)

    node_list.append(root)
    node_list.append(node1)
    node_list.append(node2)
    node_list.append(node3)
    node_list.append(node4)
    node_list.append(node5)
    node_list.append(node6)
    node_list.append(node7)
    node_list.append(node8)
    node_list.append(node9)
    node_list.append(node10)
    node_list.append(node11)
    node_list.append(node12)
    node_list.append(node13)
    node_list.append(node14)
    node_list.append(node15)
    node_list.append(node16)

    node_list[0].childrenIDs = [node_list[1].ID, node_list[2].ID]
    node_list[0].neighborIDs = [node_list[1].ID, node_list[2].ID]

    node_list[1].neighborIDs = [node_list[0].ID, node_list[2].ID, node_list[3].ID, node_list[9].ID]
    node_list[1].parentID = node_list[0].ID
    node_list[1].childrenIDs = [node_list[3].ID, node_list[9].ID]

    node_list[2].neighborIDs = [node_list[0].ID, node_list[1].ID, node_list[4].ID, node_list[5].ID]
    node_list[2].parentID = node_list[0].ID
    node_list[2].childrenIDs = [node_list[4].ID, node_list[5].ID]

    node_list[3].neighborIDs = [node_list[1].ID, node_list[6].ID, node_list[7].ID, node_list[9].ID]
    node_list[3].parentID = node_list[1].ID
    node_list[3].childrenIDs = [node_list[6].ID, node_list[7].ID]

    node_list[4].neighborIDs = [node_list[2].ID, node_list[5].ID, node_list[9].ID, node_list[10].ID]
    node_list[4].parentID = node_list[2].ID
    node_list[4].childrenIDs = [node_list[10].ID]

    node_list[5].neighborIDs = [node_list[2].ID, node_list[4].ID, node_list[8].ID, node_list[10].ID, node_list[11].ID]
    node_list[5].parentID = node_list[2].ID
    node_list[5].childrenIDs = [node_list[8].ID, node_list[11].ID]

    node_list[6].neighborIDs = [node_list[3].ID, node_list[7].ID, node_list[12].ID, node_list[13].ID]
    node_list[6].parentID = node_list[3].ID
    node_list[6].childrenIDs = [node_list[12].ID]

    node_list[7].neighborIDs = [node_list[3].ID, node_list[6].ID, node_list[9].ID, node_list[12].ID, node_list[13].ID, node_list[14].ID]
    node_list[7].parentID = node_list[3].ID
    node_list[7].childrenIDs = [node_list[13].ID, node_list[14].ID]

    node_list[8].neighborIDs = [node_list[5].ID, node_list[15].ID, node_list[16].ID]
    node_list[8].parentID = node_list[5].ID
    node_list[8].childrenIDs = [node_list[15].ID, node_list[16].ID]

    node_list[9].neighborIDs = [node_list[1].ID, node_list[3].ID, node_list[4].ID, node_list[7].ID]
    node_list[9].parentID = node_list[1].ID
    node_list[9].childrenIDs = []

    node_list[10].neighborIDs = [node_list[4].ID, node_list[5].ID]
    node_list[10].parentID = node_list[4].ID
    node_list[10].childrenIDs = []

    node_list[11].neighborIDs = [node_list[5].ID]
    node_list[11].parentID = node_list[5].ID
    node_list[11].childrenIDs = []

    node_list[12].neighborIDs = [node_list[6].ID, node_list[7].ID]
    node_list[12].parentID = node_list[6].ID
    node_list[12].childrenIDs = []

    node_list[13].neighborIDs = [node_list[6].ID, node_list[7].ID]
    node_list[13].parentID = node_list[7].ID
    node_list[13].childrenIDs = []

    node_list[14].neighborIDs = [node_list[7].ID]
    node_list[14].parentID = node_list[7].ID
    node_list[14].childrenIDs = []

    node_list[15].neighborIDs = [node_list[8].ID]
    node_list[15].parentID = node_list[8].ID
    node_list[15].childrenIDs = []

    node_list[16].neighborIDs = [node_list[8].ID]
    node_list[16].parentID = node_list[8].ID
    node_list[16].childrenIDs = []

    return node_list

def frequency_assignment(node_list, debug = False):
    fre_assigned_node_list = []

    while (len(fre_assigned_node_list) != len(vertex_c)):
        u = 0
        sum_degree = 0
        for each_id in vertex_c:
            #print("each ID in vertex_c:", each_id)
            if node_list[each_id].channel == 0:
                if len(node_list[each_id].neighborIDs_gc) >= sum_degree:
                    sum_degree = len(node_list[each_id].neighborIDs_gc)
                    u = each_id
        if debug:
            print("Node has maximum degree:", u)
        # list of channel to avoid collision
        I = []
        for each_id in node_list[u].neighborIDs_gc:
            #if node_list[each_id].channel != 0:
            #if (each_id, u) in edge_c:
            I.append(node_list[each_id].channel)
        if debug:
            print("List of channel to avoid collision:", I)
        node_list[u].channel = min(list(set(Sch) - set(I)))
        if debug:
            print("neighbors of node %u: %u" % (u, len(node_list[u].neighborIDs_gc)))
            print("channel of node %u is: %u" % (u, node_list[u].channel))
        fre_assigned_node_list.append(u)

def timeslot_assignment(node_list, debug = False):
    # Assign timeslot using a Breadth First Search order
    for each_node in node_list:
        each_node.distance = INFINITY
    node_list[0].distance = 0
    q = queue.Queue()
    q.put(node_list[0])
    count = 0
    while q.empty() is False:
        current = q.get()
        count += 1
        for each_node_id in current.neighborIDs:
            if node_list[each_node_id].distance == INFINITY:
                node_list[each_node_id].distance = current.distance + 1
                node_list[each_node_id].parentID = current.ID
                current.childrenIDs.append(each_node_id)
                q.put(node_list[each_node_id])
    else:
        if count < len(node_list):
            print("Disconnected network!!!")
            return False
    return True

def scheduling(node_list, debug = True):
    constraint_graph_construction(node_list, False)
    frequency_assignment(node_list, False)
    freq_list = []
    for each_node in node_list:
        freq_list.append(each_node.channel)
    if debug:
        print("frequency list: ", freq_list)
        m = max(freq_list)
        print("maximum frequency:", m)
    ts_assigned_node_list = []
    #while len(ts_assigned_node_list) != len(node_list):

#if __name__=="__main__":
    #node_list = topo_example()
    #scheduling(node_list)
