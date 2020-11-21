import pickle
from collections import defaultdict
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import math

edge_data = pickle.load(open('C:/Users/Kinga/OneDrive/thesis/data/corpgame/real_edge_payoff.pickle','rb'))

amount_of_edges = len(edge_data[2008])

# first, construct a dictionary that holds a list of annual values per edge
d = {i:list([]) for i in range(amount_of_edges)}
for i in range(amount_of_edges):
    l = []
    for year in edge_data:
        l.append(edge_data[year][i])
    d[i] = l

from sklearn import tree
from sklearn.ensemble import *
#https://scikit-learn.org/stable/modules/ensemble.html#voting-regressor
method = LinearRegression


import time
# then use those small timeseries per edge to fit linear models 
rmses = []
for j, year in enumerate(range(2008, 2019)):
    errors = []
    for edge in d:
        x = np.array(range(2008, 2019)).reshape(-1, 1)
        y=np.array(d[edge])
        
        #method = tree.DecisionTreeRegressor(max_depth = 2)
        #method = GradientBoostingRegressor(random_state=1, n_estimators=10)
        method = RandomForestRegressor(random_state=1, n_estimators=10)
        reg = method.fit(x, y)
        y_true = np.array(d[edge][j])
        y_pred = reg.predict(np.array([[year]]))
        #print(edge, x, y, reg.coef_, year, y_pred, y_true)
        error = (y_pred-y_true)**2
        errors.append(error)
        #print(edge, y_true, y_pred, error)
    rmse = math.sqrt(sum(errors)/amount_of_edges)
    rmses.append(rmse)
    print(f'Year: {year}, RMSE: {rmse}')
print('RMSE for all years together: ', sum(rmses)/len(rmses))