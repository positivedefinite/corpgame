# following architecture guidelines from https://realpython.com/python-application-layouts/
import os
import numpy as np
from logger import log
from player import Player

class MultiplayerGame:
    """ A multiplayer game with state vector for each player """
    def __init__(self, start_populations_matrix=[], network=None):
        self.players = None
        self.network = None
        self.strategy_profile = None
        self.payoff_matrix = None
        self.payoffs = {}
        self.state = None
        self.nash = {}
        if start_populations_matrix!=[]:
            self.initiate_players(start_populations_matrix=start_populations_matrix)
            self.get_state()

    def initiate_players(self, start_populations_matrix: list, player_names_list=None):
        """ Adds players to the game one by one """
        assert self.players == None # make sure that there aren't any players in the game
        assert type(start_populations_matrix)==list
        assert all(len(x) == len(start_populations_matrix[0]) for x in start_populations_matrix)
        players_list = []
        for i, population_vector in enumerate(start_populations_matrix):
            players_list.append(Player(population_vector=population_vector, index=i))
        self.players = players_list
        return True

    def get_state(self):
        """ Extract state of each player and concat them into np.array """
        assert self.players != None
        self.state = np.concatenate([[np.array(player.population) for player in self.players]])
        return True

    def set_strategy_profile(self, strategy_profile=[0, 1, 1]):
        """ Use a vector of pure strategies to assign it to players """
        for i, strategy in enumerate(strategy_profile):
            self.players[i].strategy = strategy
        self.strategy_profile = [player.strategy for player in self.players]
        return True


