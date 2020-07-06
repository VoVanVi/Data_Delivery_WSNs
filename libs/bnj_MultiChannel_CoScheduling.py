
from libs import gentopo
from libs import node
import pdb

vertex_c = []
edge_c = []
L = 4 # L is length of time slot in a period
#I = []
#I_prime = []



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

    for each_id_i in vertex_c:
        if debug:
            print("-------------------------------------------------------------------------------")
        #print("i in vertex_c:", vertex_c[i].idx)
        for each_id_j in vertex_c:
            if node_list[each_id_j].ID != node_list[each_id_i].ID:
                if debug:
                    print("value of node at i:", each_id_i)
                    print("Value of node at j", each_id_j)
                    print("node_list[i].neighbors:", node_list[each_id_i].neighborIDs)
                    print("node_list[j].childrenIDs:", node_list[each_id_j].childrenIDs)
                    print("node_list[i].childrenIDs", node_list[each_id_i].childrenIDs)
                    print("node_list[j].neighbors", node_list[each_id_j].neighborIDs)
                if list(set(node_list[each_id_i].neighborIDs).intersection(set(node_list[each_id_j].childrenIDs))) != []\
                        or list(set(node_list[each_id_i].childrenIDs).intersection(set(node_list[each_id_j].neighborIDs))) != []:
                    if (node_list[each_id_j].ID, node_list[each_id_i].ID) not in edge_c:
                        edge_c.append((node_list[each_id_j].ID, node_list[each_id_i].ID))
        if debug:
            print("edge_c:", edge_c)

def bnj_operation(node_list, u, debug = False):
    if debug:
        print("node u", u)
    max_num_of_desc = 0
    selected_neighbor = None
    if debug:
        print("node u has length of descendent less than L", u)
        print("len(node_list[u].descIDs_prime) ", len(node_list[u].descIDs_prime))
        print("neighbor of u", node_list[u].neighborIDs)
    for each_id in list(set(node_list[u].neighborIDs) - set(node_list[u].descIDs_prime) - set(node_list[u].ancestorIDs)):
        if debug:
            print("each neighbor of u:", each_id)
        if node_list[each_id].channel == 0 and node_list[each_id].timeslot == 0:
            if len(node_list[each_id].descIDs_prime) <= L - len(node_list[u].descIDs_prime) - 1:
                if len(node_list[each_id].descIDs_prime) >= max_num_of_desc:
                    max_num_of_desc = len(node_list[each_id].descIDs_prime)
                    selected_neighbor = each_id
    if debug:
        print("selected neighbor:", selected_neighbor)

    if selected_neighbor != None:
        temp_parent = node_list[selected_neighbor].parentID
        node_list[selected_neighbor].parentID = u
        node_list[u].childrenIDs.append(selected_neighbor)
        node_list[u].descIDs_prime.append(selected_neighbor)
        node_list[temp_parent].childrenIDs.remove(selected_neighbor)
        for each_desc in node_list[selected_neighbor].descIDs_prime:
            node_list[temp_parent].descIDs_prime.remove(each_desc)
        for each_id in node_list[selected_neighbor].descIDs_prime:
            node_list[u].descIDs_prime.append(each_id)

    if debug:
        print("selected neighbor:", selected_neighbor)
    return selected_neighbor

def split_children(node_list, u):
    #print("len(node_list[u].childrenIDs)/L ", len(node_list[u].childrenIDs)/L)
    #print("len(node_list[u].childrenIDs) % L", len(node_list[u].childrenIDs) % L )
    if len(node_list[u].childrenIDs)/L > 1 and len(node_list[u].childrenIDs) % L != 0:
        return int(len(node_list[u].childrenIDs)/L) + 1
    if len(node_list[u].childrenIDs) / L > 1 and len(node_list[u].childrenIDs) % L == 0:
        return int(len(node_list[u].childrenIDs) / L)

