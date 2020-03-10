import os
import numpy as np
from logger import log
import networkx as nx

class Network:
    """ A wrapper class for NetworkX Graph() class """
    def __init__(self, nodes: list=None, topology='fully_connected'):
        if type(topology)==str:
            if topology=='fully_connected':
                self.edges = self.all_pairs(nodes)
            elif topology=='chain':
                self.edges = [[nodes[i-1],nodes[i]] for i in range (1, len(nodes))]
            elif topology=='ring':
                self.edges = [[nodes[i-1],nodes[i]] for i in range (1, len(nodes))]
                self.edges.append([nodes[-1],nodes[0]])
            elif topology=='star':
                self.edges = [[nodes[0],nodes[i]] for i in range (1, len(nodes))]
            else:
                raise ValueError(f'{self.__class__}.__init__ unrecognized network topology \'{topology}\'')
            graph = nx.Graph(self.edges)
        elif type(topology)==list:
            # taking a list of edges
            graph = nx.Graph(topology)
        self.graph = graph

    def all_pairs(self, items):
        """ retrieved from https://stackoverflow.com/questions/5360220/how-to-split-a-list-into-pairs-in-all-possible-ways"""
        pairs = [[items[i],items[j]] for i in range(len(items)) for j in range(i+1, len(items))]
        return pairs