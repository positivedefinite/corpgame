import plac, corpgame
from logger import log




@plac.annotations(number_of_players=("Amount of players", "option", "n", int),
                    log_level=("Preferred level of logging", "option", "log", str),
                    timesteps=("Amount of rounds to be played", "option", "t", int))
def main(number_of_players=3, timesteps=2, log_level="warning"):
    #log.setLevel(log_level)
    #print(log.handlers, log.handler)
    manager = corpgame.GameManager(number_of_players)
    players = manager.get_random_players()
    # players = [[100, 100], [100, 100], [100, 100], [100, 100]]
    game_settings = {
        "start_populations_matrix": players,
        "topology": "fully_connected",
        'alpha': 1.0,
        'log_level': log_level
    }
    game = corpgame.PolymatrixGame(**game_settings)
    log.info(f"Simulated for {number_of_players} players")
    log.info(f" Network topology: {game_settings['topology']}")
    print(f" Game state {game.state.tolist()}")
    for i in range(timesteps):
        game.play(manager.get_random_strategy_profile())
        print(f" Strategy profile: {game.strategy_profile}")
        print(f" Game state {game.state.tolist()}")
    manager.naive_best_reply(game, 3)

if __name__ == "__main__":
    plac.call(main)
    
