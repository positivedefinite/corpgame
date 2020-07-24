from corpgame import PolymatrixGame
from pprint import pprint
from genetic import *
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
#game = PolymatrixGame(**game_settings)
e = evaluate_edge(hypothesis)
print(*e)