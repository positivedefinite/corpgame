import plac, corpgame
from logger import log

log.setLevel("info")


@plac.annotations(start=("Some starting parameter", "option", "s", str))
def main(start="ok"):
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
    

if __name__ == "__main__":
    plac.call(main)
    log.info("done {}".format(10))
