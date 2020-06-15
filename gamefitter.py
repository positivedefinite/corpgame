from corpgame import PolymatrixGame
import numpy as np
import pickle, math

y_true=np.array([[-14, -12,   1,   0,   6,   7,  27,  -6, -13, -14],
       [  1,   4,   8,   6,   7,  31, -24, -22, -16,   2],
       [ 27,  27,  24,  16,  14,  17,  15,  30,  73,  28],
       [ 11,  11,  24,  12,  15,   0,   7,   9, -11,  11],
       [  2,   2,  -1,  11,  -9,   7,  -6,  -3, -12,  -2],
       [ -8,  -8, -11,  14,  20,  -4,  -5,  -1, -30,  -8],
       [-12, -12, -10, -28, -40, -25,  -1,  -7, -17, -12],
       [ 12,  12,   7,   3,   9,  11,  13,  14,  14,  13],
       [ -2,  -2,  -3,  -3,   7,   3,   1,   9,   8,  -2],
       [ 11,   9,   9,   8,  14,   2,  12,  16,  12,  11],
       [ -5,  -4,  -3,  -2, -15,  -8,  -2,  -8, -10,  -4],
       [ -7,  -7,  -1,  -3,  -8,  -2,  -1, -12,   0,  -6],
       [  4,   3,   2,   0,   6,  -4,   3,   5,   2,   2],
       [ -4,  -4,  -4,  -4,   2,  -2,  -4,  -3,  -8,  -4],
       [ -2,  -2, -11, -12, -12, -16, -18, -10,   1,  -2],
       [ -2,  -5, -22,  -9,  -9, -10, -11,  -7,   2,  -3],
       [ -2,  -2,  -2,  -2,   0,   2,   0,  10,  10,   0],
       [-10, -10,  -7,  -7,  -7,  -9,  -6, -14,  -5, -10]])

from sklearn.metrics import mean_squared_error

n = 18
iterations = 10

def mutate_population(population):
    entry_size = len(population)
    new_population = []
    for k in range(0,10):
        i = np.random.randint(0, 50)
        j = np.random.randint(0, 50)
        new_population.append(crossing_over(population[i],population[j]))

    for i in range(0, 5):
        new_population.append(population[i])
        new_population.append(mutate(population[i],2))

    for i in range(5, 10):
        new_population.append(mutate(population[i],1))
    
    for i in range(10, 20):
        new_population.append(mutate(population[i],2))

    for i in range(20, 35):
        new_population.append(mutate(population[i],3))

    for i in range(35, 40):
        new_population.append(mutate(population[i],4))

    for i in range(40, 45):
        new_population.append(mutate(population[i],5))

    return new_population

def create_population(amount):
    new_population = []
    memory = {'starting_state': None, 'strategies': None, 'alpha': None, 'error':None, 'topology':'fully_connected'}
    for i in range(0, amount):
        max_state = np.random.randint(1, 2000)
        starting_state = np.random.randint(0, max_state, (n,2))
        strategies = [np.random.randint(0, 2, (1, n)) for i in range(0, iterations)]
        alpha = float(np.random.rand(1))
        
        memory['starting_state'] = list(starting_state)
        memory['strategies'] = strategies
        memory['alpha'] = alpha
        nodes = list(range(n))
        #fully_connected
        memory['topology'] = [
                    [nodes[i], nodes[j]]
                    for i in range(len(nodes))
                    for j in range(i + 1, len(nodes))
                ]
        #chain
        memory['topology'] = [[nodes[i - 1], nodes[i]] for i in range(1, len(nodes))]
        new_population.append(memory.copy())
    return new_population

def mutate(hypothesis, iterations):
    for i in range(iterations):
        p = mutate_player(hypothesis)
        p = mutate_graph(p)
        p = mutate_alpha(p)
    return p

def mutate_alpha(hypothesis):
    if np.random.randint(0,3)==1:
        hypothesis['alpha']+=0.05-0.1*np.random.rand()
    if hypothesis['alpha']<=0 or hypothesis['alpha']>1:
        hypothesis['alpha']=np.random.rand()
    return hypothesis

def mutate_graph(hypothesis):
    #print(hypothesis['topology'])
    game_settings = {
            "start_populations_matrix": hypothesis['starting_state'],
            "topology": hypothesis['topology'],
            'alpha': hypothesis['alpha'],
            'log_level': "warning"
        }
    game = PolymatrixGame(**game_settings)
    chance = True
    while chance:
        if np.random.randint(0,2)==0:
            if len(game.network.edges)>(len(game.players)-1):
                game.network.remove_random_edge()
                hypothesis['topology'] = list(game.network.edges)
        else:
            game.network.add_random_edge()
        if np.random.randint(0,2)==1:
            chance = False
    return hypothesis

