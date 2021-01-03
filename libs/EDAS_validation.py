from libs import multichannel_CoScheduling
from libs import bnj_MultiChannel_CoScheduling


def schedule_validation(node_list):
    """
    check out the constructed schedule:
    1. Check if it's a tree
    - Go from any node upwards, through the ancestors, it must reach the sink
    2. check the schedule:
    - All children of a node must have different working period (tx_wp)
    - (working period, active time slot) of the children must be smaller than the parent's
     - no collision in same (working period, active time slot)
    :return:
    """
    for u in range(1, len(node_list)):
        parent = node_list[u].parentID
        count = 1
        while parent != 0:
            parent = node_list[parent].parentID
            count += 1
            if count > len(node_list):
                print("This is not a valid tree")
                break
    """
    The parent node should be assigned larger channel than children nodes
    """

    for u in range(1, len(node_list)):
        for v in node_list[u].childrenIDs:
            if node_list[v].wp > node_list[u].wp:
                print("working period of child", v, "is larger than working period of it's parent:", u)
            if node_list[v].wp == node_list[u].wp and node_list[v].channel > node_list[u].channel:
                print("Channel of a child:", v, "is larger than channel of the parent:", node_list[u].ID)
            if node_list[v].wp == node_list[u].wp and node_list[v].channel == node_list[u].channel and node_list[v].timeslot > node_list[u].timeslot:
                print("The child node ", v , "and its parent node", node_list[u].ID, "have the same channel, but the child node has higher time slot")

    for u in node_list:
        if u.childrenIDs != []:
            if u.channel == 0:
                print("The node", u.ID, "does not allocate any channel")
    """
    To check if subtrees, having larger nodes than number of timeslot (L), should be allocated in different working period
    """

    t = 0
    for u in node_list:
        leng_children = len(u.childrenIDs)
        #if len(u.childrenIDs) > multichannel_CoScheduling.L:
        if len(u.childrenIDs) > bnj_MultiChannel_CoScheduling.L:
            for each_id_i in u.childrenIDs:
                for each_id_j in u.childrenIDs:
                    if each_id_i != each_id_j and node_list[each_id_i].wp == node_list[each_id_j].wp and node_list[each_id_i].channel == node_list[each_id_j].channel and node_list[each_id_i].timeslot == node_list[each_id_j].timeslot:
                        print("Node", node_list[each_id_i].ID, "and node", node_list[each_id_j].ID ,"are same working period, channel and TS in a subtree")

    """
    #To check the secondary collision while scheduling
    """
    for u in range(1, len(node_list)):
        for v in range(u+1, len(node_list)):
            if u in node_list[node_list[v].parentID].neighborIDs and v in node_list[node_list[u].parentID].neighborIDs:
                if node_list[u].wp == node_list[v].wp and node_list[u].channel == node_list[v].channel and node_list[u].timeslot == node_list[v].timeslot:
                    print("Secondary collision happens: Node", u, "and node", v, "are scheduled in the same wp, channel and timeslot" )

    """
    #To check the primary collision while scheduling
    """
    for u in range(1, len(node_list)):
        for v in range(u+1, len(node_list)):
            if node_list[u].parentID == node_list[v].parentID:
                if node_list[u].wp == node_list[v].wp and node_list[u].channel == node_list[v].channel and node_list[u].timeslot == node_list[v].timeslot:
                    print("Primary collision happens: Node", u, "and node", v, "are schedule in the same wp, channel and time slot")

    # collision check
    #for u in range(1, len(node_list)-1):
        #for v in range(u+1, len(node_list)):
            #if node_list[u].channel == node_list[v].channel and node_list[u].timeslot == node_list[v].timeslot:
                    #print("Collisions detected!!!, between nodes ", u, v)
