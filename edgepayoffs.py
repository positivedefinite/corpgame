from corpgame import PolymatrixGame
from pprint import pprint
player_labels = ['Mordor','Kalimandor','Shire']
game = PolymatrixGame([[10,10],[20,20],[0,0]],player_labels=player_labels)
game.play([1,0,0])
pprint(game.edge_payoffs)
pprint(game.state)

import pickle
population = pickle.load(open('./data/optimization/population_random_10.70.pickle','rb'))
hypothesis = population[0]
game_settings = {
            "start_populations_matrix": hypothesis['starting_state'],
            "topology": hypothesis['topology'],
            'alpha': hypothesis['alpha'],
            'player_labels':hypothesis['player_labels'],
            'log_level': "warning"
        }
game = PolymatrixGame(**game_settings)
pprint(game.state)
#pprint(hypothesis['strategies'][0])
#pprint(hypothesis['strategies'][0][0])
#pprint(hypothesis['strategies'][0][0][0])
game.play(list(hypothesis['strategies'][0][0]))
pprint(game.edge_payoffs)