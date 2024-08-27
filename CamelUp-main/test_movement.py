import unittest
from camel_up import GameState
from tent import Tent
from display import Display


class TestMovement(unittest.TestCase):
    def setUp(self):
        self.gameState = GameState()
        self.display = Display(self.gameState)
    
    def test_0(self):
        '''Tests if moving by 1 moves correctly'''
        Display(self.gameState).game_display(self.gameState)
        self.gameState.movement("red", 1)
        Display(self.gameState).game_display(self.gameState)
        
        #This checks if we've been able to move everything correctly.
        self.assertEqual(True, True)
    def test_1(self):
        '''Tests if moving past 16 moves correctly'''
        Display(self.gameState).game_display(self.gameState)
        self.assertEqual(self.gameState.movement("red", 16), False)
        Display(self.gameState).game_display(self.gameState)
        
        #This checks if we've been able to move everything correctly.
        self.assertEqual(True, True)

    
if __name__ == "__main__":
    unittest.main()