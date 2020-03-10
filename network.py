import os
import numpy as np
from logger import log
import networkx as nx


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
            elif topology == "star":
                self.edges = [[nodes[0], nodes[i]] for i in range(1, len(nodes))]
            else:
                raise ValueError(
                    f"{self.__class__}.__init__ unrecognized network topology '{topology}'"
                )
            graph = nx.Graph(self.edges)
        elif type(topology) == list:
            # taking a list of edges
            graph = nx.Graph(topology)
        self.graph = graph
