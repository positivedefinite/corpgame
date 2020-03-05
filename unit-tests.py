import unittest
from corpgame import Game
game = Game()

class TestGame(unittest.TestCase):
    def test_class_initiation(self):
        self.assertTrue(game.__class__ is type(game))
    def test_player_generation(self):
        self.assertTrue(len(game.players)==0)

if __name__=='__main__':
    unittest.main()