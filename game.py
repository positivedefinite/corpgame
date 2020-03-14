import plac, corpgame
from logger import log

log.setLevel("info")


@plac.annotations(number_of_players=("Amount of players", "option", "n", int))
def main(number_of_players=3):
    manager = corpgame.GameManager(number_of_players)
    players = manager.get_random_players()
    # players = [[100, 100], [100, 100], [100, 100], [100, 100]]
    game_settings = {
        "start_populations_matrix": players,
        "topology": "fully_connected"
    }
    game = corpgame.PolymatrixGame(**game_settings)
    log.info(f" Network edges: {game.network.edges}")
    game.play(manager.get_random_strategy_profile())
    log.info(f" Game state {game.state.tolist()}")
    game.play(manager.get_random_strategy_profile())
    log.info(f" Game state {game.state.tolist()}")
    log.info(f"Simulated for {amount} players")

if __name__ == "__main__":
    plac.call(number_of_players)
    