def assign_working_period(node_list, scheduled_nodes_list, x):
    t = 0
    wp_rx_node_layer_list = []

    for each_node in scheduled_nodes_list:
        for each_id in node_list[x].descIDs_prime:
            if each_node.parentID == node_list[each_id].ID:
                t = t + 1
                wp_rx_node_layer_list.append(each_node.wp)

    z = 0
    wp_children_list = []
    for each_id in node_list[x].childrenIDs:
        if node_list[each_id].channel != 0 and node_list[each_id].timeslot != 0 and node_list[each_id].wp not in wp_children_list:
            wp_children_list.append(node_list[each_id].wp)
            z = z + 1

    if t != 0 and z != 0:
        if max(wp_rx_node_layer_list) > max(wp_children_list):
            node_list[x].wp = max(wp_rx_node_layer_list) + 1
        else:
            node_list[x].wp = max(wp_children_list) + 1

    if t != 0 and z == 0:
        node_list[x].wp = max(wp_rx_node_layer_list) + 1

    if t == 0 and z != 0:
        node_list[x].wp = max(wp_children_list) + 1

    if t == 0 and z == 0:
        node_list[x].wp = 1

def sub_scheduling(node_list, u, channel, wp, sub_children=None, debug=False):

    if sub_children == None:
        """
        Channel allocation
        """
        if debug:
            print("node_list[%u].rx_channel: %u" % (node_list[u].ID, node_list[u].rx_channel))

        for each_id in node_list[u].descIDs_prime:
            if debug:
                print("u.descIDs:", node_list[u].descIDs_prime)
                print("each ID in u:", each_id)

            if node_list[each_id].channel == 0:
                node_list[each_id].channel = channel
                node_list[each_id].wp = wp
                if debug:
                    print("receiving channel of %u: %u" % (each_id, node_list[each_id].rx_channel))
            if debug:
                print("node_list[%u].channel: %u" % (each_id, node_list[each_id].channel))

        """
        Time slot assignment in Bottom up manner
        """
        t = len(node_list[u].descIDs_prime)
        # if len(node_list[u].descIDs_prime) <= L:
        for each_id in node_list[u].descIDs_prime:
            if node_list[each_id].channel != 0:
                node_list[each_id].timeslot = t
                t = t - 1

    else:
        t = 0
        # pdb.set_trace()
        for each_ID in node_list[u].descIDs_prime:
            if debug:
                print("u_prime.childrenIDs", node_list[u].childrenIDs)
                print("u_prime.descIDs:", node_list[u].descIDs_prime)
                print("each ID in u_prime:", each_ID)

            node_list[each_ID].channel = channel
            node_list[each_ID].wp = wp
            t = t + 1
            if debug:
                print("t = ", t)
                print("node_list[%u].channel: %u" % (each_ID, node_list[each_ID].channel))
            if t == L:
                break

        if debug:
            print("node u_prime", node_list[u].ID)
        if node_list[u].ID != 0:
            node_list[u].channel = 0

        """
        #Time slot assignment in Bottom up manner for subtrees having descendent nodes more than L 
        """
        t_prime = 1
        for each_ID in node_list[u].descIDs_prime:
            if node_list[each_ID].channel != 0 and t_prime < (L + 1):
                node_list[each_ID].timeslot = t_prime
                t_prime = t_prime + 1

