import unittest
from camel_up import GameState
from tent import Tent


class TestTent(unittest.TestCase):
    def setUp(self):
        self.gameState = GameState()
        self.tent = Tent()

    def test_0(self):
        actual = self.tent.roll()
        self.assertIsInstance(actual, tuple)
    
    def test_1(self):
        actual = self.tent.roll()
        self.assertTrue(actual[1] > 0)
    
    def test_2(self):
        actual = self.tent.roll()
        self.assertTrue(actual[1] < 4)
    
    def test_3(self):
        actual = self.tent.roll()
        self.assertTrue(actual[0] in self.gameState.colors)

if __name__ == "__main__":
    unittest.main()