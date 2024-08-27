import unittest

from camel_up import GameState

class TestGetBet(unittest.TestCase):
    def setUp(self):
        self.gamestate = GameState()
    
    def test_0(self):
        curr_size = len(self.gamestate.available_betting_tickets["purple"])
        self.gamestate.bet(1, "purple")
        updated_size = len(self.gamestate.available_betting_tickets["purple"])
        self.assertEqual(curr_size - updated_size, 1)


if __name__ == "__main__":
    unittest.main()