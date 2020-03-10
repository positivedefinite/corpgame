import plac, corpgame
from logger import log

log.setLevel('info')

@plac.annotations(
    start=("Some starting parameter","option","s", str)
    )
    
def main(start='ok'):
    game_settings = {
        'start_populations_matrix' : [
            [300, 100], 
            [100, 200], 
            [200, 100],
            [10,50]],
        'topology' : 'fully_connected'
    }
    game = corpgame.PolymatrixGame(**game_settings)
    #game.initiate_players(start_populations_matrix = [[300, 100], [100, 200], [200, 100]])
    game.play([0,1,0,1])
    print(game.state)
    game.play([0,1,1,1])
    print(game.state)
    print(game.network.edges)

if __name__=="__main__":
    plac.call(main)
    log.info('done {}'.format(10))