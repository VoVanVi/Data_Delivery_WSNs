"""@package docstring
Programmed by Vi @SKKU, Korea
Data structure of a network node
"""

class Node:
    ## The constructor
    def __init__(self, ID=0, x=0.0, y=0.0, active_slot= []):
        ## ID of a node
        self.ID = ID
        ## x-axis position
        self.x = x
        ## y-axis position
        self.y = y
        ##active slot
        self.active_slot = active_slot
        ##ID of ancestor
        self.ancestorIDs = []
        ## ID of the parent
        self.parentID = None
        ## list of children
        self.childrenIDs = []
        ## list of descendent nodes used in LDF, MultiChannel Coscheduling (original idea) (created while scheduling)
        self.descIDs = []
        ## List of descendent nodes used in bnj MultiChannel Coscheduling (improved idea) (created while constructing a spanning tree)
        self.descIDs_prime = []
        ## list of neighbors
        self.neighborIDs = []
        ## list of neighbors in Constraint graph
        self.neighborIDs_gc = []
        ## active time slot
        #self.timeslot = 0
        ## transmitting channel
        self.channel = 0
        ## receiving channel
        self.rx_channel = 0
        ## transmitting working period
        self.wp = 0

        ## distance from the source, for building a BFS Tree
        self.distance = 100000

        self.layer = -1         # layer in the SPT


        self.next_layer_neighbors = []
        self.prev_layer_neighbors = []
        self.current_layer_neighbors = []

        # list of working periods that this node will hear other transmissions
        self.overhearing = []

        self.dcat_weight = 0

        self.added = 0
        # for constructing dfs tree:
        self.discovered = False

        #self.mat_dc = -1 # for MAT calculation for duty cycle network