import os
import numpy as np
from logger import log
import networkx as nx
import random
import copy


class Network(nx.Graph):
    """ A wrapper class for NetworkX Graph() class """

    def __init__(self, nodes: list = None, topology="fully_connected"):
        if type(topology) == str:
            if topology == "fully_connected":
                topology = [
                    [nodes[i], nodes[j]]
                    for i in range(len(nodes))
                    for j in range(i + 1, len(nodes))
                ]
            elif topology == "chain":
                topology = [[nodes[i - 1], nodes[i]] for i in range(1, len(nodes))]
            elif topology == "ring":
                topology = [[nodes[i - 1], nodes[i]] for i in range(1, len(nodes))]
                topology.append([nodes[-1], nodes[0]])
            elif topology == "star": # node 0 is the center
                topology = [[nodes[0], nodes[i]] for i in range(1, len(nodes))]
            else:
                raise ValueError(
                    f"{self.__class__}.__init__ unrecognized network topology '{topology}', try 'fully_connected', 'ring', 'chain' or 'star'"
                )
        elif type(topology) == list:
            # taking a list of edges
            pass
        else:
            raise "Bad topology data structure"
        #self.graph = graph
        self = super().__init__(topology)
    
    def remove_random_edge(self):
        # TODO: label edges if their removal is found to disconnect the graph, to avoid re-visiting them ever
        keep_looking = True
        edges = list(np.random.permutation(list(self.edges)))
        if len(edges)==0:
            raise ValueError(f"Cannot remove any more edges, the graph is probably already a spanning tree")
        while keep_looking and len(edges)>0: # try to remove edges but only if it doesn't disconnect the graph
            temp_graph = copy.deepcopy(self)
            temp_graph.remove_edge(*list(edges.pop(0)))
            if nx.algorithms.components.is_connected(temp_graph):
                self = copy.deepcopy(temp_graph)
                keep_looking=False

    def add_random_edge(self):
        def in_list(candidate, full_list):
            for element in full_list:
                if candidate==element:
                    return True
            return False
        keep_looking = True
        n = len(self.nodes)
        m = len(self.edges)
        if m<n*(n-1)/2: # check if it's not a complete graph already
            edges = list(self.edges)
            nodes = list(range(0,n))
            possible_edges = [
                            [nodes[i], nodes[j]]
                            for i in range(len(nodes))
                            for j in range(i + 1, len(nodes))
                        ]
            while keep_looking and len(possible_edges)>0: # try to add edges if they're not already there
                #print(len(possible_edges))
                edge_candidate = tuple(possible_edges.pop(np.random.randint(0,len(possible_edges))))
                
                #print(edge_candidate, edges, in_list(edge_candidate, edges))
                if not in_list(edge_candidate, edges):
                    temp_graph = copy.deepcopy(self)
                    temp_graph.add_edge(*edge_candidate)
                    if nx.algorithms.components.is_connected(temp_graph):
                        self.add_edge(*edge_candidate)
                        keep_looking = False
        


