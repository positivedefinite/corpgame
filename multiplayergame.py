import os, random
import numpy as np
from logger import log
from player import Player
from network import Network
from collections import defaultdict
import itertools


class MultiplayerGame: # ! change to NetworkGame
    """ A multiplayer game with state vector for each player """

    def __init__(
        self,
        start_populations_matrix=[],
        player_labels = None,
        topology="fully_connected",
        alpha=0.5, # ! REMOVE
        log_level="info",
    ):
        self.alpha = alpha
        self.players = None
        self.network = None
        self.loss_velocity = None
        self.strategy_profile = None
        self.payoff_matrix = None
        self.payoffs = {}
        self.state = None
        self.nash = {}
        log.setLevel(log_level)
        if start_populations_matrix != []:
            self.initiate_players(start_populations_matrix=start_populations_matrix, player_labels=player_labels)
            self.get_state()
            self.players_indices = [player.index for player in self.players]
            log.info(
                f"{self.__class__}.__init__() players indexed {self.players_indices}"
            )
            self.network = Network(nodes=self.players_indices, topology=topology)
        else:
            log.warning(
                f"{self.__class__}.__init__() players and network not initiated"
            )
        self.edge_payoffs = defaultdict()
        for edge in itertools.permutations(player_labels, 2):
            self.edge_payoffs[edge]= np.array([0.,0.]) #! this creates new dictionary keys!

    def initiate_players(self, start_populations_matrix: list, player_labels=None):
        """ Adds players to the game one by one """
        assert (
            self.players == None
        )  # make sure that there aren't any players in the game
        assert type(start_populations_matrix) == list
        assert all(
            len(x) == len(start_populations_matrix[0]) for x in start_populations_matrix
        )
        if player_labels!=None:
            assert len(player_labels)==len(start_populations_matrix)
        players_list = []
        for i, population_vector in enumerate(start_populations_matrix):
            players_list.append(Player(population_vector=population_vector, index=i))
            if player_labels!=None:
                players_list[i].label = player_labels[i]
        self.players = players_list
        return True

    def get_state(self):
        """ Extract state of each player and concat them into np.array """
        assert self.players != None
        self.state = np.concatenate(
            [[np.array(player.population) for player in self.players]]
        )
        return True

    def set_strategy_profile(self, strategy_profile=[0, 1, 1]):
        """ Use a vector of pure strategies to assign it to players """
        assert len(strategy_profile) == len(
            self.players
        ), f"Length of strategy_profile {len(strategy_profile)} does not match the amount of players {len(self.players)}"
        for i, strategy in enumerate(strategy_profile):
            self.players[i].strategy = strategy
        self.strategy_profile = [player.strategy for player in self.players]
        return True

    def apply_payoff_matrix(self):
        """ Applies payoffs to all players """
        log.info(
            f"{self.__class__}.apply_payoff_matrix() using payoff matrix {self.payoff_matrix.tolist()}"
        )
        for i, payoff in enumerate(self.payoff_matrix):
            log.debug(
                f"{self.__class__}.apply_payoff_matrix() player {i} old state {self.players[i].population}"
            )
            log.debug(
                f"{self.__class__}.apply_payoff_matrix() player {i} should get {payoff}"
            )
            self.players[i].apply_player_payoff(payoff)
            log.debug(
                f"{self.__class__}.apply_payoff_matrix() player {i} new state {self.players[i].population}"
            )
        self.get_state()

    @classmethod
    def get_payoff_matrix(self):
        return self
