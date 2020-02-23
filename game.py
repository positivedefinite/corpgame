import plac, corpgame
from logger import log

@plac.annotations(
    start=("Some starting parameter","option","s", str)
    )
    
def main(start='ok'):
    print(start)

if __name__=="__main__":
    plac.call(main)
    log.info('done {}'.format(10))