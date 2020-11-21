import pickle
from collections import defaultdict
import itertools
import pandas as pd
class Population():
    def __init__(self, path_to_pickle):
        self.list = pickle.load(open(path_to_pickle,'rb'))
        print(len(self.list))
    def sort(self):
        sorted(self.list, key=lambda x: x['error'])
    def print_errors(self):
        print([p['error'] for p in self.list])

    def to_dict(self):
        alldict = defaultdict()
        print(f"Turning {len(self.list)} record to dictionary")
        for k, p in enumerate(self.list):
            instance = defaultdict()
            instance['nonzero']=p['error']!=11.056420959987207 #!
            instance['error']=p['error']
            instance['alpha']=p['alpha']
            state = defaultdict()
            for i, arr in enumerate(p['starting_state']):
                for j, arg in enumerate(arr):
                    state[f"state_{i}_{j}"]=arg
            strategies = defaultdict()
            for i, arr in enumerate(p['strategies']):
                for j, arg in enumerate(arr[0]):
                    strategies[f"strategy_{i}_{j}"]=arg
            f = itertools.combinations(list(range(27)),2)
            topology = defaultdict()
            for e in f:
                topology[f"{e}"]=0
            for i, tup in enumerate(p['topology']):
                topology[f"{tup}"]=1
            instance.update(state)
            instance.update(strategies)
            instance.update(topology)
            alldict[k] = instance.values()
        self.dict = alldict
        self.columns = list(instance.keys())
        return alldict
    def to_df(self):
        self.to_dict()
        self.df = pd.DataFrame.from_dict(self.dict, orient='index', columns=self.columns)
        return self.df

population = Population('./data/optimization/population_random_edges_1.571.pickle')
#population.sort()
#population.print_errors()
population.to_df()
print(population.df)
