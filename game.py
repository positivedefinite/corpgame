import plac, corpgame
from logger import log

log.setLevel('debug')

@plac.annotations(
    start=("Some starting parameter","option","s", str)
    )
    
def main(start='ok'):
    game = corpgame.PolymatrixGame()
    game.initiate_players(start_populations_matrix = [[3, 10], [10, 2], [2, 1]])
    game.get_state()
    #print(game.state)
    game.play([0,1,0])

if __name__=="__main__":
    plac.call(main)
    log.info('done {}'.format(10))