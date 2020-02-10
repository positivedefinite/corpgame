class Player:
    def __init__(self, population, index=0):
        """
        Create a player country with a population of companies
        """
        self.company = [0] * len(population)
        for i in range(len(population)):
            self.company[i] = population[i]
        self.strategy = [None, None]
        self.index = index
        self.round_history = []
        log.debug(
            "Created player object with population "
            + str(self.company)
            + " under index "
            + str(self.index)
        )

    def __call__(self, payoffs):
        """
        Takes a payoff (positive or negative) and distributes it to the player
        """
        for i in range(len(payoffs)):
            self.company[i] += payoffs[i]
        self.round_history.append(payoffs)
        return migration