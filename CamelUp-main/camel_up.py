#Class for Game States/Updating Game States
import random
from tent import Tent
from colorama import *
init(autoreset=True)

class GameState:
    def __init__(self):
        #This tells me the types of colors the camels can have.
        self.colors = ["green", "yellow", "red", "blue", "purple"]
        self.colors_short = ["g", "y", "r", "b", "p"]

        #This tells me the position each camel is at.
        self.camel_positions = {}

        #This tells me what the board looks like.
        self.board_camels = []
        for i in range(16):
            self.board_camels.append([])
        
        #These are the available betting tickets for each camel.
        self.available_betting_tickets = {}
        self.overall_winner = []
        self.overall_loser = []

        #These are the betting tickets each player has.
        self.player_betting_tickets = [{}, {}]

        #These are starting player scores.
        self.player_scores = [3, 3]

        # Even means p1 turn, Odd means p2 turn
        self.turn = 0

        #These are the camels that still can roll.
        self.taken_rolls = self.colors.copy()
        self.rolls = []

        #The tent is the pyramid containing the dice
        self.inital_tent = Tent()
        self.tent = Tent()
        
        #We are initializing the camel positions.
        self.initial_rolls = []
        for i in range(5):
            self.initial_rolls.append(self.inital_tent.roll())
        for roll in self.initial_rolls:
            camel_color = roll[0]
            camel_position = roll[1]
            self.camel_positions[camel_color] = camel_position - 1
            self.available_betting_tickets[camel_color] = [5, 3, 2, 2]
        
        for color in self.camel_positions:
            self.board_camels[self.camel_positions[color]].append(color)
    
    def ticketTentsString(self):
        ans = ""
        for ticket in self.available_betting_tickets:
            ticket = ticket.lower()
            length = len(self.available_betting_tickets[ticket])
            firstCard = str((self.available_betting_tickets[ticket])[0]) if length else None
            
            if ticket == "green" or ticket == "g":
                ans+= Back.GREEN + firstCard if length else Back.GREEN + "X"
            elif ticket == "yellow" or ticket == "y":
                ans += Back.YELLOW + firstCard if length else Back.YELLOW + "X"
            elif ticket == "red" or ticket == "r":
                ans += Back.RED + firstCard if length else Back.RED + "X"
            elif ticket == "blue" or ticket == "b":
                ans += Back.BLUE + firstCard if length else Back.BLUE + "X"
            elif ticket == "purple" or ticket == "p":
                ans += Back.MAGENTA + firstCard if length else Back.MAGENTA + "X"
            ans += Style.RESET_ALL + " "
        return ans + Style.RESET_ALL
    
    def movement(self, camel: str, move_number: int) -> bool:
        '''This moves stuff. I have no idea if this is right.
        Ideally this is what the code does:
        It takes the current camel and all the camels on top of the current camel
        and then it moves all of them by the move number.
        And then it updates their positions.
        '''
        old_position = self.camel_positions[camel]
        if old_position + move_number > 15:
            return False
        # print("camels", self.board_camels)
        camels_on_top = self.board_camels[old_position][self.board_camels[old_position].index(camel):].copy()
        next_position = old_position + move_number
        self.board_camels[next_position].extend(camels_on_top)
        for animal in camels_on_top:
            self.board_camels[old_position].remove(animal)
        for animal in camels_on_top:
            self.camel_positions[animal] = next_position
        return True

    def bet(self, player: int, camel_color: str) -> bool:
        '''
        Bet takes in two parameters: the player who bets, and the camel the player is betting on.
        Bet updates the gamestate to reflect the bet (e.g. modifies our betting ticket lists).
        Bet returns True if the GameState was successfully updated. Otherwise, it returns false.
        '''
        if len(self.available_betting_tickets[camel_color]) > 0:
            if camel_color in self.player_betting_tickets[player]:
                (self.player_betting_tickets[player])[camel_color].append((self.available_betting_tickets[camel_color]).pop(0))
                return True
            else:
                (self.player_betting_tickets[player])[camel_color] = [(self.available_betting_tickets[camel_color]).pop(0)]
                return True
        return False
    
    def overall(self, player, camel_color, pos):
        # pos 0 = winner
        # pos 1 = loser
        if pos == 0:
            self.overall_winner.append((player, camel_color))
        else:
            self.overall_loser.append((player, camel_color))

    def pay_out(self):
        p1 = 0
        p2 = 0
        first = ""
        second = ""
        third = ""
        fourth = ""
        fifth = ""
        for i in range(len(self.board_camels) - 1, 0, -1):
            while len(self.board_camels[i]) > 0:
                if first == "":
                    first = self.board_camels[i].pop()
                elif second == "":
                    second = self.board_camels[i].pop()
                elif third == "":
                    third = self.board_camels[i].pop()
                elif fourth == "":
                    fourth = self.board_camels[i].pop()
                elif fifth == "":
                    fifth = self.board_camels[i].pop()
            if first != "" and second != "" and third != "" and fourth != "" and fifth != "":
                break
        for bet in self.player_betting_tickets[0]:
            if bet == first:
                for num in (self.player_betting_tickets[0])[bet]:
                    p1 += num
            elif bet == second:
                for num in (self.player_betting_tickets[0])[bet]:
                    p1 += 1
            elif bet == third or bet == fourth or bet == fifth:
                for num in (self.player_betting_tickets[0])[bet]:
                    p1 -= 1
        for bet in self.player_betting_tickets[1]:
            if bet == first:
                for num in (self.player_betting_tickets[1])[bet]:
                    p2 += num
            elif bet == second:
                for num in (self.player_betting_tickets[1])[bet]:
                    p2 += 1
            elif bet == third or bet == fourth or bet == fifth:
                for num in (self.player_betting_tickets[1])[bet]:
                    p2 -= 1
        p1 += self.player_scores[0]
        p2 += self.player_scores[1]
        return (p1, p2)