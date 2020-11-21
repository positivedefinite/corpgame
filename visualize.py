import networkx as nx
import matplotlib.pyplot as plt

def draw_3player_states(payoff, pne):
    ''' Works only for 3 players! '''
    G= nx.DiGraph()
    for key in payoff:
        G.add_node(key)
    pos = {'000': [0, 0], 
           '100': [0.5,0],
           '010': [0, 0.5], 
           '110': [0.5,0.5], 
           '001': [0.3,0.3], 
           '011': [0.3,0.8], 
           '101': [0.8,0.3], 
           '111': [0.8,0.8]
          }
    node_colors = []
    for key in payoff:
        if key in pne:
            node_colors.append([0.3,1,1])
        else:
            node_colors.append([1,1,1])
    nx.draw_networkx_nodes(G, pos,
                           #nodelist=[0, 1, 2, 3],
                           node_color=node_colors,#[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0.3,1,1],[1,1,1],[0,0,0]],#'w',
                           node_size=2500,
                           alpha=0.8)
    labels = {}
    for i, key in enumerate(payoff):
        labels[key] = key+'\n'+str([i for i in payoff[key]])
    nx.draw_networkx_labels(G, pos, labels, font_size=10)
    
    #for each strategy, check if outgoing improves. If so, add edge
    for i, profile in enumerate(payoff):
        for j, strategy in enumerate(profile):
            deviation = list(profile)
            deviation[j] = str(1-int(strategy))
            deviation = ''.join(deviation)
            if payoff[profile][j]>payoff[deviation][j]:
                #print(j, profile, payoff[profile], deviation, payoff[deviation])
                G.add_edge(deviation,profile,player=j)

    cmap = {0: 'r', 1: 'g', 2: 'b'}

    for edge in G.edges():
        player = G[edge[0]][edge[1]]['player']
        #print(edge, cmap[player])
        nx.draw_networkx_edges(G, pos,
                           edgelist=[edge],
                               arrows=True,
                           width=12, edge_color=cmap[player],
                              style='dashed')

    plt.axis('off')
    plt.show()