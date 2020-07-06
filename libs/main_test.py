#from libs import dsa_scheduling
from libs import gentopo
#from libs import pipeline_scheduling
#from libs import dtc_fas
from libs import validation
from libs import draw
import queue
from libs import trees
from libs import multichannel_CoScheduling
from libs import LDFmultichannelscheduling
from libs import limitedFreqScheduling
from libs import bnj_MultiChannel_CoScheduling
from libs import multichannel_dutycycle_coscheduling
import pdb

if __name__ == "__main__":
    #N = 30
    N = 100
    #x_range = 20
    x_range = 200
    #y_range = 20
    y_range = 200
    #comm_range = 15
    comm_range = 30
    total_channel_list = []
    wp_list = []
    scheduling_scheme = 3
    #for i in range(0, 100):
    i = 1
    if i == 1:
        print("------------------------------------------------")
        print("Topo: ", i)
        #topofile = open('..\\topos\\sinkrandom\\tp_%u_%u_%u_sinkcorner.txt' % (N, comm_range, i))
        topofile = open('..\\topos\\sink_center\\tp_%u_%u_%u_sinkcenter.txt' % (N, comm_range, i))
        node_list = gentopo.read_from_topo_repo(topofile, comm_range)
        #print("I'm here")
        #trees.bspt_sm1(node_list)
        #trees.build_bfs(node_list)
        #trees.dijkstra_duty_cycle_1slot(node_list, 10)
        #draw.draw(node_list)

        #limitedFreqScheduling.freq_assignment(node_list)

        if scheduling_scheme == 0:
            """
            Multi-channel co-scheduling
`           """
            # trees.build_bfs(node_list)
            # trees.dijkstra_duty_cycle_1slot(node_list, 10)
            draw.draw(node_list)

            multichannel_CoScheduling.constraint_graph_construction(node_list, False)
            multichannel_CoScheduling.coscheduling(node_list, False)

            validation.schedule_validation(node_list)
            channel_list_each_topo = []

            wp_list.append(node_list[0].wp)
            for u in node_list:
                channel_list_each_topo.append(u.channel)
            print("Maximum channel has been used in topo %u: %u " % (i, max(channel_list_each_topo)))

            node_list.clear()
            multichannel_CoScheduling.edge_c.clear()
            multichannel_CoScheduling.vertex_c.clear()
            # multichannel_CoScheduling.I.clear()
            # multichannel_CoScheduling.I_prime.clear()

            total_channel_list.append(max(channel_list_each_topo))

        if scheduling_scheme == 1:
            """
            BnJ Multi-channel co-scheduling
            """
            # trees.build_bfs(node_list)
            # trees.dijkstra_duty_cycle_1slot(node_list, 10)
            draw.draw(node_list)

            bnj_MultiChannel_CoScheduling.constraint_graph_construction(node_list, False)
            bnj_MultiChannel_CoScheduling.coscheduling(node_list, False)

            validation.schedule_validation(node_list)
            channel_list_each_topo = []

            wp_list.append(node_list[0].wp)
            for u in node_list:
                channel_list_each_topo.append(u.channel)
            print("Maximum channel has been used in topo %u: %u " % (i, max(channel_list_each_topo)))

            node_list.clear()
            bnj_MultiChannel_CoScheduling.edge_c.clear()
            bnj_MultiChannel_CoScheduling.vertex_c.clear()

            total_channel_list.append(max(channel_list_each_topo))

        if scheduling_scheme == 2:
            """
            LDF multischeduling 

            #LDFmultichannelscheduling.constraint_graph_construction(node_list, False)
            #LDFmultichannelscheduling.frequency_assignment(node_list, False)
            """
            # trees.build_bfs(node_list)
            # trees.dijkstra_duty_cycle_1slot(node_list, 10)
            draw.draw(node_list)

            LDFmultichannelscheduling.scheduling(node_list)
            #validation.schedule_validation(node_list)

            channel_list_each_topo = []

            for u in node_list:
                channel_list_each_topo.append(u.channel)
            print("Maximum channel has been used in topo %u: %u " % (i, max(channel_list_each_topo)))
            total_channel_list.append(max(channel_list_each_topo))

            node_list.clear()
            LDFmultichannelscheduling.edge_c.clear()
            LDFmultichannelscheduling.vertex_c.clear()

        if scheduling_scheme == 3:
            """
            Multi-channel Duty-cycle co-scheduling
            """
            multichannel_dutycycle_coscheduling.tree_construction_based_mis(node_list)
            #draw.draw(node_list)
            multichannel_dutycycle_coscheduling.EDAS(node_list)

            for u in range(1, len(node_list)):
                parent = node_list[u].parentID
                count = 1
                while parent != 0:
                    parent = node_list[parent].parentID
                    count += 1
                    if count > len(node_list):
                        print("This is not a valid tree")
                        break


            #draw.draw(node_list)
            #validation.schedule_validation(node_list)
            channel_list_each_topo = []

            wp_list.append(node_list[0].wp)
            for u in node_list:
                channel_list_each_topo.append(u.channel)
            print("Maximum channel has been used in topo %u: %u " % (i, max(channel_list_each_topo)))

            node_list.clear()
            bnj_MultiChannel_CoScheduling.edge_c.clear()
            bnj_MultiChannel_CoScheduling.vertex_c.clear()

            total_channel_list.append(max(channel_list_each_topo))

    sum_channel = 0
    sum_wp = 0
    print("total channel list: ", total_channel_list)
    print(len(total_channel_list))
    print("total working period: ", wp_list)
    print(len(wp_list))
    for each_channel in total_channel_list:
        sum_channel = sum_channel + each_channel
    print("Average channels were used: ", sum_channel/400)

    for each_wp in wp_list:
        sum_wp = sum_wp + each_wp
    print("Average working period were used: ", sum_wp/400)



    #for node in node_list:
    #   print(node.ID," has children ",node.childrenIDs)
    print("finish!!!")



