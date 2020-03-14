import plac, corpgame, manager
from logger import log

log.setLevel("info")


@plac.annotations(amount=("Amount of players", "option", "a", int))
def main(amount=3):
    manager.Manager.get_random_players(3)
    game_settings = {
        "start_populations_matrix": [[100, 100], [100, 100], [100, 100], [100, 100]],
        "topology": "fully_connected"
    }
    game = corpgame.PolymatrixGame(**game_settings)
    log.info(f" Network edges: {game.network.edges}")
    game.play([0, 1, 0, 1])
    log.info(f" Game state {game.state.tolist()}")
    game.play([0, 1, 1, 1])
    log.info(f" Game state {game.state.tolist()}")
    log.info(f"Simulated for {amount} players")

if __name__ == "__main__":
    plac.call(main)
    
