# make a list of all possible dice rolls
# make a copy of gamestate
# play out all the moves
# keep track of who is first, second, third, etc
# divide how many times first, second by the number of possibilities
from camel_up import GameState
from display import *
from tent import Dice
from copy import deepcopy
import itertools
import math

class ExpectedValue():
    '''
    Calculates probabilities that each camel gets first or second
    Calculates EV of each camel and betting ticket
    '''
    def __init__(self, gameState:GameState):
        self.gameState = gameState
        self.possibilities = None
    
    
    def calculate(self) -> dict[str, list[float]]:
        '''
        Calculates probabilities each camel gets first/second

        :param none
        :type none
        :rtype: dict[str, list[float]]
        :return: dictionary of each camel of their probability of getting first or second
        '''
        gameState = deepcopy(self.gameState)

        #dice is an array of strings i.e. ['purple', 'yellow']
        dice = []
        for die in gameState.tent.dices:
            dice.append(die.name)
        color_hash = {"green": 1, "yellow": 2, "red": 3, "blue": 4, "purple": 5}

        possibilities = {"green": [0.00, 0.00], "yellow": [0.00, 0.00], "red": [0.00, 0.00], "blue": [0.00, 0.00], "purple": [0.00, 0.00]}
        for process in itertools.permutations(dice):
            for i in range(243, 486, 1):
                gameState2 = deepcopy(gameState)
                minus_one_camel_moves = self.ternary(i)
                for camel in process:
                    current_move = int(minus_one_camel_moves[color_hash[camel]]) + 1
                    gameState2.movement(camel, current_move)
                placements = self.probability(gameState2)
                possibilities[placements[0]][0] += 1.00
                possibilities[placements[1]][1] += 1.00

        for key in possibilities: # divide num of times camel gets first/second by total roll possibilities
            (possibilities[key])[0] /= math.factorial(len(dice)) * pow(3, 5)
            (possibilities[key])[1] /= math.factorial(len(dice)) * pow(3, 5)

        self.possibilities = possibilities
        return possibilities
    
    
    def calculateEv(self, camel: str, possibilities):
        '''
        Calculates EV of specific camel

        :param camel: camel color, possibilities: probability of camel getting first/second
        :type camel: str, possibilities: dict{str: [int, int]}
        :rtype: float
        :return: EV of specific camel
        '''
        pFirst = possibilities[camel][0]
        pSecond = possibilities[camel][1]
        if len(self.gameState.available_betting_tickets[camel]) == 0:
            return 0 - math.inf
        return self.gameState.available_betting_tickets[camel][0] * pFirst + 1 * pSecond  - 1 * (1 - pFirst - pSecond)
    
    
    def ternary(self, n):
        '''
        Converts n to base 3

        :param n: number in base 10 to be turned into base 3
        :type n: int
        :rtype: int
        :return: n as base 3
        '''
        if n == 0:
            return '0'
        nums = []
        while n:
            n, r = divmod(n, 3)
            nums.append(str(r))
        return ''.join(reversed(nums))
    
    def probability(self, gameState:GameState) -> list[str]:
        '''
        Calculates the order of first, second, third, etc

        :param gameState: current game state
        :type gameState: GameState
        :rtype: list[str]
        :return: list of order of first, second, third, etc
        '''

        # returns a list in order of first, second, third, etc
        first = ""
        second = ""
        third = ""
        fourth = ""
        fifth = ""
        for i in range(len(gameState.board_camels) - 1, 0, -1):
            while len(gameState.board_camels[i]) > 0:
                if first == "":
                    first = gameState.board_camels[i].pop()
                elif second == "":
                    second = gameState.board_camels[i].pop()
                elif third == "":
                    third = gameState.board_camels[i].pop()
                elif fourth == "":
                    fourth = gameState.board_camels[i].pop()
                elif fifth == "":
                    fifth = gameState.board_camels[i].pop()
            if first != "" and second != "" and third != "" and fourth != "" and fifth != "":
                break
        placements = [first, second, third, fourth, fifth]
        return placements