from corpgame import PolymatrixGame
from visualize import *
import numpy as np

game_settings = {
            "start_populations_matrix": [[6,6],[12,9],[9,21],[3,6]],
    "player_labels": [1,2,3,1],
            "topology": "fully_connected",
            'alpha': 1.0,
            'log_level': "error"
        }
game = PolymatrixGame(**game_settings)
game.solve()
import pprint
pprint.pprint(game.payoffs)
print(game.pne)