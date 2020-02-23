import plac, corpgame

@plac.annotations(
    start=("Some starting parameter","option","s", str)
    )
def main(start='ok'):
    print(start)

if __name__=="__main__":
    plac.call(main)