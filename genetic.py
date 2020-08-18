from corpgame import PolymatrixGame
from evaluation import *
import numpy as np
import pickle, math
import networkx as nx
import scipy
from pprint import pprint
from sklearn.metrics import mean_squared_error
import pandas as pd
df = pd.read_excel('C:/Users/Kinga/OneDrive/thesis/data/cbm/july/eurostat.xlsx', encoding='utf-8', index='country')
df = df.set_index('country')

n = len(PLAYER_LABELS)
iterations = 10 #amount of years over which the system evolves

def mutate_population(population):
    new_population = []
    population_size = len(population)   
    for k in range(0,10):       
        i = np.random.randint(0, population_size)
        j = np.random.randint(0, population_size)
        new_population.append(crossing_over(population[i],population[j]))

    for i in range(0, 5):
        new_population.append(population[i])
        new_population.append(mutate(population[i],2))

    for i, p in enumerate(population):
        new_population.append(mutate(p, i//5))
    '''
    for i, p in enumerate(new_population):
        if new_population[i]['alpha']==None:
           new_population[i] = optimize_hypothesis(new_population[i]) 
    '''

    return new_population

def create_population(amount_of_individuals, alpha_init):
    print(f"Creating {amount_of_individuals} new hypotheses")
    population = [None]*amount_of_individuals
    for i in range(amount_of_individuals):
        population[i] = create_hypothesis(alpha_init=alpha_init[i])
    return population

def create_hypothesis(alpha_init = None):
    assert type(alpha_init) == float or type(alpha_init) == None, f"genetic.create_hypothesis() Alpha_init is {alpha_init}, not float nor None"
    hypothesis = {'starting_state': None, 'strategies': None, 'alpha': None, 'error':None, 'topology':None, 'player_labels': PLAYER_LABELS}
    def create_starting_state():
        scenario = 'real' #'simulation'
        if scenario=='real':
            starting_state = np.random.randint(0, 1, (len(PLAYER_LABELS),2))
            for i, label in enumerate(PLAYER_LABELS):
                companies = df.loc[label, '2009']
                a = np.random.randint(0, companies)
                b = companies - a
                #print(label, companies,'=', a,'+', b)
                starting_state[i, :] = [a,b]
        elif scenario=='simulation':
            max_state = np.random.randint(1, 2000)
            starting_state = np.random.randint(0, max_state, (len(PLAYER_LABELS),2))
        else:
            raise ValueError(f"Unrecognized scenario {scenario}, use 'real' or 'simulation' ")
        return list(starting_state)
    hypothesis['starting_state'] = create_starting_state()
    hypothesis['strategies'] = [np.random.randint(0, 2, (1, n)) for i in range(0, iterations)]
    hypothesis['alpha'] = alpha_init
    def create_topology():
        #nodes = list(range(n))
        topology = []
        while len(topology)<18:
            topology = nx.erdos_renyi_graph(n, np.random.rand(1)).edges
        return list(topology)
    hypothesis['topology'] = create_topology()
    return hypothesis

def mutate(hypothesis, iterations):
    for i in range(iterations):
        hypothesis = mutate_player(hypothesis)
        hypothesis = mutate_graph(hypothesis)
    if iterations>0:
        hypothesis = mutate_alpha(hypothesis)
        hypothesis['error'] = None
    return hypothesis

def eval_fun(alpha, hypothesis):
    hypothesis['alpha'] = alpha
    return evaluate_edge(hypothesis) #! evaluate() for net values

def optimize_hypothesis(p):
    x0=[0.2]
    bnds = [(0.0, 1.0)]
    r = scipy.optimize.minimize(eval_fun, x0, args=p, bounds=bnds, tol=0.001)
    p['alpha'] = r['x'][0]
    p['error'] = r['fun']
    return p

def mutate_alpha(hypothesis):
    """ unused, as we are using exact solutions """
    if np.random.randint(0,3)==1:
        hypothesis['alpha']+=0.025-0.05*np.random.rand()
    if hypothesis['alpha']<=0 or hypothesis['alpha']>1:
        hypothesis['alpha']=np.random.rand()
    return hypothesis

def mutate_graph(hypothesis):
    #print(hypothesis['topology'])
    game_settings = {
            "start_populations_matrix": hypothesis['starting_state'],
            "topology": hypothesis['topology'],
            'alpha': hypothesis['alpha'],
            'player_labels': hypothesis['player_labels'],
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