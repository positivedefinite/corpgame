# following architecture guidelines from https://realpython.com/python-application-layouts/
import os, random
import numpy as np
from logger import log
from player import Player
from network import Network
from multiplayergame import MultiplayerGame


class PolymatrixGame(MultiplayerGame):
    def play(self, strategy_profile):
        """ Wrapper method for setting a strategy profile, computing payoff and distributing it to players """
        self.set_strategy_profile(strategy_profile)
        self.get_payoff_matrix()
        self.apply_payoff_matrix()
        self.get_state()

    def get_payoff_matrix(self):
        """ Computes payoffs for all player pairs (edges) """
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
        return self

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
        return [p1_payoff, p2_payoff]

    def payoff_function(self, x: int, alpha: float = 0.1, roundoff=True):
        """ A function that decides how much a player looses """
        # !!! alpha is overriden b self.alpha
        y = x * self.alpha / (len(self.players) - 1)
        # print(f'Payoff function x={x},alpha={self.alpha},not rounded y={y}')
        if roundoff:
            y = int(y)
        assert y >= 0
        return y


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


class GameManager:
    def __init__(self, number_of_players=3):
        self.number_of_players = number_of_players
        pass

    def get_random_players(self):
        n = self.number_of_players
        players = [
            [random.randint(n, n * 10), random.randint(n, n * 10)] for i in range(n)
        ]
        return players

    def get_random_strategy_profile(self):
        n = self.number_of_players
        strategy_profile = [random.randint(0, 1) for i in range(n)]
        return strategy_profile