def mutate_player(hypothesis):
    p = hypothesis.copy()
    mutation_location = np.random.randint(0, len(p['starting_state']))
    loc = np.random.randint(0,2)
    state_mutation_value = int(np.random.randint(-10, 10)/30*p['starting_state'][mutation_location][loc])
    state = p['starting_state'][mutation_location][loc]
    if state>=-state_mutation_value: #only subtract if it won't create a negative value
        p['starting_state'][mutation_location][loc]+=state_mutation_value
    for i, s in enumerate(p['strategies']):
        if np.random.randint(0,2)>0:
            #print(p['strategies'][i])
            p['strategies'][i][0][mutation_location]=1-p['strategies'][i][0][mutation_location]
    p['error']=None
    return p

def evaluate(hypothesis):
        strategies = hypothesis['strategies']
        game_settings = {
            "start_populations_matrix": hypothesis['starting_state'],
            "topology": hypothesis['topology'],
            'alpha': hypothesis['alpha'],
            'log_level': "warning"
        }
        game = PolymatrixGame(**game_settings)
        outcomes = []
        for iteration, strategy in enumerate(strategies):
            strategy = strategy[0]
            game.play(strategy)
            payoff = game.payoff_matrix.sum(axis=1).transpose().reshape(n,1)
            outcomes.append(payoff)
        y_pred = np.hstack(outcomes)
        err = math.sqrt(mean_squared_error(y_true, y_pred))
        return err

def remove_clones(sorted_populations):
    clean_populations = []
    i = 0
    clean_populations.append(sorted_populations[i])
    i += 1
    while i<len(sorted_populations)-1:
        if sorted_populations[i-1]['error']!=sorted_populations[i]['error'] and sorted_populations[i-1]['alpha']!=sorted_populations[i]['alpha']:
            clean_populations.append(sorted_populations[i])
        i += 1
    return clean_populations

def crossing_over(p1, p2):
    p3 = p1.copy()
    p3['error']=None
    z = zip(p1['starting_state'],p2['starting_state'])
    p3['starting_state']=[np.array((int((b[0][0]+b[1][0])/2),int((b[0][1]+b[1][1])/2))) for b in z]
    p3['alpha']=(p1['alpha']+p2['alpha'])/2
    #print(p1['topology'],p2['topology'])
    s1 = set([tuple(p) for p in p1['topology']])
    s2 = set([tuple(p) for p in p2['topology']])
    intersection = s1.intersection(s2)
    unique_s1 = s1.difference(intersection)
    unique_s2 = s2.difference(intersection)
    candidate_edges = unique_s1.union(unique_s2)
    chosen_edges = []
    for edge in candidate_edges:
        if np.random.randint(0,2)==1:
            chosen_edges.append(edge)
    p3['topology'] = list(intersection.union(set(chosen_edges)))
    for i, sv in enumerate(p3['strategies']):
        for j, s in enumerate(sv):
            if p3['strategies'][i][0][j]!=p2['strategies'][i][0][j]:
                p2['strategies'][i][0][j]=np.random.randint(0,2)
    return p3


import plac, corpgame
from logger import log

@plac.annotations(number_of_individuals=("Amount of players", "option", "n", int),
                    experiment_name=("Experiment name", "option", "name", str))
def main(number_of_individuals=50, experiment_name="chainX"):
    best = 1000
    max_pops = number_of_individuals
    population = create_population(number_of_individuals)
    #population = pickle.load(open('./data/optimization/population_chain_1_10.10.pickle','rb'))
    #population = [population[i] for i in [0,2,6,14]]
    pairs = [
                    [i, j]
                    for i in range(4)
                    for j in range(i + 1, 4)
                ]
    #population.extend([crossing_over(population[p1],population[p2]) for (p1,p2) in pairs])
    #population.extend(create_population(max_pops-len(population)))
    #population = [mutate(p,2) for p in population]

    while True:
        print('1. Evaluating')
        for i, p in enumerate(population):
            if i%5==0:
                print(f"{i}/{len(population)}")
            if population[i]['error'] == None:
                population[i]['error'] = evaluate(p)
        print('2. Sorting')
        population.sort(key=lambda x: x['error'])
        print('TOP 10 Error rates:')
        for i, p in enumerate(population[0:10]):
            print(i, p['error'])
        if best!=population[0]['error']:
            best = population[0]['error']
            pickle.dump(population, open(f'./data/optimization/population_{experiment_name}_{str(best)[0:5]}.pickle','wb'))
        
        population = remove_clones(population)
        population.pop(np.random.randint(3,(len(population)))) #random killing
        print('3. Expanding')
        population = population[0:45]
        if len(population)<max_pops:
            population.extend(create_population(max_pops-len(population)))
        

        
        
        population = mutate_population(population)
        
        print()
if __name__ == "__main__":
    plac.call(main)
    
