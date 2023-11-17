from libs import gentopo
from libs import node
import pdb
import sys
import queue
from collections import defaultdict
import pandas as pd
import numpy as np
import copy
from copy import deepcopy

vertex_c = []
edge_c = []
INFINITY = sys.maxsize - 1


# T = 10 # L is length of time slot in a period

def distance(src, dst):
    """

    :param src:
    :param dst:
    :return:
    """
    return np.sqrt(np.square(src.x - dst.x) + np.square(src.y - dst.y))


def create_list_of_channels(r1, r2):
    return [item for item in range(r1, r2 + 1)]


def link(u, v):
    """
    Create a link consisting of two nodes as a type tuple
    """
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
    # for each_node in range(0, len(node_list)):

    blue_nodes = []
    white_nodes = []
    black_nodes, max_layer = find_mis(node_list)
    # print("black nodes", black_nodes)

    """
    for each_neighbor in node_list[0].next_layer_neighbors:
        node_list[0].childrenIDs.append(each_neighbor)
        node_list[each_neighbor].parentID = 0
    """

    q = queue.Queue()

    for i in range(1, max_layer + 1):
        for each_node in range(0, len(node_list)):
            if node_list[each_node].layer == i:
                q.put(each_node)

    while q.empty() is False:
        current = q.get()
        if current in black_nodes:
            t = 10000
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
            t = 10000
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

    # print("length of all nodes", len(blue_nodes) + len(black_nodes) + len(white_nodes))

    for each_node in node_list:
        find_descendent_nodes(node_list, each_node)

    return black_nodes, blue_nodes, white_nodes, max_layer


def find_descendent_nodes(node_list, x):
    for each_child in x.childrenIDs:
        if each_child not in x.descIDs:
            x.descIDs.append(each_child)
            if node_list[each_child].childrenIDs == []:
                continue
            else:
                dsc = find_descendent_nodes(node_list, node_list[each_child])
                for each_id in dsc:
                    if each_id not in x.descIDs:
                        x.descIDs.append(each_id)
    return x.descIDs


def find_parent_node_list(node_list, children_list):
    list_of_links = []
    for each_node in children_list:
        list_of_links.append(link(each_node, node_list[each_node].parentID))
    return list_of_links


def NDAS(node_list, T, m, comm_range, alpha):
    """
    :param node_list:
    :param T:
    :param m:
    :param comm_range:
    :param alpha:
    :return:
    """
    Sn = []
    black_nodes, blue_nodes, white_nodes, max_layer = tree_construction_based_mis(node_list)

    links_from_black_nodes = find_parent_node_list(node_list, black_nodes)
    for i in range(1, len(links_from_black_nodes)):
        Sn.append(links_from_black_nodes[i])
    links_from_blue_nodes = find_parent_node_list(node_list, blue_nodes)
    for i in links_from_blue_nodes:
        Sn.append(i)

    for i in range(0, len(node_list) - 1):
        for j in range(i + 1, len(node_list)):
            if distance(node_list[i], node_list[j]) <= comm_range * alpha:
                node_list[i].interfereIDs.append(node_list[j].ID)
                node_list[j].interfereIDs.append(node_list[i].ID)

    links_from_white_nodes = find_parent_node_list(node_list, white_nodes)
    for i in links_from_white_nodes:
        Sn.append(i)

    ts = 0
    # links_selection(node_list, links_from_white_nodes, ts, T, m)
    ts = links_selection(node_list, Sn, links_from_white_nodes, ts, T, m)
    """
    for each_node in white_nodes:
        print("timeslot of each white node: %u %u" % (each_node, node_list[each_node].timeslot))
    """
    for i in range(max_layer, 0, -1):
        blue_nodes_by_layer = []
        black_nodes_by_layer = []
        for each_node in range(0, len(node_list)):
            if node_list[each_node].layer == i:
                if each_node in blue_nodes:
                    if node_list[each_node].channel is None and node_list[each_node].timeslot is None:
                        blue_nodes_by_layer.append(each_node)
                if each_node in black_nodes:
                    if node_list[each_node].channel is None and node_list[each_node].timeslot is None:
                        black_nodes_by_layer.append(each_node)
        links_from_black_nodes_by_layer = find_parent_node_list(node_list, black_nodes_by_layer)
        links_from_blue_nodes_by_layer = find_parent_node_list(node_list, blue_nodes_by_layer)
        ts = links_selection(node_list, Sn, links_from_blue_nodes_by_layer, ts, T, m)
        ts = links_selection(node_list, Sn, links_from_black_nodes_by_layer, ts, T, m)

    for each_node in range(1, len(node_list)):
        print("channel and timeslot of each node: %u %u %u" % (
        each_node, node_list[each_node].channel, node_list[each_node].timeslot))
        # print(each_node)
        # print(node_list[each_node].timeslot)

    wp = 1000
    for i in range(1, wp):
        for each_node in range(1, len(node_list)):
            if node_list[each_node].timeslot >= T * (i - 1) and node_list[each_node].timeslot < T * i:
                if node_list[each_node].wp == 0:
                    node_list[each_node].wp = i


