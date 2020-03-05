import os
import numpy as np
from logger import log


class Player:
    def __init__(self, population_vector: np.array, index=None):
        """
        Create a player country with a population of companies
        """
        self.population = np.array(population_vector)
        self.strategy = None
        self.index = index
        self.history = []
        log.debug(
            f"Created player object with population {str(self.population)} under index {str(self.index)}"
        )

    def payoff(self, payoffs_vector):
        """
        Takes a payoff vector (positive or negative) and distributes it to the player
        """
        assert self.strategy != None
        assert len(payoffs_vector) == len(self.population)
        for i, payoff in enumerate(payoffs_vector):
            self.population[i] += payoff
        self.history.append({"strategy": self.strategy, "payoff": payoffs_vector})
        # situation changes so the player doesn't know what he's going to do now, reset strategy
        self.strategy = None
        return True

    def set_strategy(self, strategy):
        assert self.strategy == None  # to avoid overwritting an existing strategy
        self.strategy = strategy
        return True