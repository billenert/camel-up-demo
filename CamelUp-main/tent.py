
import random
from colorama import *
init(autoreset=True)

'''
Used if player chooses to roll the dice
'''
class Tent:
    def __init__(self) -> None:
        green = Dice("green")
        yellow = Dice("yellow")
        red = Dice("red")
        blue = Dice("blue")
        purple = Dice("purple")
        self.dices = [green, yellow, red, blue, purple]
        self.rolls = []
    
    def roll(self):
        '''
        Rolls dice left in the pyramid

        :param none
        :type none
        :rtype: tuple(str, int)
        :return: tuple of the color of dice rolled and number the dice rolled
        '''
        dice = random.choice(self.dices)
        color = dice.name
        roll = dice.getRandomNumber()
        self.dices.remove(dice)
        self.rolls.append(dice)
        return (color, roll)

    def __str__(self):
        '''
        Converts the dice rolled into a string

        :param none
        :type none
        :rtype: str
        :return: dice rolled as string
        '''
        ans = ""
        for dice in self.rolls:
            if dice.name == "green":
                if dice.number != None:
                    ans += Back.GREEN + str(dice.number)
            elif dice.name == "yellow":
                if dice.number != None:
                    ans += Back.YELLOW + str(dice.number)
            elif dice.name == "red":
                if dice.number != None:
                    ans += Back.RED + str(dice.number)
            elif dice.name == "blue":
                if dice.number != None:
                    ans += Back.BLUE + str(dice.number)
            elif dice.name == "purple":
                if dice.number != None:
                    ans += Back.MAGENTA + str(dice.number)
            ans += Style.RESET_ALL + " "
        return ans

class Dice:
    def __init__(self, name, number = None) -> None:
        self.name = name
        self.number = number
    def getRandomNumber(self):
        value = random.randint(1,3)
        self.number = value
        return value