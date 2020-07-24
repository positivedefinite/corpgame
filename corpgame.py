# following architecture guidelines from https://realpython.com/python-application-layouts/
# ! Rename module to polygame
import os, random
import numpy as np
from logger import log
from player import Player
from multiplayergame import MultiplayerGame
from pprint import pprint
import itertools
from collections import defaultdict


class PolymatrixGame(MultiplayerGame):

    def play(self, strategy_profile=None):
        """ INSTANCE METHOD
        Wrapper for setting a strategy profile, computing payoff and distributing it to players.
        If strategy profile is not specified, a random strategy profile is chosen.
        """
        if strategy_profile.all()==None:
            strategy_profile = np.random.randint(0,2,len(self.players))
        self.set_strategy_profile(strategy_profile)
        self.get_payoff_matrix()
        self.apply_payoff_matrix()
        self.get_state()

    def get_directed_payoffs(self):
        ''' INSTANCE METHOD Transforms a dictionary with np.array() as values to int values. '''
        #print(self.edge_payoffs)
        edge_dict = self.edge_payoffs.copy()
        for edge in edge_dict:
            val = edge_dict[edge]
            # only take the positive value in the array, as that's the amount of companies going from 0 to 1 (the other direction is handled for edge (1,0))
            if val[0]>0:
                edge_dict[edge] = val[0]
                assert val[1]<=0, f"val = {val}, type={type(val)}"
            elif val[1]>0:
                edge_dict[edge] = val[1]
                assert val[0]<=0, f"val = {val}, type={type(val)}"
            else:
                assert val[1]<=0 and val[0]<=0, f"val = {val}, type={type(val)}"
                edge_dict[edge] = 0
        self.directed_edge_payoffs = edge_dict

    def get_payoff_matrix(self):
        """ INSTANCE METHOD Computes payoffs for all player pairs (edges) """
        payoff_matrix = np.zeros((len(self.players), 2))
        log.debug(f"{self.__class__}.get_payoff_matrix() init {payoff_matrix.tolist()}")
        network_edges = self.network.edges
        for pair in network_edges:
            p1 = pair[0]
            p2 = pair[1]
            p1_payoff, p2_payoff = self.pair_fractional(p1, p2)
            log.debug(
                f"{self.__class__}.get_payoff_matrix() payoffs {p1_payoff} {p2_payoff}"
            )
            payoff_matrix[p1] += p1_payoff
            payoff_matrix[p2] += p2_payoff
        log.debug(
            f"{self.__class__}.get_payoff_matrix() final {payoff_matrix.tolist()}"
        )
        self.payoff_matrix = payoff_matrix

    def pair_fractional(self, player1: int, player2: int):
        """ Computer payoff between two players (one edge) """
        alpha = 1 / len(self.players)
        p1 = self.players[player1]
        p2 = self.players[player2]
        p1_payoff = np.zeros(2)
        p2_payoff = np.zeros(2)
        if p1.strategy != p2.strategy:
            log.debug(
                f"{self.__class__}.pair_fractional() strategy pair is: ({p1.strategy},{p2.strategy})"
            )
            p1_losing_type = [1 - p1.strategy]
            p1_losing_amount = self.payoff_function(
                x=p1.population[p1_losing_type], alpha=alpha
            )
            p1_payoff[p1_losing_type] -= p1_losing_amount
            p2_payoff[p1_losing_type] += p1_losing_amount
            log.debug(
                f"{self.__class__}.pair_fractional() p1 loss {p1_losing_type} {p1_losing_amount} {p1_payoff} {p2_payoff}"
            )
            p2_losing_type = [1 - p2.strategy]
            p2_losing_amount = self.payoff_function(
                x=p2.population[p2_losing_type], alpha=alpha
            )
            p2_payoff[p2_losing_type] -= p2_losing_amount
            p1_payoff[p2_losing_type] += p2_losing_amount
            log.debug(
                f"{self.__class__}.pair_fractional() p2 loss {p2_losing_type} {p2_losing_amount} {p1_payoff} {p2_payoff}"
            )
        self.get_state()
        assert np.all((p1_payoff + p2_payoff) == 0)  # check if zero sum
        assert (p1.label, p2.label) in self.edge_payoffs
        assert (p2.label, p1.label) in self.edge_payoffs
        self.edge_payoffs[(p1.label, p2.label)]=p2_payoff
        self.edge_payoffs[(p2.label, p1.label)]=p1_payoff
        log.debug(p1.label, p1.strategy, p1_payoff, p2.label, p2.strategy, p2_payoff)
        return [p1_payoff, p2_payoff]

    def payoff_function(self, x: int, alpha: float = 0.1, roundoff=False):
        """ A function that decides how much a player looses """
        # ! alpha is overriden b self.alpha
        y = x * self.alpha / (len(self.players) - 1)
        # print(f'Payoff function x={x},alpha={self.alpha},not rounded y={y}')
        if roundoff:
            y = int(y)
        log.debug(
                f"{self.__class__}.payoff_function() y={y}"
            )
        assert y >= 0
        return y
    
    def action_space(self):
        """ Only use under self.analyse """
        subdict = {'payoff_matrix':None, 'payoff':None, 'pure_nash':None}
        self.actions = {"".join(map(str, strategy)):subdict.copy() for strategy in all_binary_strategies(len(self.players))}

    def get_all_payoffs(self):
        """ Only use under self.analyseInstance method to write self.payoffs """
        base_players = self.players.copy()
        base_state = self.state.copy()
        base_profile = self.strategy_profile
        #pprint(self.actions)
        strategies = all_binary_strategies(length=len(self.players))
        for strategy in strategies:
                self.set_strategy_profile(strategy)
                self.get_payoff_matrix()
                self.actions[strs(strategy)]['payoff_matrix'] = self.payoff_matrix.tolist()
                payoff = np.sum(self.payoff_matrix, axis=1)
                self.payoffs[strs(strategy)]=payoff.tolist()
                self.actions[strs(strategy)]['payoff']=payoff.tolist()
                self.players = base_players
                self.state = base_state
                self.strategy_profile = base_profile
        #pprint(self.payoffs)
        return self
    def is_strategy_nash(self, strategy):
        """Only use under self.analyse"""
        is_nash = True
        base_payoff = self.payoffs[
            "".join(map(str, strategy))
        ]  # np.sum(self.state, axis=0)
        for i in range(len(strategy)):
            compared_strategy = strategy.copy()
            compared_strategy[i] = 1 - compared_strategy[i]  # flips 1 and 0
            compare_payoff = self.payoffs["".join(map(str, compared_strategy))]
            if base_payoff[i] < compare_payoff[i]:
                is_nash = False
            # print(strategy, compared_strategy, base_payoff[i]<compare_payoff[i])
        return is_nash

    def get_pure_nash(self):
        """ Instance method for getting pure nash """
        strategies = all_binary_strategies(length=len(self.players))
        self.nash = {"".join(map(str, strategy)):None for strategy in strategies}
        for strategy in strategies:
            str_strategy = "".join(map(str, strategy))
            is_nash = self.is_strategy_nash(strategy)
            self.nash[str_strategy] = is_nash
            self.actions[str_strategy]['pure_nash'] = is_nash
    
    def count_nash(self):
        self.nash_counter = 0
        for key in self.actions:
            if self.actions[key]['pure_nash']==True:
                self.nash_counter += 1
        return self.nash_counter
    
    def get_pne(self):
        self.pne = {}
        for key in self.actions:
            if self.actions[key]['pure_nash']==True:
                self.pne[key] = self.actions[key]['payoff']
    
    def get_all_actions(self):
        self.action_space()
        self.get_all_payoffs()
        self.get_pure_nash()
        self.count_nash()
        self.get_pne()
    
    def solve(self):
        self.get_all_actions()
  
    
    def print_nash(self):
        for key in self.actions:
            if self.actions[key]['pure_nash']==True:
                print(key)
                pprint(self.actions[key])

    def naive_best_reply(self, start_strategy):
        """ Given a strategy vector, what would be a new vector of naive best replies? """
        self.strategy_profile = start_strategy
        base_players = self.players.copy()
        base_state = self.state.copy()
        base_profile = self.strategy_profile
        self.get_all_payoffs()
        #print(f"Last profile {base_profile} with new payoff {self.payoffs[strs(base_profile)]}")
        new_profile = [None]*len(self.players)
        # check all deviations
        for player in self.players:
            #print(player.index)
            base_payoff = self.payoffs[strs(self.strategy_profile)]
            deviation_strategy = self.strategy_profile.copy()
            deviation_strategy[player.index]=1-deviation_strategy[player.index]
            #print(player.index, deviation_strategy, self.payoffs[strs(deviation_strategy)])
            deviation_payoff = self.payoffs[strs(deviation_strategy)]
            if deviation_payoff[player.index]>base_payoff[player.index]:
                new_profile[player.index]=deviation_strategy[player.index]
            else:
                new_profile[player.index]=base_profile[player.index]
        #print(f"Naive best-reply profile {new_profile} with payoff {self.payoffs[strs(self.strategy_profile)]}")
        return new_profile
        
    def naive_best_replies(self):
        self.get_all_actions()
        from collections import defaultdict
        d = defaultdict()
        for strategy in all_binary_strategies(len(self.players)):
            naive_profile = self.naive_best_reply(strategy)
            key = str(naive_profile)
            if key not in d.keys():
                d[key]=[]
            d[key].append(strategy)
        self.naive = d

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

def strs(strategy):
    return "".join(map(str, strategy))

class GameManager:
    def __init__(self, number_of_players=3):
        self.number_of_players = number_of_players
        pass

    def get_random_players(self, lower_bound=0, upper_bound=100):
        n = self.number_of_players
        players = [
            [random.randint(lower_bound, upper_bound), random.randint(lower_bound, upper_bound)] for i in range(n)
        ]
        return players

    def get_random_strategy_profile(self):
        n = self.number_of_players
        strategy_profile = [random.randint(0, 1) for i in range(n)]
        return strategy_profile
