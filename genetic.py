from corpgame import PolymatrixGame
import numpy as np
import pickle, math
import networkx as nx

import pandas as pd
df = pd.read_excel('C:/Users/Kinga/OneDrive/thesis/data/cbm/july/eurostat.xlsx', encoding='utf-8', index='country')
df = df.set_index('country')

df_true = pd.read_csv('C:/Users/Kinga/OneDrive/thesis/data/cbm/payoffs.csv')
countries = list(df_true['Unnamed: 0'])
y_true = df_true.drop(columns='Unnamed: 0').values

from sklearn.metrics import mean_squared_error
n = len(countries)
iterations = 10 #amount of years over which the system evolves
player_labels = countries

def mutate_population(population):
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
    memory = {'starting_state': None, 'strategies': None, 'alpha': None, 'error':None, 'topology':'fully_connected', 'player_labels': player_labels}
    for i in range(0, amount):
        # 1. Amount of companies
        scenario = 'real' #'simulation'
        if scenario=='real':
            starting_state = np.random.randint(0, 1, (len(player_labels),2))
            for i, label in enumerate(player_labels):
                companies = df.loc[label, '2009']
                a = np.random.randint(0, companies)
                b = companies - a
                #print(label, companies,'=', a,'+', b)
                starting_state[i, :] = [a,b]
        else: 
            max_state = np.random.randint(1, 2000)
            starting_state = np.random.randint(0, max_state, (len(player_labels),2))
        strategies = [np.random.randint(0, 2, (1, n)) for i in range(0, iterations)]
        alpha = 0
        while alpha<0.001:
            alpha = float(np.random.rand(1))/3
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
        #random
        topology = []
        while len(topology)<18:
            topology = nx.erdos_renyi_graph(n,np.random.rand(1)).edges
        #print(type(topology), topology)
        memory['topology'] = list(topology)
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
            "player_labels": hypothesis['player_labels'],
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