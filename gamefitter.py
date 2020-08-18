from genetic import *
import plac, corpgame
from logger import log

@plac.annotations(number_of_individuals=("Amount of players", "option", "n", int),
                    experiment_name=("Experiment name", "option", "name", str))
def main(number_of_individuals=50, experiment_name="edgeval7"):
    print(f"True payoff matrix:\n{df_true}")
    best = 1000
    max_pops = number_of_individuals
    alpha_init = [0.05 + np.random.rand()/5 for i in range(number_of_individuals)]
    population = create_population(number_of_individuals, alpha_init)
    #population = pickle.load(open('./data/optimization/population_bigpops_exact_1_10.91.pickle','rb'))
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
                population[i]['error'] = evaluate_edge(p)
        print('2. Sorting')
        population.sort(key=lambda x: x['error'])
        print('TOP 10 Error rates:')
        for i, p in enumerate(population[0:10]):
            print(f"{i} {p['error']} for alpha {p['alpha']} and {len(p['topology'])} edges"    )
        if best!=population[0]['error']:
            best = population[0]['error']
            pickle.dump(population, open(f'./data/optimization/population_{experiment_name}_{str(best)[0:5]}.pickle','wb'))
        
        population = remove_clones(population)
        #population.pop(np.random.randint(3,(len(population)))) #random killing
        print('3. Expanding')
        population = population[0:45]
        if len(population)<max_pops:
            population.extend(create_population(max_pops-len(population), alpha_init = [0.05 + np.random.rand()/5 for i in range(max_pops-len(population))]))
        population = mutate_population(population)
        
        print()
if __name__ == "__main__":
    plac.call(main)
    
