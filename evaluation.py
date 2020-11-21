from corpgame import PolymatrixGame
from evaluation import *
import numpy as np
import pickle, math
import networkx as nx
import scipy
from pprint import pprint
from sklearn.metrics import mean_squared_error
import pandas as pd

df_true = pd.read_csv('C:/Users/Kinga/OneDrive/thesis/data/cbm/payoffs.csv')
PLAYER_LABELS = list(df_true['Unnamed: 0'])
# old way of using net node values for y_true
y_net_true = df_true.drop(columns='Unnamed: 0').values

edge_data = pickle.load(open('C:/Users/Kinga/OneDrive/thesis/data/corpgame/real_edge_payoff.pickle','rb'))
y_edge_true = [edge_data[edge] for edge in edge_data]

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
        payoff = game.payoff_matrix.sum(axis=1).transpose().reshape(len(game.players), 1)
        outcomes.append(payoff)
    y_net_pred = np.hstack(outcomes)
    err = math.sqrt(mean_squared_error(y_net_true, y_net_pred))
    return err

def evaluate_edges_error(hypothesis):
    strategies = hypothesis['strategies']
    game_settings = {
        "start_populations_matrix": hypothesis['starting_state'],
        "topology": hypothesis['topology'],
        "player_labels": hypothesis['player_labels'],
        'alpha': hypothesis['alpha'],
        'log_level': "warning"
    }
    game = PolymatrixGame(**game_settings)
    baselines = []
    E = []
    average_per_year = [0.2037037037037037,
        0.2934472934472934,
        0.37464387464387466,
        0.4415954415954416,
        0.5042735042735043,
        0.42165242165242167,
        0.35185185185185186,
        0.2962962962962963,
        0.43874643874643876,
        0.5854700854700855,
        0.5868945868945868] # computed from real-world dataset of CBM per year, each entry is year's average per edge
    for iteration, strategy in enumerate(strategies):
        #print(strategy[0])
        game.play(strategy[0])
        game.get_directed_payoffs()
        predicted_edge_data = game.directed_edge_payoffs
        y_edge_pred = [predicted_edge_data[edge] for edge in predicted_edge_data]
        baselines.append(mean_squared_error(y_edge_true[iteration], [average_per_year[iteration]]*702))
        err = math.sqrt(mean_squared_error(y_edge_true[iteration], y_edge_pred))
        E.append(err)
        #zip(baselines, E)
    return E, baselines

def evaluate_edge(hypothesis):
    """ Wrapper for edge evaluation to return only scalar average result """
    E, _ = evaluate_edges_error(hypothesis)
    return sum(E)/len(E)