def coscheduling(node_list, debug = False):
    assigned_wp_list = [0]
    scheduled_nodes = []
    while len(scheduled_nodes) + 1 != len(node_list):
        I = []  # I is the set of channels for avoiding the channel interference
        I_prime = []
        R = []  # R is the set of the nodes that the no. of descendent nodes are less or equal than L (Declared as list)
        R_prime = []  # Set of the set of the nodes that the no. of descendent nodes are larger than L (Declared as list)

        for i in range(len(node_list)):
            if debug:
                print("len(node_list)", len(node_list))
            if node_list[i].childrenIDs != []:
                if debug:
                    print("node list[i].ID", node_list[i].ID)
                    print("node_list[i].descIDs:", node_list[i].descIDs_prime)
                    print("len(node_list[i].descIDs:", len(node_list[i].descIDs_prime))
                if len(node_list[i].descIDs_prime) >= 1 and len(node_list[i].descIDs_prime) <= L:
                    R.append(node_list[i].ID)
                    if debug:
                        print("List R:", R)
                        print("---------------")
                elif len(node_list[i].descIDs_prime) > L:
                    R_prime.append(node_list[i].ID)
        if debug:
            print("List R:", R)
            print("List R_prime:", R_prime)

        #pdb.set_trace()
        u = None  # The node that has maximum descendents in R
        #u_prime = 0
        if R != []:
            """
            Pick up node u such that u has max descendents in the R   
            """

            x = 0  # A temp variable demonstrates number of descendents of a node
            for each_id in R:
                if debug:
                    print("each id", each_id)
                    print("node_list[each_id].descIDs_prime", node_list[each_id].descIDs_prime)
                    print("len(node_list[each_id].descIDs_prime", len(node_list[each_id].descIDs_prime))
                    print("x ", x)
                if len(node_list[each_id].descIDs_prime) > x:
                    x = len(node_list[each_id].descIDs_prime)
                    u = each_id
            if debug:
                print("Node has maximum descendents in R is:", u)
                print("descendent nodes:", node_list[u].descIDs_prime)

            if len(node_list[u].descIDs) < L:
                selected = bnj_operation(node_list, u, False)
                if debug:
                    print("selected node", selected)
                    print("Node u", u)
                    print("node_list[u].descIDs_prime", node_list[u].descIDs_prime)
                vertex_c.clear()
                edge_c.clear()
                constraint_graph_construction(node_list)

        if R == [] and R_prime != []:
            """            
            Pick up node u_prime such that u has minimum descendents in the R_prime for subtrees having 
            descendent nodes more than L aiming to schedule from the leaf to the sink
            """
            x = 1000  # A temp variable demonstrates number of descendents of a node
            for each_node_id in R_prime:
                if debug:
                    print("each node id = ", each_node_id)
                    print("x_prime = ", x)
                if len(node_list[each_node_id].descIDs_prime) <= x:
                    x = len(node_list[each_node_id].descIDs_prime)
                    u = each_node_id
            if debug:
                print("Node has maximum descendents in R is:", u)

        """
        Interference list for u to avoid
        """
        # I is the set of channels for avoiding the channel interference
        for each_id in vertex_c:
            if debug:
                print("(each_id, u): ", (each_id, u))
                print("node_list[each_id].rx_channel ", node_list[each_id].rx_channel)
            if (each_id, u) in edge_c and node_list[each_id].rx_channel != 0 and node_list[each_id].rx_channel not in I:
                I.append(node_list[each_id].rx_channel)
        if debug:
            print("The list I to interference:", I)
            print("node_list[%u].rx_channel)")

        # subtree_collision_list is a set of channel should be avoided when conflict happens with grandchild nodes
        # because the RCG just avoid conflict between parent and its children nodes
        subtree_collision_list = []
        for each_id in node_list[u].descIDs_prime:
            for each_node in scheduled_nodes:
                if each_node.ID in vertex_c:
                    if node_list[each_id].ID in each_node.neighborIDs:
                        if each_node.channel != 0 and each_node.channel not in subtree_collision_list:
                            subtree_collision_list.append(each_node.channel)
                            if debug:
                                print("subtree_collision_list", subtree_collision_list)
                if each_node.ID not in vertex_c:
                    if each_node.ID in node_list[each_id].neighborIDs and each_node.channel not in subtree_collision_list:
                        subtree_collision_list.append(each_node.channel)
        if debug:
            print("set(I)", set(I))
            print("set(I_prime) ", set(I_prime))
            print("set(subtree_collision_list) ", subtree_collision_list)

        for each_node in scheduled_nodes:
            if each_node.ID in vertex_c:
                if node_list[u].ID in each_node.neighborIDs:
                    if each_node.channel != 0 and each_node.channel not in subtree_collision_list:
                        subtree_collision_list.append(each_node.channel)

        #pdb.set_trace()
        if len(node_list[u].descIDs_prime) <= L:

            if debug:
                print("set(I)", set(I))
                print("set(I_prime) ", set(I_prime))
                print("min(list(set(Sch) - set(I)))", min(list(set(Sch) - set(I))))

            assign_working_period(node_list, scheduled_nodes, u)
            # Allocating the lowest channel number for subtrees having length = L
            if debug:
                print("node_list[%u].wp %u" % (u, node_list[u].wp))

            if node_list[u].wp > max(assigned_wp_list):
                node_list[u].rx_channel = 1
            else:
                node_list[u].rx_channel = min(list(set(Sch) - set(I) - set(subtree_collision_list)))
            if debug:
                print("u.channel:", node_list[u].rx_channel)

            sub_scheduling(node_list, u, node_list[u].rx_channel, node_list[u].wp)
        """
        if len(node_list[u].descIDs_prime) < L:
            bnj_operation(node_list, u, False)
            if debug:
                print("Node u", u)
                print("node_list[u].descIDs_prime", node_list[u].descIDs_prime)

            assign_working_period(node_list, scheduled_nodes, u)

            if debug:
                print("node_list[%u].wp %u" % (u, node_list[u].wp))

            if node_list[u].wp > max(assigned_wp_list):
                node_list[u].rx_channel = 1
            else:
                node_list[u].rx_channel = min(list(set(Sch) - set(I) - set(I_prime)))

            if debug:
                print("u.channel:", node_list[u].rx_channel)

            sub_scheduling(node_list, u, node_list[u].rx_channel, node_list[u].wp)
        """
        if len(node_list[u].descIDs_prime) > L:
            sub_children = split_children(node_list, u)
            if debug:
                print("sub children:", sub_children)

            if debug:
                print("set(I)", set(I))
                print("set(I_prime) ", set(I_prime))
                print("min(list(set(Sch) - set(I)))", min(list(set(Sch) - set(I))))
                print("min(list(set(Sch) - set(I) - set(I_prime)))", min(list(set(Sch) - set(I) - set(I_prime))))

            assign_working_period(node_list, scheduled_nodes, u)
            if debug:
                print("node_list[%u].wp %u" % (u, node_list[u].wp))

            if node_list[u].wp > max(assigned_wp_list):
                node_list[u].rx_channel = 1
            else:
                node_list[u].rx_channel = min(list(set(Sch) - set(I) - set(subtree_collision_list)))
            if debug:
                print("u.channel:", node_list[u].rx_channel)

            sub_scheduling(node_list, u, node_list[u].rx_channel, node_list[u].wp, sub_children)

        for each_node in node_list:
            if debug:
                print("channel and timeslot of node %u: %u %u %u" % (each_node.ID, each_node.wp, each_node.channel,
                                                                     each_node.timeslot))

        for each_node in node_list:
            if each_node.channel != 0 and each_node.timeslot != 0 and each_node not in scheduled_nodes:
                scheduled_nodes.append(each_node)
                if each_node.wp not in assigned_wp_list:
                    assigned_wp_list.append(each_node.wp)

        if len(scheduled_nodes) + 1 == len(node_list):
            node_list[0].channel = 1
            node_list[0].timeslot = 1

        """
        for each_node in node_list:
            if debug:
                print("each node", each_node.ID)
                print("each node.descendent", each_node.descIDs_prime)
            for each_id in each_node.descIDs_prime:
                print("each id in descID:", each_id)
                if debug:
                    print("node_list[%u].channel %u and time slot %u" % (each_id, node_list[each_id].channel, node_list[each_id].timeslot))
                if node_list[each_id].channel != 0 and node_list[each_id].timeslot != 0:
                    print("remove", each_id)
                    each_node.descIDs_prime.remove(each_id)
            print("each node.descendent", each_node.descIDs_prime)
        """
        #pdb.set_trace()
        for each_node_i in node_list:
            for each_node_j in scheduled_nodes:
                if each_node_j.ID in each_node_i.descIDs_prime:
                    each_node_i.descIDs_prime.remove(each_node_j.ID)
            if debug:
                print("each node i:", each_node_i.ID)
                print("each node.descendent", each_node_i.descIDs_prime)



        if debug:
            print("len(scheduled nodes):", len(scheduled_nodes))
    #print("Total working period: ", node_list[0].wp)
