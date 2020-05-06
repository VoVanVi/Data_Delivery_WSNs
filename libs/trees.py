import sys
import queue
import pdb
INFINITY = sys.maxsize - 1

def find_descendent_nodes(node_list, x):
    for each_child in x.childrenIDs:
        if each_child not in x.descIDs_prime:
            x.descIDs_prime.append(each_child)
            if node_list[each_child].childrenIDs == []:
                continue
            else:
                dsc = find_descendent_nodes(node_list, node_list[each_child])
                for each_id in dsc:
                    if each_id not in x.descIDs_prime:
                        x.descIDs_prime.append(each_id)
    return x.descIDs_prime

def find_ancestor_nodes(node_list, x):
    ancestor = 0
    if x.ID == 0:
        x.ancestorIDs = []
    else:
        x.ancestorIDs.append(x.parentID)
        up = x.parentID
        while up != ancestor:
            up = node_list[up].parentID
            x.ancestorIDs.append(up)

def build_bfs(node_list):
    # Build a Breadth First Search Tree, equivalent to an SPT in case all edge costs are 1
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


    for each_node in node_list:
        find_descendent_nodes(node_list, each_node)
        find_ancestor_nodes(node_list, each_node)

    return True


def build_dfs(node_list):
    """
    https://en.wikipedia.org/wiki/Depth-first_search
    :param node_list:
    :return:
    """
    S = []
    S.append(0)
    while len(S) > 0:
        v = S[-1]
        S.remove(v)
        if node_list[v].discovered is False:
            node_list[v].discovered = True
            for u in node_list[v].neighbors:
                if u not in S and node_list[u].discovered is False:
                    node_list[u].parentID = v
                    node_list[v].childrenIDs.append(u)
                    S.append(u)


def bspt_sm1(node_list):
    """
    to build the tree:
    Wireless Netw. '11, "Aggregation convergecast scheduling in wireless sensor networks"

    Using semi-matching 2 algorithm, A. Harvey Lecture
    :param node_list:
    :return:
    """
    # first reset the tree built, if any
    #delete_tree(node_list)
    # then do the scheduling

    """
    Step 1: Initialize a semi-matching
    Algorithm:
    - Sort vertices in next-level nodes by increasing degree to the previous-level nodes
    - Match each u in the next-level nodes with its least-loaded node v in the previous-level nodes. In case of a tie,
    choose v with least degree
    """

    # update the 'degree' of each node in terms of 'to-prev-level' and 'to-next-level':
    node_list, max_layer = layering(node_list)
    for u in node_list:
        u.marked = -1
    P = []
    E = []
    P.append(0)

    while len(P) > 0:
        C = []
        for m in P:
            node_list[m].marked = 1
        for m1 in P:
            for n in node_list[m1].neighborIDs:
                if node_list[n].marked == -1:
                    C.append(n)
                    node_list[
                        n].marked = 1  # to avoid the case that a node is a common neighbor of two nodes in P => duplicatedly added to C
        # ==> P is the previous level nodes
        # ==> C is the current level nodes
        find_matching_bspt(node_list, P, C)
        P = C

    for each_node in node_list:
        find_descendent_nodes(node_list, each_node)
        find_ancestor_nodes(node_list, each_node)


def find_matching_bspt(node_list, P, C):
    """
    implementation from pseudocode SM1 in https://pdfs.semanticscholar.org/76af/c6c5bcf40aaee624f45d238572d36625b4c3.pdf
    Semi-Matchings for Bipartite Graphs and Load Balancing- Harvey et al.

    :param P:
    :param C:
    :return:
    """
    M = []
    # print "\t\t\t\t\tP=", P
    # print "\t\t\t\t\tC=", C
    for r in C:
        Q = queue.Queue()
        Q.put(r)
        S = []
        S.append(r)

        bestV = -1
        for i in P:
            node_list[i].matchingParent = []
        for i in C:
            node_list[i].matchingParent = []
        while not Q.empty():
            w = Q.get()
            if w in C:
                nC = [x for x in node_list[w].neighborIDs if x in P]  # neighboring nodes from the previous neighbors
                N = [x for x in nC if (w, x) not in M and (x, w) not in M]
            else:
                nP = [x for x in node_list[w].neighborIDs if x in C]  # neighboring nodes from the previous neighbors
                N = [x for x in nP if (x, w) in M or (w, x) in M]
                if bestV == -1 or deg_in_matching_bspt(M, w) < deg_in_matching_bspt(M, bestV):
                    bestV = w
            for n in N:
                if n not in S:
                    node_list[n].matchingParent.append(w)

                    Q.put(n)
                    S.append(n)
        v = bestV
        if v > -1:
            u = node_list[v].matchingParent[-1]
            node_list[v].matchingParent.remove(u)
            M.append((u, v))
            node_list[u].matched = 1
            node_list[v].matched = 1
            while u != r:
                v = node_list[u].matchingParent[-1]
                node_list[u].matchingParent.remove(v)
                if (u, v) in M:
                    M.remove((u, v))
                else:
                    M.remove((v, u))

                u = node_list[v].matchingParent[-1]
                node_list[v].matchingParent.remove(u)

                M.append((u, v))
    for (u, v) in M:
        if u in C:
            node_list[u].parentID = v
            node_list[v].childrenIDs.append(u)
        else:
            node_list[v].parentID = u
            node_list[u].childrenIDs.append(v)
    # print "Final M:", M
    return M


def deg_in_matching_bspt(M, w):
    """
    Return the degree of node w in the matching M
    :param M:
    :param w:
    :return:
    """
    matchedNodes = []
    for (u, v) in M:
        if u == w:
            if v not in matchedNodes:
                matchedNodes.append(v)
        elif v == w:
            if u not in matchedNodes:
                matchedNodes.append(u)

    return len(matchedNodes)


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


def mlst(node_list):
    """
    to build the Minimum Lower bound Spanning Tree (MLST)
    Wireless Netw.'16, A time-efficient aggregation convergecast scheduling algorithm for wireless sensor networks
    :param node_list:
    :return:
    """
    N = len(node_list)
    M = N * 3
    if N == 0 or N == 1:
        print("Simple graph with 0 or 1 node!!!")
        return
    added = [0]
    node_list[0].hopCount = 0
    node_list[0].added = 1
    for u in range(0, len(node_list)):
        node_list[u].nnbrs = len(node_list[u].neighbors)
    not_added = [x for x in range(1, N)]
    while len(not_added) > 0:
        mincost = INFINITY
        tobe_added = -1
        prnt = -1
        for i in added:
            for j in node_list[i].neighbors:
                if node_list[j].added == 0:
                    cij = M * M * (len(node_list[i].childrenIDs) + node_list[i].hopCount) + M * node_list[i].nnbrs + node_list[j].nnbrs
                    if cij < mincost:
                        mincost = cij
                        tobe_added = j
                        prnt = i
        if tobe_added != -1:
            added.append(tobe_added)
            not_added.remove(tobe_added)
            node_list[prnt].childrenIDs.append(tobe_added)
            node_list[tobe_added].parentID = prnt
            node_list[tobe_added].hopCount = node_list[prnt].hopCount + 1
            node_list[tobe_added].added = 1
        else:
            print("No node to add", not_added)
            return False
    return True, False

