from pprint import pprint
import pandas as pd
import numpy as np
from logger import log
from corpgame import PolymatrixGame
from corpgame import GameManager

import random
import random
x=[]
y=[]
for games in range(10):
    print(games)
    manager = GameManager(6)
    players = manager.get_random_players()
    game_settings = {
        "start_populations_matrix": players,
        "topology": "fully_connected",
        'alpha': 1.0,
        'log_level': "error"
    }
    game = PolymatrixGame(**game_settings)
    #print(f"Initiated a game with {len(game.network.graph.nodes)} players and {len(game.network.graph.edges)} edges")

    for iterations in range(12):
        #print(f"Network edges: {game.network.graph.edges}")
        game.get_all_actions()
        #print(f"Amount of edges: {len(game.network.graph.edges)}, amount of PNE: {game.nash_counter}")
        #game.print_nash()
        x.append(iterations)
        y.append(game.nash_counter)
        edges = list(game.network.graph.edges)
        edge_num = random.randint(0, len(edges)-1)
        #print(f"removing edge {edge_num}\n")
        game.network.graph.remove_edge(*edges[edge_num])
print(x)
print(y)