import unittest
from camel_up import *
from expected_value import *


class TestEV(unittest.TestCase):
    def setUp(self):
        self.gamestate = GameState()
        self.ev = ExpectedValue(self.gamestate)
    
    def test_0(self):
        actual = self.ev.calculate()
        self.assertIsInstance(actual, dict)
    
    def test_1(self):
        possibilities = self.ev.calculate()
        actual = self.ev.calculateEv("green", possibilities)
        self.assertIsInstance(actual, float)
    
    def test_2(self):
        actual = self.ev.ternary(4)
        self.assertEqual(int(actual), 11)
    
    def test_3(self):
        actual = self.ev.ternary(4)
        self.assertIsInstance(actual, str)
    

if __name__ == "__main__":
    unittest.main()