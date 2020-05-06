

# Number of frequencies used
K = 3

def create_List(r1, r2):
    return [item for item in range(r1, r2+1)]

freq_list = create_List(1,K) # freq_list is the set of given frequencies can be used

def freq_assignment(node_list, debug = False):
    dim_range = 200
    alpha = 50
    dim = int(dim_range/alpha)
    list_cell = []
    num_nodes = 200

    for i in range(0, dim*dim):
        #print("i = ", i)
        x_start = (i % dim)*alpha
        #print("x_start", x_start)
        y_start = (int(i/dim))*alpha
        #print("y_start", y_start)

        cell = []
        for each_node in node_list:
            if x_start != 3*alpha and y_start != 3*alpha:
                if x_start <= each_node.x < x_start + alpha:
                    if y_start <= each_node.y < y_start + alpha:
                        if debug:
                            print("each node: ", each_node.ID)
                            print("%u has dimension x: %u" % (each_node.ID, each_node.x))
                            print("%u has dimension y: %u" % (each_node.ID, each_node.y))
                        cell.append(each_node.ID)
            if x_start == 3*alpha and y_start != 3*alpha:
                if x_start <= each_node.x <= x_start + alpha:
                    if y_start <= each_node.y < y_start + alpha:
                        if debug:
                            print("each node: ", each_node.ID)
                            print("%u has dimension x: %u" % (each_node.ID, each_node.x))
                            print("%u has dimension y: %u" % (each_node.ID, each_node.y))
                        cell.append(each_node.ID)
            if y_start == 3*alpha and x_start != 3*alpha:
                if x_start <= each_node.x < x_start + alpha:
                    if y_start <= each_node.y <= y_start + alpha:
                        if debug:
                            print("each node: ", each_node.ID)
                            print("%u has dimension x: %u" % (each_node.ID, each_node.x))
                            print("%u has dimension y: %u" % (each_node.ID, each_node.y))
                        cell.append(each_node.ID)
            if x_start == 3*alpha and y_start == 3*alpha:
                if x_start <= each_node.x <= x_start + alpha:
                    if y_start <= each_node.y <= y_start + alpha:
                        if debug:
                            print("each node: ", each_node.ID)
                            print("%u has dimension x: %u" % (each_node.ID, each_node.x))
                            print("%u has dimension y: %u" % (each_node.ID, each_node.y))
                        cell.append(each_node.ID)
        list_cell.append(cell)
    count = 0
    for each_cell in list_cell:
        #print("list of nodes in cell: ", list_cell[])
        if debug:
            print("list of nodes in cell: ", each_cell)
            print("length of number of nodes in this cell: ", len(each_cell))
            print("------------------------------------------------------------------")
        count = count + len(each_cell)
    if debug:
        print("count", count)
    if count != num_nodes:
        if debug:
            print("The total nodes in all cells is not equal to number of nodes")

    load_of_freq = []
    for each_freq in freq_list:
        load_of_freq[each_freq].append()

    for each_cell in list_cell:
        receiver_list = []
        for each_id in each_cell:
            if node_list[each_id].childrenIDs != []:
                receiver_list.append(each_id)

        arranged_receiver_list = []
        temp = 0
        max_in_degrees = 0
        while len(arranged_receiver_list) != len(receiver_list):
            for each_id in receiver_list:
                if len(node_list[each_id].childrenIDs) > max_in_degrees:
                    max_in_degrees = len(node_list[each_id].childrenIDs)
                    temp = each_id

            arranged_receiver_list.append(temp)

        load_of_freq = []
        for each_id in arranged_receiver_list:

            node_list[each_id].rx_channel = min(freq_list)

