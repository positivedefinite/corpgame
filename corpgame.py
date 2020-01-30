import logging, os
import numpy as np

# logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger()
log.setLevel(logging.INFO)


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


class Game:
    def __init__(self):
        self.players = []
        self.strategy = []
        self.payoff = {}
        self.state = []
        self.nash = {}

    def player_generator(self, input_population=[[3, 0], [1, 2], [2, 1]]):
        """
        Adds players to the game one by one
        """
        for i in range(1, len(input_population)):
            if len(input_population[i - 1]) != len(input_population[i]):
                error_text = (
                    "Inconsistent population sizes for indexes "
                    + str(i - 1)
                    + " and "
                    + str(i)
                )
                log.error(error_text)
                raise Error(error_text)
        if type(input_population) == list:
            for i in range(len(input_population)):
                self.players.append(Player(input_population[i], i))
        return self.players

    def update_strategies(self, strategies=[0, 1, 1]):
        givens = strategies
        for i in range(len(self.players)):
            given = givens[i]
            if given == 1:
                self.players[i].strategy = 1
            elif given == 0:
                self.players[i].strategy = 0
            else:
                log.error("You messed up.")
            # print('Player '+str(i)+' holds ('+str(self.players[i].company[0])+','+str(self.players[i].company[1])+') and decides '+str(self.players[i].strategy))
        # print('\n')
        self.strategy = [c.strategy for c in self.players]
        return self

    def round(self):
        """
        Play the game once
        """
        for i in range(len(self.players)):
            p1 = self.players[i]
            contestants = []
            # print('Player '+str(p1.index)+' with '+str(p1.company))
            for j in range(len(self.players)):
                p2 = self.players[j]
                if i != j and p1.strategy != p2.strategy:
                    contestants.append(p2)
                    # print('Contested by ' +str(p2.index)+' with strategy '+str(p2.strategy))
            # sort first by second company to ensure tie breaking
            losing_type = 1 - p1.strategy
            contestants.sort(key=lambda x: x.company[p1.strategy], reverse=True)
            contestants.sort(key=lambda x: x.company[losing_type], reverse=True)
            contested_amount = len(contestants)
            losing_amount = min(p1.company[losing_type], contested_amount)
            # print('Losing '+str(losing_amount)+' of type '+str(losing_type))
            p1.company[losing_type] -= losing_amount
            while losing_amount > 0:
                for i in range(len(contestants)):
                    if losing_amount > 0:
                        contestants[i].company[losing_type] += 1
                        losing_amount -= 1
                    else:
                        break
            all_players = contestants + [p1]
            all_players.sort(key=lambda x: x.index)
            # for c in all_players:
            # print(c.index, c.company)
            # print('\n')
            # break
        # for c in self.players:
        # print(c.index, c.company)
        # return contestants

    def print(self):
        for c in self.players:
            print("Player ", c.index, c.company, " score ", sum(c.company))

    def get_state(self):
        self.state = np.array(
            [[c.company[0] for c in self.players], [c.company[1] for c in self.players]]
        )
        return self

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

    def __call__(self, state=[[3, 0], [1, 2], [2, 1], [0, 0]], show_nash=True):
        self.player_generator(state)
        self.get_payoffs()
        # print('Payoffs:', self.payoff)
        self.get_nash()
        if show_nash == True:
            for key in self.nash:
                if self.nash[key] == True:
                    print("Nash:", key, " with payoff ", self.payoff[key])


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
    iterations=10
):
    game = Game()
    population = []
    game(start_population, show_nash=False)
    # game.print()
    game.update_strategies(strategy)
    game.get_state()
    s = [list(np.sum(game.state, axis=0))]
    # print(s)
    for i in range(interations):
        game.update_strategies(strategy)
        game.round()
        game.get_state()
        s.append(list(np.sum(game.state, axis=0)))
    population = np.array(s)
    return population
