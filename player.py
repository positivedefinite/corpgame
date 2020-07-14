import os
import numpy as np
from logger import log


class Player:
    def __init__(self, population_vector: np.array, index=None, label=None):
        """
        Create a player country with a population. 
        Players are "stupid" and don't know anything, such as who are their neighbors or what is best to do.   
        """
        self.population = np.array(population_vector).astype(float)
        self.strategy = None
        self.index = index
        self.label = label
        self.history = []
        log.debug(
            f"{self.__class__}.__init__ created player indexed {str(self.index)} with population {str(self.population)}"
        )

    def apply_player_payoff(self, payoffs_vector: np.array):
        """
        Takes a payoff vector (positive or negative) and distributes it to the player
        """
        assert self.strategy != None, f"Player {(self.index, self.label)} doesn't have a strategy and cannot be assigned with payoff."
        assert len(payoffs_vector) == len(self.population)
        for i, payoff in enumerate(payoffs_vector):
            self.population[i] += payoff
        self.history.append({"strategy": self.strategy, "payoff": payoffs_vector})
        # situation changes so the player doesn't know what he's going to do now, reset strategy
        self.strategy = None
        return True

    def set_strategy(self, strategy):
        assert self.strategy == None, f"Player {(self.index, self.label)} already has a strategy, but it was not used?"  # to avoid overwritting an existing strategy
        self.strategy = strategy
        return True

    def print(self):
        print(f"Index: {self.index}")
        print(f"Label: {self.label}")
        print(f"Population: {self.population}")
        print(f"Strategy: {self.strategy}")
        print(f"History: {self.history}")