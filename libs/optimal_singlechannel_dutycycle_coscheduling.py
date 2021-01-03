from libs import gentopo
from libs import node
import pdb
import sys
import queue
from collections import defaultdict
import pandas as pd
from copy import deepcopy

vertex_c = []
edge_c = []
INFINITY = sys.maxsize - 1


# T = 10 # L is length of time slot in a period


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
    #print("black nodes", black_nodes)

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

    print("length of all nodes", len(blue_nodes) + len(black_nodes) + len(white_nodes))
    #print("blue nodes", blue_nodes)

    return black_nodes, blue_nodes, white_nodes, max_layer


def find_parent_node_list(node_list, children_list):
    list_of_links = []
    for each_node in children_list:
        list_of_links.append(link(each_node, node_list[each_node].parentID))
    return list_of_links


def EDAS(node_list, T=10, m= 2):
    black_nodes, blue_nodes, white_nodes, max_layer = tree_construction_based_mis(node_list)
    print("white nodes: ", white_nodes )
    #links_from_black_nodes = find_parent_node_list(node_list, black_nodes)
    #links_from_blue_nodes = find_parent_node_list(node_list, blue_nodes)
    links_from_white_nodes = find_parent_node_list(node_list, white_nodes)
    ts = 0
    #links_selection(node_list, links_from_white_nodes, ts, T, m)
    ts = links_selection(node_list, links_from_white_nodes, ts, T, m)
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
                    blue_nodes_by_layer.append(each_node)
                if each_node in black_nodes:
                    black_nodes_by_layer.append(each_node)
        links_from_black_nodes_by_layer = find_parent_node_list(node_list, black_nodes_by_layer)
        links_from_blue_nodes_by_layer = find_parent_node_list(node_list, blue_nodes_by_layer)
        ts = links_selection(node_list, links_from_blue_nodes_by_layer, ts, T, m)
        ts = links_selection(node_list, links_from_black_nodes_by_layer, ts, T, m)
        """
        if len(links_from_blue_nodes_by_layer):
            ts_update = 0
            for each_link in links_from_blue_nodes_by_layer:
                for each_child in node_list[each_link[0]].childrenIDs:
                    if node_list[each_child].timeslot > ts_update:
                        ts_update = node_list[each_child].timeslot
            for x in range(1, T+1):
                if (ts_update+x) % T == 0:
                    ts_update = ts_update + x
                    break
            links_selection(node_list, links_from_blue_nodes_by_layer, ts_update, T, m)
        """

    for each_node in range(1, len(node_list)):
        print("timeslot of each node: %u %u" % (each_node, node_list[each_node].timeslot))
            #print(each_node)
            #print(node_list[each_node].timeslot)


def links_selection(node_list, list_of_links, ts, T, m):
    scheduled_nodes = []
    while list_of_links:
        Sc = []
        considered_parent_nodes = []
        for i in range(0, len(list_of_links)):
            links_same_parent = []
            if list_of_links[i][1] in considered_parent_nodes:
                continue
            else:
                links_same_parent.append(list_of_links[i])
            for j in range(i+1, len(list_of_links)):
                if list_of_links[j][1] == list_of_links[i][1]:
                    links_same_parent.append(list_of_links[j])
            selected_link = select_one_child(node_list, links_same_parent)
            #if selected_link not in Sc:
            Sc.append(selected_link)
            considered_parent_nodes.append(selected_link[1])
        # Apply algorithm 3
        link_schedule(node_list, Sc, ts, T, m)
        ts = ts + T

        #print("ts", ts)
        for each_link in list_of_links:
            if node_list[each_link[0]].timeslot != None:
                scheduled_nodes.append(each_link)

        for each_link in scheduled_nodes:
            if each_link in list_of_links:
                list_of_links.remove(each_link)

    return ts

def select_one_child(node_list, links_same_parent):
    t = 1000
    for each_link in links_same_parent:
        if each_link[0] <= t:
            t = each_link[0]
            selected_link = each_link
    return selected_link