def links_selection(node_list, Sn, list_of_links, ts, T, m):
    """
    :param node_list:
    :param list_of_links: illustrates link(Vc, F(Vc)), F(Vc) is father of a node Vc
    :param ts: scheduling time
    :param T: number of slots in a working period
    :param m: number of channels
    :return: smallest times ts when the previous scheduling finishes
    """

    while list_of_links:
        scheduled_links = []
        Sc = []
        # Sc_copy = []
        considered_parent_nodes = []
        for i in range(0, len(list_of_links)):
            links_same_parent = []
            if list_of_links[i][1] in considered_parent_nodes:
                continue
            else:
                links_same_parent.append(list_of_links[i])
            for j in range(i + 1, len(list_of_links)):
                if list_of_links[j][1] == list_of_links[i][1]:
                    links_same_parent.append(list_of_links[j])
            selected_link = select_one_child(node_list, links_same_parent)
            Sc.append(selected_link)
            considered_parent_nodes.append(selected_link[1])

        scheduled_links = copy.deepcopy(Sc)
        # Apply algorithm 3
        ts = link_schedule(node_list, Sc, ts, T, m)
        """
        for x in range(1, T + 1):
            if (te + x) % T == 0:
                te = te + x
                break
        """
        te = (ts // T + 1) * T
        """
        #print("ts", ts)
        for each_link in list_of_links:
            if node_list[each_link[0]].timeslot != None and node_list[each_link[0]].channel != None:
                scheduled_links.append(each_link)
        """
        """
        Apply algorithm 6 to schedule schedulable links in Sn from ts to (te-1)
        """
        scheduled_links = novel_link_scheduling(node_list, scheduled_links, Sn, ts, te, T, m)

        """
        for each_link in scheduled_links:
            if each_link in list_of_links:
                list_of_links.remove(each_link)
        """

        for each_link in scheduled_links:
            if each_link in Sn:
                Sn.remove(each_link)
            if each_link in list_of_links:
                list_of_links.remove(each_link)

        ts = te

    return ts


def novel_link_scheduling(node_list, scheduled_links, Sn, ts, te, T, m):
    # scheduled_links = []
    for t in range(ts, te - 1):
        slot = t % T
        Sr = create_list_of_channels(1, m)
        for each_link in scheduled_links:
            if node_list[each_link[0]].channel in Sr and slot in node_list[each_link[1]].active_slot:
                Sr.remove(node_list[each_link[0]].channel)

        mr = len(Sr)

        if mr != 0:
            """
            Find schedulable links to add into St
            """
            St = []
            Gt = defaultdict(list)
            Gs = defaultdict(list)
            for each_edge in Sn:

                temp = 0
                if slot in node_list[each_edge[1]].active_slot and node_list[each_edge[1]].timeslot is None and \
                        check_rcv_not_yet_scheduled(node_list, each_edge[1], t) is True and node_list[each_edge[0]]. \
                        timeslot is None and check_scheduled_desc(node_list, each_edge[0]) is True and \
                        check_timeslot_scheduled_children(node_list, each_edge[0], t) is True:

                    for e in St:
                        if each_edge[1] == e[1]:
                            temp += 1
                    if temp == 0:
                        St.append(each_edge)

            Gt = find_CACG_at_t(node_list, St, slot)
            # Gt = sorted(Gt.get(), key=lambda x: x[2])

            for slot, edges in Gt.items():
                for each_edge in edges:
                    if each_edge[2] <= mr - 1:
                        Gs[slot].append(each_edge)

            """
            Adopt the first-fit coloring method h in Gs by smallest-degree-last ordering
            """
            for slot, links in Gs.items():
                """
                H: coloring method c according smallest-degree-last ordering
                Hj: color set Cj
                F: coloring method f according colo ordering in set Cj
                """

                H = defaultdict(list, {color: [] for color in range(0, mr)})
                Hj = defaultdict(list)
                for each_link_index in range(0, len(links)):
                    for color, vals in H.items():
                        if collision_in_FACG(node_list, vals, links[each_link_index]) == False:
                            vals.append(links[each_link_index])
                            break

                for color_h, edges in H.items():
                    for each_edge in edges:
                        if node_list[each_edge[0]].timeslot is None and node_list[each_edge[0]].channel is None:
                            node_list[each_edge[0]].timeslot = t
                            node_list[each_edge[0]].channel = Sr[color_h]
                            scheduled_links.append(link(each_edge[0], each_edge[1]))

    # for each_link in scheduled_links:
    # Sn.remove(each_link)

    return scheduled_links


def find_CACG_at_t(node_list, St, t):
    CACG_t = defaultdict(list)
    for each_edge in St:
        each_edge = each_edge + (INFINITY,)
        CACG_t[t].append(each_edge)

    # find degree of a link at the certain slot

    for key, value in CACG_t.items():
        for each_link in range(0, len(value)):
            degree = find_degree(node_list, value, value[each_link], key)
            if degree <= value[each_link][2]:
                temp = list(value[each_link])
                temp[2] = degree
                value[each_link] = tuple(temp)  # add degree to the link as a tuple

    # Sorting degrees of nodes in the conflict graph in ascending order
    for key, value in CACG_t.items():
        value.sort(key=lambda v: v[2])

    return CACG_t


def check_rcv_not_yet_scheduled(node_list, rcv, time_slot):
    """

    :param node_list:
    :param rcv:
    :return:
    """
    temp = 0
    for each_node in node_list[rcv].childrenIDs:
        if node_list[each_node].timeslot is not None:
            if node_list[each_node].timeslot == time_slot:
                temp = temp + 1
    if temp == 0:
        return True
    else:
        return False


def check_scheduled_desc(node_list, x):
    """
    Check all descendent nodes of a tree rooted at node x had been scheduled or not.
    :param node_list:
    :param x: Given node ID
    :param t: Node x should be scheduled after timeslot t
    :return: "True" means all descendent nodes had been scheduled,
             "False" means some of the descendent nodes has not been scheduled yet

    temp = 0
    for each_node_ID in node_list[x].descIDs:
        if node_list[each_node_ID].channel is None and node_list[each_node_ID].timeslot is None:
            temp = temp + 1
    if temp == 0:
        #return True
        for each_child in node_list[x].childrenIDs:
            if node_list[each_child].timeslot <= t:
                return False
            else:
                return True
    else:
        return False
    """
    temp = 0
    for each_node_ID in node_list[x].descIDs:
        if node_list[each_node_ID].channel is None and node_list[each_node_ID].timeslot is None:
            temp = temp + 1
    if temp == 0:
        return True
    else:
        return False


def check_timeslot_scheduled_children(node_list, x, t):
    """

    :param node_list:
    :param x:
    :param t:
    :return:
    """
    temp = 0
    for each_node_ID in node_list[x].childrenIDs:
        if node_list[each_node_ID].timeslot > t:
            temp = temp + 1
    if temp == 0:
        return True
    else:
        return False


def select_one_child(node_list, links_same_parent):
    t = 1000
    for each_link in links_same_parent:
        if each_link[0] <= t:
            t = each_link[0]
            selected_link = each_link
    return selected_link


def link_schedule(node_list, candidate_links, ts, T, m):
    # Ch = create_list_of_channels(1, m)  # Sch is the set of given channels

    CACG = find_CACG(node_list, candidate_links, T)

    FACG = defaultdict(list)
    temp_dict = defaultdict(list)
    for i in range(0, T):
        # temp_dict = defaultdict(list)

        for key, value in temp_dict.items():
            if key < i:
                temp_dict[key].clear()

        while len(CACG[i]):
            # for key, value in CACG.items():
            # if i == key:
            # for each_link_i in CACG[i]:
            temp_slot = i
            temp_link = CACG[i][0]
            temp_dict[temp_slot].append(temp_link)
            for j in range(i + 1, T):
                for each_link_j in CACG[j]:
                    # if each_link_j[0] == temp_link[0] and each_link_j[1] == temp_link[1]:
                    # temp_dict[j].append(each_link_j)
                    if each_link_j[0] == temp_link[0] and each_link_j[1] == temp_link[1] and each_link_j[2] >= \
                            temp_link[2]:
                        # lst = list(CACG[j][each_element_in_j])
                        CACG[j].remove(each_link_j)
                        # lst = (INFINITY,INFINITY,INFINITY)
                        # CACG[j].append(lst)
                    if each_link_j[0] == temp_link[0] and each_link_j[1] == temp_link[1] and each_link_j[2] < \
                            temp_link[2]:
                        temp_dict[temp_slot].remove(temp_link)
                        temp_slot = j
                        temp_link = each_link_j
                        temp_dict[j].append(each_link_j)

            if temp_link not in FACG[temp_slot]:
                FACG[temp_slot].append(temp_link)
            # break
            for t in temp_dict:
                # for key, value in temp_dict.items():
                for each_element_in_t in temp_dict[t]:
                    if link(each_element_in_t[0], each_element_in_t[1]) in candidate_links:
                        candidate_links.remove(link(each_element_in_t[0], each_element_in_t[1]))
                # if link(value[0], value[1]) in candidate_links:
                # candidate_links.remove(link(value[0], value[1]))
            CACG = find_CACG(node_list, candidate_links, T)
            """
            Update degrees of links in CACG which the link was chosen at a certain slot
            """
            for k1, v1 in CACG.items():
                for k2, v2 in temp_dict.items():
                    if k1 == k2:

                        for index in range(0, len(v1)):
                            degree = update_degree(node_list, v2, v1[index], k2)
                            t = list(v1[index])
                            t[2] = t[2] + degree
                            v1.remove(v1[index])
                            v1.insert(index, tuple(t))

    FACG = sort_by_slot(FACG)

    current_ts = 0
    for slot, links in FACG.items():
        """
        C: coloring method c according smallest-degree-last ordering
        Cj: color set Cj
        F: coloring method f according colo ordering in set Cj
        """

        C = defaultdict(list, {k: [] for k in range(0, 10)})
        Cj = defaultdict(list)
        F = defaultdict(list)
        I = []
        # C[0].append(links[0])
        for each_link_index in range(0, len(links)):

            for k, v in C.items():
                #if collision_in_FACG(node_list, v, links[each_link_index]) == False:
                v.append(links[each_link_index])
                break

        """
        Add value j into 3th element of a link to be as channel of a transmitter node 
        """
        for color_c, edges in C.items():
            for each_edge in edges:
                j = (color_c % m) + 1
                t = list(each_edge)
                t.append(j)
                Cj[color_c].append(tuple(t))

        for color_c, edges in Cj.items():
            for ind in range(0, len(edges)):
                F[color_c].append(edges[ind])

        for color_f, edges in F.items():
            for each_edge in edges:
                if node_list[each_edge[0]].timeslot is None and node_list[each_edge[0]].channel is None:
                    node_list[each_edge[0]].timeslot = ts + color_f * T + slot
                    node_list[each_edge[0]].channel = each_edge[3]

        for each_link in links:
            if node_list[each_link[0]].timeslot > current_ts:
                current_ts = node_list[each_link[0]].timeslot

        if ts > current_ts:
            current_ts = ts

    return current_ts


def find_CACG(node_list, candidate_links, T):
    CACG = defaultdict(list)
    for each_slot in range(0, T):
        for item in candidate_links:
            for each_active_slot in node_list[item[1]].active_slot:
                if each_active_slot == each_slot:
                    item = item + (INFINITY,)
                    CACG[each_slot].append(item)

        # find degree of a link at a certain slot, then delete links having higher degrees which are active at different slots

        for key, value in CACG.items():
            if key == each_slot:
                for each_link in range(0, len(value)):
                    degree = find_degree(node_list, value, value[each_link], each_slot)
                    if degree <= value[each_link][2]:
                        temp = list(value[each_link])
                        temp[2] = degree
                        value[each_link] = tuple(temp)  # add degree to the link as a tuple
    return CACG


def find_degree(node_list, candidate_links, considering_link, time_slot):
    degree = -1
    for each_link in candidate_links:
        for each_active_slot in node_list[each_link[1]].active_slot:
            if each_active_slot == time_slot:
                if considering_link[0] in node_list[each_link[1]].neighborIDs or considering_link[1] in node_list[
                    each_link[0]].neighborIDs:
                    # if considering_link[0] in node_list[each_link[1]].interfereIDs or considering_link[1] in node_list[each_link[0]].interfereIDs:
                    degree += 1
    return degree


def collision_in_FACG(node_list, candidate_links, considering_link):
    """
    Check collision between links in FACG in a specific slot
    :param node_list:
    :param candidate_links:
    :param considering_link:
    :return:
    """
    degree = -1
    for each_link in candidate_links:
        if considering_link[0] in node_list[each_link[1]].neighborIDs or considering_link[1] in node_list[
            each_link[0]].neighborIDs:
            # if considering_link[0] in node_list[each_link[1]].interfereIDs or considering_link[1] in node_list[each_link[0]].interfereIDs:
            degree += 1
    if degree == -1:
        return False
    else:
        return True


def update_degree(node_list, candidate_links, considering_link, time_slot):
    degree = 0
    for each_link in candidate_links:
        for each_active_slot in node_list[each_link[1]].active_slot:
            if each_active_slot == time_slot:
                # if considering_link[0] in node_list[each_link[1]].interfereIDs or considering_link[1] in node_list[each_link[0]].interfereIDs:
                if considering_link[0] in node_list[each_link[1]].neighborIDs or considering_link[1] in node_list[
                    each_link[0]].neighborIDs:
                    degree += 1
    return degree


def check_conflict_links(node_list, candidate_links, considering_link, time_slot):
    I = []
    for each_link in candidate_links:
        if node_list[each_link[1]].active_slot == time_slot:
            if considering_link[0] in node_list[each_link[1]].neighborIDs:
                # if considering_link[0] in node_list[each_link[1]].interfereIDs:
                # candidate_links.remove(each_link)
                if node_list[each_link[1]].channel != None and node_list[each_link[1]].channel not in I:
                    I.append(node_list[each_link[1]].channel)
            if considering_link[1] in node_list[each_link[0]].neighborIDs:
                # if considering_link[1] in node_list[each_link[0]].interfereIDs:
                # candidate_links.remove(each_link)
                if node_list[each_link[0]].channel != None and node_list[each_link[0]].channel not in I:
                    I.append(node_list[each_link[0]].channel)
    return I


def getkey(item):
    return item[2]


def sort_by_slot(dictnary):
    dictnary = sorted(dictnary.items(), key=lambda i: i[0])
    new_defaultdict = dict()
    for item in dictnary:
        item[1].sort(key=lambda x: x[2], reverse=True)
        # sorted(item[1], key=lambda x: (x[0], x[1], -x[2]))
        new_defaultdict[item[0]] = item[1]
    return new_defaultdict



