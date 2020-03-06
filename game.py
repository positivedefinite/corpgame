import plac, corpgame
from logger import log

log.setLevel('info')

@plac.annotations(
    start=("Some starting parameter","option","s", str)
    )
    
def main(start='ok'):
    game = corpgame.Game()
    game.initiate_players(start_populations_matrix = [[3, 0], [1, 2], [2, 1]])
    game.set_strategy_profile(strategy_profile = [0, 1, 1])

if __name__=="__main__":
    plac.call(main)
    log.info('done {}'.format(10))