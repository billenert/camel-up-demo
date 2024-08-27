from camel_up import GameState
from tent import *
from colorama import *
init(autoreset=True)

class Display:
    '''
    Takes in info from GameState and prints to terminal for user to read
    '''
        
    def toColor(self, color, index):
        '''
        Prints the camels out with the first letter of their color and background of their color

        :param: color: camel color, index: position of camel
        :type: color: str, index: int
        :rtype: str
        :return: camel as a string
        '''
        color = color.lower()
        empty = "   "
        spaces = "  "
        if index >= 9:
            empty = "    "
            spaces = "   "
        if color == "":
            return empty
        if color == "green" or color == "g":
            return Back.GREEN + "g" + Style.RESET_ALL + spaces
        elif color == "yellow" or color == "y":
            return Back.YELLOW + "y" + Style.RESET_ALL + spaces
        elif color == "red" or color == "r":
            return Back.RED + "r" + Style.RESET_ALL + spaces
        elif color == "blue" or color == "b":
            return Back.BLUE + "b" + Style.RESET_ALL + spaces
        elif color == "purple" or color == "p":
            return Back.MAGENTA + "p" + Style.RESET_ALL + spaces
        
    def printCamels(self, level):
        '''
        Prints all the camels out according to their board position

        :param: level: tracks camels that are stacked on top of each other
        :type level: list[str]
        :rtype: nothing
        :return: nothing
        '''
        tree = '🌴'
        flag = '🏁'
        print(f"{tree}{self.toColor(level[0], 0)}{self.toColor(level[1], 1)}{self.toColor(level[2], 2)}{self.toColor(level[3], 3)}{self.toColor(level[4], 4)}{self.toColor(level[5], 5)}{self.toColor(level[6], 6)}{self.toColor(level[7], 7)}{self.toColor(level[8], 8)}{self.toColor(level[9], 9)}{self.toColor(level[10], 10)}{self.toColor(level[11], 11)}{self.toColor(level[12], 12)}{self.toColor(level[13], 13)}{self.toColor(level[14], 14)}{self.toColor(level[15], 15)}|{flag}")
    
    def betsToColor(self, color, num):
        '''
        Converts players tickets to how much the ticket was and the color

        :param color: camel color, num: how much the ticket was
        :type color: str, num: int
        :rtype: str
        :return: string of player ticket
        '''
        color = color.lower()
        if color == "green" or color == "g":
            return Back.GREEN + str(num) + Style.RESET_ALL
        elif color == "yellow" or color == "y":
            return Back.YELLOW + str(num) + Style.RESET_ALL
        elif color == "red" or color == "r":
            return Back.RED + str(num) + Style.RESET_ALL
        elif color == "blue" or color == "r":
            return Back.BLUE + str(num) + Style.RESET_ALL
        elif color == "purple" or color == "p":
            return Back.MAGENTA + str(num) + Style.RESET_ALL
    
    def printBets(self, bets):
        '''
        Converts all player bets to string

        :param bets: all the player bets
        :type bets: list[str]
        :rtype: str
        :return: player bets as a string
        '''
        if bets == None:
            return ""
        
        ans = ""
        for color in bets:
            for num in bets[color]:
                ans += self.betsToColor(color, num) + " "
        
        return ans
    
    def game_display(self, gameState:GameState):
        '''
        Main function for display. Prints out tickets, dice tents, camel positions, player scores, and player bets

        :param gameState: current game state
        :type gameState: GameState
        :rtype: nothing
        :return: nothing
        '''
        Style.RESET_ALL
        print(f"Ticket Tents: {gameState.ticketTentsString()} Dice Tents: {gameState.tent}")

        # calculates stacks of camels
        level1 = [""] * 16
        level2 = [""] * 16
        level3 = [""] * 16
        level4 = [""] * 16
        level5 = [""] * 16
        index = 0
        for list in gameState.board_camels:
            if len(list) > 4:
                level5[index] = list[4]
            if len(list) > 3:
                level4[index] = list[3]
            if len(list) > 2:
                level3[index] = list[2]
            if len(list) > 1:
                level2[index] = list[1]
            if len(list) > 0:
                level1[index] = list[0]
            index += 1
        self.printCamels(level5)
        self.printCamels(level4)
        self.printCamels(level3)
        self.printCamels(level2)
        self.printCamels(level1)
        print("  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16")
        print(f"p1 has {gameState.player_scores[0]} coins. Bets: {self.printBets(gameState.player_betting_tickets[0])}             p2 has {gameState.player_scores[1]} coins. Bets: {self.printBets(gameState.player_betting_tickets[1])}")
    
        
    