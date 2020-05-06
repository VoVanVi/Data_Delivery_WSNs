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
    num_nodes = np.arange(30, 35, 5)
        #T = [5, 10, 20, 100]

    for index in range(0, 10):
        for n in num_nodes:
            valid = False
            j = 0
            while not valid:
                j += 1
                comm_range = 8
                #N = int(n * np.square(t) / np.pi) + 1
                x_range = 20
                y_range = 20
                print("Loop", index)
                node_list = gentopo.random_rect(num_node=n,
                                                   x_range=x_range,
                                                   y_range=y_range,
                                                   comm_range=comm_range)
                print(len(node_list))
                if gentopo.build_bfs(node_list):
                    topoFile = open('..\\topos\\sinkrandom\\tp_%d_%d_%d_sinkcorner.txt' % (n, comm_range, index), 'w')
                    #topoFile.write("N %d T %d\n" % (n, t))
                    topoFile.write("N %d \n" % n)
                    for i in range(0, n):
                            # write to file: [node1_ID , node2_ID, link quality, node1.x, node1.y, node2.x, node2.y]
                        topoFile.write("%u %u %u\n" % (node_list[i].ID, node_list[i].x, node_list[i].y))
                    valid = True