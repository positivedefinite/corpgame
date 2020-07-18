from corpgame import PolymatrixGame

game = PolymatrixGame([[10,10],[20,20],[0,0]],player_labels=['Mordor','Kalimandor','Shire'])
game.play([1,0,0])
print(game.edge_payoffs)