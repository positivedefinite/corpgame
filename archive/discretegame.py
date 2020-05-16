import os, random
import numpy as np
from logger import log
from player import Player
from network import Network
from multiplayergame import MultiplayerGame


class DiscreteGame(MultiplayerGame):
    def play(self, strategy_profile):
        """ Wrapper method for setting a strategy profile, computing payoff and distributing it to players """
        self.set_strategy_profile(strategy_profile)
        self.get_payoff_matrix()
        self.apply_payoff_matrix()
        self.get_state()

    def print(self):
        for c in self.players:
            print("Player ", c.index, c.company, " score ", sum(c.company))

    def get_payoffs(self):
        self.get_state()
        base_state = self.state.copy()
        number_of_players = len(self.players)

        payoff = self.payoffs
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
            self.payoffs = payoff

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
