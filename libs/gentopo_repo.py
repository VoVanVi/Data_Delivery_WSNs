#from . import gentopo
#import gentopo
from libs import gentopo
import numpy as np
import pdb

if __name__=="__main__":

    # scheme = "duty_cycle_varies"
    #scheme = "num_nodes_varies"
    #if scheme == "duty_cycle_varies":
    #num_nodes = [100, 600, 1000]
        #T = [2, 3, 4, 5, 8, 10, 15, 20, 30, 50, 80, 100]
    #else:
    num_nodes = np.arange(100, 105, 5)
    T = [10]

    for index in range(0, 100):
        for n in num_nodes:
            for t in T:
                valid = False
                j = 0
                while not valid:
                    j += 1
                    comm_range = 30
                    #N = int(n * np.square(t) / np.pi) + 1
                    x_range = 200
                    y_range = 200
                    print("Loop", index)
                    node_list = gentopo.random_rect(num_node=n,
                                                   x_range=x_range,
                                                   y_range=y_range,
                                                   comm_range=comm_range,
                                                    time_slot=10,
                                                    active_slot_no=2)
                    if gentopo.build_bfs(node_list):
                        """
                        topoFile = open('..\\topos\\sink_center\\tp_%d_%d_%d_sinkcenter.txt' % (n, comm_range, index), 'w')
                        #topoFile.write("N %d T %d\n" % (n, t))
                        topoFile.write("N %d \n" % n)
                        for i in range(0, n):
                            topoFile.write("%u %u %u %u\n" % (node_list[i].ID, node_list[i].x, node_list[i].y, node_list[i].active_slot))
                        """
                        #Gen topos for multiple times duty cycle nodes in a network
                        topoFile = open('..\\topos\\sink_center\\tp_%d_%d_%d_sinkcenter.txt' % (n, comm_range, index), 'w')
                        #topoFile.write("N %d T %d\n" % (n, t))
                        topoFile.write("N %d \n" % n)
                        for i in range(0, n):
                                # write to file: [node1_ID , node2_ID, link quality, node1.x, node1.y, node2.x, node2.y]
                            topoFile.write("%u %u %u " % (node_list[i].ID, node_list[i].x, node_list[i].y))
                            for item in node_list[i].active_slot:
                                topoFile.write("%s " % item)
                            topoFile.write("\n")
                        valid = True