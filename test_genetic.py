from genetic import *
import time
populations = []
best = 12
T = []
counter = 0
while True:
    counter+=1
    t0 = time.time()
    p = create_hypothesis()
    x0=[0.1]
    bnds = [(0.0, 1.0)] 
    r = scipy.optimize.minimize(eval_fun, x0, args=p, bounds=bnds, tol=0.001)
    p['alpha'] = r['x'][0]
    p['error'] = r['fun']
    if p['error']<best:
        best = p['error']
    t = time.time() - t0
    T.append(t)
    print(f"{r['fun']} for alpha={r['x'][0]} in time {t} and mean time {sum(T)/counter} and total time {sum(T)} while best = {best} ")
    populations.append(p)
    pickle.dump(populations, open(f'./data/optimization/population_random_{str(best)[0:5]}.pickle','wb'))