class PolymatrixGame(MultiplayerGame):
    def play(self, strategy_profile):
        """ Wrapper method for setting a strategy profile, computing payoff and distributing it to players """
        self.set_strategy_profile(strategy_profile)
        self.get_payoff_matrix()
        self.apply_payoff_matrix()
        #self.get_payoffs()
        self.get_state()

    def apply_payoff_matrix(self):
        """ Applies payoffs to all players """
        log.info(f"{self.__class__}.apply_payoff_matrix() using payoff matrix {self.payoff_matrix.tolist()}")
        for i, payoff in enumerate(self.payoff_matrix):
            log.debug(f"{self.__class__}.apply_payoff_matrix() player {i} old state {self.players[i].population}")
            log.debug(f"{self.__class__}.apply_payoff_matrix() player {i} should get {payoff}")
            self.players[i].apply_player_payoff(payoff)
            log.debug(f"{self.__class__}.apply_payoff_matrix() player {i} new state {self.players[i].population}")

    def get_payoff_matrix(self):
        """ Computes payoffs for all player pairs (edges) """
        payoff_matrix = np.zeros((len(self.players),2))
        log.debug(f"{self.__class__}.get_payoff_matrix() init {payoff_matrix.tolist()}")
        network_edges = [[0,1],[1,2]]
        for pair in network_edges:
            p1 = pair[0]
            p2 = pair[1]
            p1_payoff, p2_payoff = self.pair_fractional(p1, p2)
            log.debug(f"{self.__class__}.get_payoff_matrix() payoffs {p1_payoff} {p2_payoff}")
            payoff_matrix[p1]+=p1_payoff
            payoff_matrix[p2]+=p2_payoff
        log.debug(f"{self.__class__}.get_payoff_matrix() final {payoff_matrix.tolist()}")
        self.payoff_matrix = payoff_matrix
        return self

    def pair_fractional(self, player1: int, player2: int):
        """ Computer payoff between two players (one edge) """
        alpha = 0.1 #1/len(self.players)
        p1 = self.players[player1]
        p2 = self.players[player2]
        p1_payoff= np.zeros(2)
        p2_payoff= np.zeros(2)
        if p1.strategy!=p2.strategy:
            log.debug(f"{self.__class__}.pair_fractional() strategy pair is: ({p1.strategy},{p2.strategy})")
            p1_losing_type = [1-p1.strategy]
            p1_losing_amount = self.payoff_function(x=p1.population[p1_losing_type], alpha=alpha)
            p1_payoff[p1_losing_type] -= p1_losing_amount
            p2_payoff[p1_losing_type] += p1_losing_amount
            log.debug(f"{self.__class__}.pair_fractional() p1 loss {p1_losing_type} {p1_losing_amount} {p1_payoff} {p2_payoff}")
            p2_losing_type = [1-p2.strategy]
            p2_losing_amount = self.payoff_function(x=p2.population[p2_losing_type], alpha=alpha)
            p2_payoff[p2_losing_type] -= p2_losing_amount
            p1_payoff[p2_losing_type] += p2_losing_amount
            log.debug(f"{self.__class__}.pair_fractional() p2 loss {p2_losing_type} {p2_losing_amount} {p1_payoff} {p2_payoff}")
        self.get_state()
        assert np.all((p1_payoff+p2_payoff)==0) # check if zero sum
        return [p1_payoff, p2_payoff]

    def payoff_function(self, x: int, alpha: float = 0.1, roundoff=True):
        """ A function that decides how much a player looses """
        y = alpha*x
        if roundoff:
            y = int(y)
        assert y>=0
        return y

    def print(self):
        for c in self.players:
            print("Player ", c.index, c.company, " score ", sum(c.company))

    def get_payoffs(self):
        self.get_state()
        base_state = self.state.copy()
        number_of_players = len(self.players)

        payoff = self.payoff
        strategies = all_binary_strategies(length=len(self.players))

        for strategy in strategies:
            str_strategy = "".join(map(str, strategy))
            self.players = []
            player_state = []
            # [list(base_state[:,0]),list(base_state[:,1]),list(base_state[:,2])]
            for i in range(number_of_players):
                player_state.append(list(base_state[:, i]))
            # print(player_state)
            self.player_generator(player_state)
            self.update_strategies(strategy)
            self.round()
            self.get_state()
            difference = self.state - base_state
            difference = np.sum(difference, axis=0)
            payoff[str_strategy] = list(difference)

    def get_nash(self):
        nash = self.nash
        strategies = all_binary_strategies(length=len(self.players))

        for strategy in strategies:
            str_strategy = "".join(map(str, strategy))
            nash[str_strategy] = self.is_strategy_nash(strategy)

    def is_strategy_nash(self, strategy):
        """
        For strategy being a list of binary values corresponding to 
        """
        is_nash = True
        base_payoff = self.payoff[
            "".join(map(str, strategy))
        ]  # np.sum(self.state, axis=0)
        for i in range(len(strategy)):
            compared_strategy = strategy.copy()
            compared_strategy[i] = 1 - compared_strategy[i]  # flips 1 and 0
            compare_payoff = self.payoff["".join(map(str, compared_strategy))]
            if base_payoff[i] < compare_payoff[i]:
                is_nash = False
            # print(strategy, compared_strategy, base_payoff[i]<compare_payoff[i])
        return is_nash

    def __call__(self):
        self.get_payoffs()
        return True
        # print('Payoffs:', self.payoff)

    def show_nash(self):
        is_nash = True
        if self.nash == {}:
            print("Nash empty!")
            is_nash = False
        self.get_nash()
        for key in self.nash:
            if self.nash[key] == True:
                print("Nash:", key, " with payoff ", self.payoff[key])
        return is_nash


def all_binary_strategies(length=3):
    from itertools import product

    strategies = []
    dummies = list(product(range(2), repeat=length))
    for i in range(0, len(dummies)):
        dummy = list(dummies[i])
        strategies.append(dummy)
    return strategies


def simulate(
    strategy=[1, 1, 0, 0, 0],
    start_population=[[5, 10], [5, 5], [15, 5], [15, 5], [30, 5]],
    iterations=10,
    payoff="discrete",
):
    game = Game()
    population = []
    game(start_population)
    # game.print()
    game.update_strategies(strategy)
    game.get_state()
    # game.print()
    s = [list(np.sum(game.state, axis=0))]
    # print(s)
    for i in range(iterations):
        game.update_strategies(strategy)
        if payoff == "fractional":
            game.round_fractional()
        elif payoff == "discrete":
            game.round()
        else:
            raise Error("Wrong payoff name")
        game.get_state()
        # game.print()
        s.append(list(np.sum(game.state, axis=0)))
    population = np.array(s)
    return population