def link_schedule(node_list, candidate_links, ts, T, m):
    Sch = create_list_of_channels(1, m)  # Sch is the set of given channels

    CACG = find_CACG(node_list, candidate_links, T)

    FACG = defaultdict(list)
    temp_dict = defaultdict(list)
    for i in range(0, T):
        #temp_dict = defaultdict(list)
        for key, value in temp_dict.items():
            if key < i:
                    temp_dict[key].clear()
        while len(CACG[i]):
            # for key, value in CACG.items():
            # if i == key:
            #for each_link_i in CACG[i]:
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
                            temp_link[
                                2]:
                        temp_dict[temp_slot].remove(temp_link)
                        temp_slot = j
                        temp_link = each_link_j
                        temp_dict[j].append(each_link_j)
                """
                for ind in range(0, len(CACG[j])):
                    temp = list(CACG[j][ind])
                    temp[2] = find_degree(node_list, CACG[j], temp, j)
                    CACG[j].remove(CACG[j][ind])
                    # CACG[j].append(tuple(temp))
                    CACG[j].insert(ind, tuple(temp))
                """
                """
                for each_link in CACG[j]:
                    temp = list(each_link)
                    temp[2] = find_degree(node_list, CACG[j], each_link, j)
                    CACG[j].remove(each_link)
                    CACG[j].append(tuple(temp))
                """
            if temp_link not in FACG[temp_slot]:
                FACG[temp_slot].append(temp_link)
            # break
            for t in temp_dict:
            #for key, value in temp_dict.items():
                for each_element_in_t in temp_dict[t]:
                    if link(each_element_in_t[0], each_element_in_t[1]) in candidate_links:
                        candidate_links.remove(link(each_element_in_t[0], each_element_in_t[1]))
                #if link(value[0], value[1]) in candidate_links:
                    #candidate_links.remove(link(value[0], value[1]))
            CACG = find_CACG(node_list, candidate_links, T)
            """
            Update degrees of links in CACG which the link was chosen at a certain slot
            """
            for k1, v1 in CACG.items():
                for k2, v2 in temp_dict.items():
                    if k1 == k2:
                        lst = []
                        #lst.append(v2)
                        for index in range(0, len(v1)):
                            degree = update_degree(node_list, v2, v1[index], k2)
                            t = list(v1[index])
                            t[2] = t[2] + degree
                            v1.remove(v1[index])
                            v1.insert(index, tuple(t))

    FACG = sort_by_slot(FACG)
    """
    Update degree of link in FACG
    
    for key, value in FACG.items():
        for each_link in range(0, len(value)):
            degree = find_degree(node_list, value, value[each_link], key)
            temp = list(value[each_link])
            temp[2] = degree
            value[each_link] = tuple(temp)
    """

    """
    In single channel multi-active slots, if two nodes in the FACG are conflict, they must be assigned in different timeslot
    
    for key, value in FACG.items():
        degree = 1
        t = tuple()
        for each_link in value:
            if each_link[2] >= degree:
                return each_link
        candidate_links.append(link(each_link[0], each_link[1]))
    """
    for key, value in FACG.items():
        degree = 1
        t = tuple()
        for each_link_index in range(0, len(value)):
            # for i in range(0, len(links_from_black_nodes_by_layer)):
            """
            if node_list[value[each_link][0]].childrenIDs:
                ts_update = 0
                for each_child in node_list[value[each_link][0]].childrenIDs:
                    if node_list[each_child].timeslot > ts_update:
                        ts_update = node_list[each_child].timeslot

                for x in range(1, T + 1):
                    if (ts_update + x) % T == 0:
                        ts = ts_update + x
                        break

            parent_node = node_list[value[each_link][0]].parentID
            # ts_update = 0
            lst_of_chi_ts = []
            for each_node in node_list[parent_node].childrenIDs:
                if node_list[each_node].timeslot is not None:
                    lst_of_chi_ts.append(node_list[each_node].timeslot)

            if node_list[value[each_link][0]].timeslot is None:
                node_list[value[each_link][0]].timeslot = ts + key

            if node_list[value[each_link][0]].timeslot in lst_of_chi_ts:
                node_list[value[each_link][0]].timeslot = max(lst_of_chi_ts) + T
            """

            if node_list[value[each_link_index][0]].timeslot is None:
                node_list[value[each_link_index][0]].timeslot = ts + key
            """
            for each_link in value:
                if each_link[2] >= degree:
                    degree = each_link[2]
                    t = each_link
        node_list[t[0]].timeslot = ts + T + key
            """

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
                if considering_link[0] in node_list[each_link[1]].neighborIDs or considering_link[1] in node_list[each_link[0]].neighborIDs:
                    degree += 1
    return degree

def update_degree(node_list, candidate_links, considering_link, time_slot):
    degree = 0
    for each_link in candidate_links:
        for each_active_slot in node_list[each_link[1]].active_slot:
            if each_active_slot == time_slot:
                if considering_link[0] in node_list[each_link[1]].neighborIDs or considering_link[1] in node_list[
                    each_link[0]].neighborIDs:
                    degree += 1
    return degree

def check_conflict_links(node_list, candidate_links, considering_link, time_slot):
    I = []
    for each_link in candidate_links:
        if node_list[each_link[1]].active_slot == time_slot:
            if considering_link[0] in node_list[each_link[1]].neighborIDs:
                # candidate_links.remove(each_link)
                if node_list[each_link[1]].channel != None and node_list[each_link[1]].channel not in I:
                    I.append(node_list[each_link[1]].channel)
            if considering_link[1] in node_list[each_link[0]].neighborIDs:
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
        #sorted(item[1], key=lambda x: (x[0], x[1], -x[2]))
        new_defaultdict[item[0]] = item[1]
    return new_defaultdict
