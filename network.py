import os
import numpy as np
from logger import log
import networkx as nx
import random


class Network:
    """ A wrapper class for NetworkX Graph() class """

    def __init__(self, nodes: list = None, topology="fully_connected"):
        if type(topology) == str:
            if topology == "fully_connected":
                self.edges = [
                    [nodes[i], nodes[j]]
                    for i in range(len(nodes))
                    for j in range(i + 1, len(nodes))
                ]
            elif topology == "chain":
                self.edges = [[nodes[i - 1], nodes[i]] for i in range(1, len(nodes))]
            elif topology == "ring":
                self.edges = [[nodes[i - 1], nodes[i]] for i in range(1, len(nodes))]
                self.edges.append([nodes[-1], nodes[0]])
            elif topology == "star": # node 0 is the center
                self.edges = [[nodes[0], nodes[i]] for i in range(1, len(nodes))]
            else:
                raise ValueError(
                    f"{self.__class__}.__init__ unrecognized network topology '{topology}'"
                )
            graph = nx.Graph(self.edges)
        elif type(topology) == list:
            # taking a list of edges
            graph = nx.Graph(topology)
            self.edges = graph.edges
        else:
            raise "Bad topology"
        self.graph = graph
    
    def remove_random_edge(self):
        # TODO: label edges if their removal is found to disconnect the graph, to avoid re-visiting them ever
        keep_looking = True
        edges = list(np.random.permutation(list(self.graph.edges)))
        if len(edges)==0:
            raise ValueError(f"Cannot remove any more edges, the graph is probably already a spanning tree")
        while keep_looking: # try to remove edges but only if it doesn't disconnect the graph
            temp_graph = self.graph.copy()
            temp_graph.remove_edge(*list(edges.pop(0)))
            if nx.algorithms.components.is_connected(temp_graph):
                self.graph = temp_graph.copy()
                keep_looking=False
        


