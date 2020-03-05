import unittest
from corpgame import Game
from player import Player
game = Game()
class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(population_vector=[1,2], index=1)
    def test_player_history(self):
        self.assertTrue(self.player.history==[])

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_object_instantiation(self):
        self.assertTrue(
            self.game != None, "Game was not instantiated so self.game==None"
        )

    def test_class_type(self):
        self.assertTrue(
            str(self.game.__class__) == "<class 'corpgame.Game'>",
            "Type of object is not <class 'corpgame.Game'>",
        )

    def test_game_empty(self):
        self.assertTrue(
            len(self.game.players) == 0, "In empty game there are not 0 players."
        )

    def test_game_state(self):
        self.assertTrue(
            self.game.initiate_players(start_populations_matrix=[[3, 0], [1, 2], [2, 1]]),
            "Player initiation failed",
        )


if __name__ == "__main__":
    unittest.main()
