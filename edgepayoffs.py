from corpgame import PolymatrixGame
from pprint import pprint
from genetic import *

player_labels = ['Mordor','Kalimandor','Shire']
game = PolymatrixGame([[10,10],[20,20],[0,0]],player_labels=player_labels)


import pickle
population = pickle.load(open('./data/optimization/population_random_10.70.pickle','rb'))
hypothesis = population[0]
game_settings = {
            "start_populations_matrix": hypothesis['starting_state'],
            "topology": hypothesis['topology'],
            'alpha': 0.0,
            'player_labels':hypothesis['player_labels'],
            'log_level': "warning"
        }
game = PolymatrixGame(**game_settings)
#pprint(game.state)
print(len(game.edge_payoffs))
for edge in game.edge_payoffs:
    #print(type(edge), edge, game.edge_payoffs[edge])
    continue

game.play()
#pprint(game.state)
print(len(game.edge_payoffs))
for edge in game.edge_payoffs:
    #print(type(edge), edge, game.edge_payoffs[edge])
    continue
#pprint(hypothesis['strategies'][0])
#pprint(hypothesis['strategies'][0][0])
#pprint(hypothesis['strategies'][0][0][0])
#game.play(list(hypothesis['strategies'][0][0]))
#pprint(game.edge_payoffs)
import numpy as np
s = np.array([0, 0])
for edge in game.edge_payoffs:
    if type(game.edge_payoffs[edge])!='NoneType':
        s = s+game.edge_payoffs[edge]
print(s)
game.get_directed_payoffs()
print(len(game.edge_payoffs))
pprint(game.edge_payoffs)
print(len(game.edge_payoffs))
#pickle.dump(game.edge_payoffs, open('C:/Users/Kinga/OneDrive/thesis/data/corpgame/predicted_edge_payoff.pickle','wb'))
