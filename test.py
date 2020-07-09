from corpgame import PolymatrixGame

game_settings = {
        "start_populations_matrix": [[6,4],[2,6],[10,0]],
        "player_labels":['Denmark','Canada','Moonnation'],
        "topology": "fully_connected",
        'alpha': 1.0,
        'log_level': "error"
    }
game = PolymatrixGame(**game_settings)

for p in game.players:
    p.print()
    print()
