from camel_up import GameState
from display import Display
from expected_value import ExpectedValue
from colorama import *
import math
from copy import deepcopy

def scores_calculator(index) -> int:
    '''
    Calculates how much to add for overall winner/loser bets

    :param index: determines how many points to gain/lose
    :type index: int
    :rtype: int
    :return: how much a player gains/loses
    '''
    score = 0
    if index == 0:
        score += 8
    elif index == 1:
        score += 5
    elif index == 2:
        score += 3
    elif index == 3:
        score += 2
    else:
        score += 1
    return score

def overall_calculator(overall, end):
    '''
    Calculates total points p1/p2 gets for overall winner/loser

    :param overall: the bets placed on overall winner/loser, end: order of camels in first, second, third, etc
    :type overall: dict{int: str}, end: list[str]
    :rtype: tuple(int, int)
    :return: tuple of p1 and p2 scores from bets on overall winner/loser
    '''
    p1 = 0
    p2 = 0
    for index in range(len(overall)):
            if overall[index][1] == end[0]:
                if overall[index][0] == 0:
                    p1 += scores_calculator(index)
                else:
                    p2 += scores_calculator(index)
            else:
                if overall[index][0] == 0:
                    p1 -= 1
                else:
                    p2 -= 1
    return (p1, p2)

def ai_advice(gameState:GameState):
    '''
    Calculates the expected value and probabilities for the passed in game state

    :param gameState: current game state
    :type gameState: GameState
    :rtype: nothing
    :return: nothing
    '''
    enumerative = ExpectedValue(gameState).calculate()
    print("AI Advice-")
    print("   1st   2nd")

    # prints probabilities
    for camel in enumerative:
        if camel == "green":
            ans = Back.GREEN + "g" + Style.RESET_ALL
        elif camel == "blue":
            ans = Back.BLUE + "b" + Style.RESET_ALL
        elif camel == "yellow":
            ans = Back.YELLOW + "y" + Style.RESET_ALL
        elif camel == "purple":
            ans = Back.MAGENTA + "p" + Style.RESET_ALL
        elif camel == "red":
            ans = Back.RED + "r" + Style.RESET_ALL
        first = round((enumerative[camel])[0], 2)
        second = round((enumerative[camel])[1], 2)
        ans += "  %3.2f" %(first)
        ans += "  %3.2f" %(second)
        print(ans)
    
    ans = "Available betting tickets:"
    
    # calculuates evs
    evs = {}
    
    max_ev = -1 * math.inf
    
    for camel in enumerative:
        if len(gameState.available_betting_tickets[camel]) > 0:
            ev = round(ExpectedValue(gameState).calculateEv(camel, enumerative), 2)
            evs[camel] = ev
            if ev > max_ev:
                max_ev = ev
            
    for camel in evs:
        if camel == "green":
            ans += " (g)" + Back.GREEN
        elif camel == "blue":
            ans += " (b)" + Back.BLUE
        elif camel == "yellow":
            ans += " (y)" + Back.YELLOW
        elif camel == "purple":
            ans += " (p)" + Back.MAGENTA
        elif camel == "red":
            ans += " (r)" + Back.RED
        ans += str(gameState.available_betting_tickets[camel][0]) + Style.RESET_ALL
        if evs[camel] == max_ev and max_ev >= 1:
            ans += " " + Fore.GREEN + Back.WHITE + "EV:%.2f" %(evs[camel]) + Style.RESET_ALL
        else:
            ans += " EV:%.2f" %(evs[camel])
        
    print(ans)
    print()
    
def placements(gameState:GameState) -> list[str]:
    '''
    Determines who is first, second, third, etc

    :param gameState: current game state
    :type gameState: GameState
    :rtype: list[str]
    :return: list in order of first, second, third, etc
    '''
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

if __name__ == "__main__":
    # tracks overall info
    leg = 1
    p1 = 0
    p2 = 0

    mode = input("Do you want auto AI advice? (y/n) ") # auto: output EV every turn, non-auto: output EV if ticketing
    print()

    # tracks info between legs
    starting_positions = {} 
    board_positions = []

    end = False # if camel not past 16th position
    turn = 0 # even = p1 move, odd = p2 move
    
    while not end:
        gameState = GameState()
        if leg > 1: # maintain positions of camels between legs
            gameState.camel_positions = deepcopy(starting_positions)
            gameState.board_camels = deepcopy(board_positions)
        display = Display()
        print()
        display.game_display(gameState)
        while len(gameState.tent.dices) > 0: # each leg
            if mode == "y":
                ai_advice(gameState)
            restart = False # if player decides to not ticket anymore after choosing to ticket
            move = ""
            while move != "b" and move != "r" and move != "t":
                if turn % 2 == 0: # p1 turn
                    move = input("p1 - (T)icket or (R)oll or (B)et? ")
                    move = move.lower()
                    print()
                else: # p2 turn
                    move = input("p2 - (T)icket or (R)oll or (B)et? ")
                    move = move.lower()
                    print()

            if move == "r": # roll
                roll = gameState.tent.roll()
                if not gameState.movement(roll[0], roll[1]):
                    end = True
                    break
                gameState.player_scores[turn % 2] += 1
            elif move == "t": # ticket
                if mode == "n":
                    ai_advice(gameState)
                bet = ""
                length = 1
                while True:
                    bet = input("What color do you want to bet on or (n) to not bet. ")
                    if bet == "n":
                        restart = True
                        break
                    if bet in gameState.colors or bet in gameState.colors_short:
                        if bet == "g":
                            bet = "green"
                        elif bet == "y":
                            bet = "yellow"
                        elif bet == "p":
                            bet = "purple"
                        elif bet == "b":
                            bet = "blue"
                        elif bet == "r":
                            bet = "red"
                        if gameState.bet(turn % 2, bet):
                            break
                    print()
            elif move == "b": # bet
                camel_color = ""
                pos = ""
                while True:
                    bet = input("Which camel do you want to bet on and winner or loser? (color, w/l) ")
                    if len(bet.split(",")) >= 2:
                        camel_color = bet.split(",")[0].strip()
                        pos = bet.split(",")[1].strip()
                        if camel_color == "g":
                            camel_color = "green"
                        elif camel_color == "y":
                            camel_color = "yellow"
                        elif camel_color == "p":
                            camel_color = "purple"
                        elif camel_color == "b":
                            camel_color = "blue"
                        elif camel_color == "r":
                            camel_color = "red"
                        if pos == "w":
                            pos = 0
                        elif pos == "l":
                            pos = 1
                        move = (turn % 2, camel_color)
                        if pos == 0:
                            if move not in gameState.overall_winner and camel_color in gameState.colors:
                                break
                        elif pos == 1:
                            if move not in gameState.overall_loser and camel_color in gameState.colors:
                                break
                gameState.overall(turn % 2, camel_color, pos)
            if not restart:
                print("---------------------------------------------------------------------------------")
                display.game_display(gameState)
                turn += 1
            starting_positions = deepcopy(gameState.camel_positions)
            board_positions = deepcopy(gameState.board_camels)
        finalGameState = deepcopy(gameState) # to calculate overall winner/loser

        # leg scores
        scores = gameState.pay_out()
        p1 += scores[0]
        p2 += scores[1]
        first = "🥇"
        second = "🥈"
        print()
        print(f"Leg {leg} scores: ")
        if scores[0] > scores[1]:
            print(f"p1 comes in 1st with {scores[0]} coins {first} {first} {first}!")
            print(f"p2 comes in 2nd with {scores[1]} coins {second} {second} {second}!")
        elif scores[1] > scores[0]:
            print(f"p2 comes in 1st with {scores[1]} coins {first} {first} {first}!")
            print(f"p1 comes in 2nd with {scores[0]} coins {second} {second} {second}!")
        else:
            print(f"p1 and p2 tie with {scores[0]} coins each {first} {first} {first}!")
        leg += 1
        print("---------------------------------------------------------------------------------")

    # overall game scores
    end = placements(finalGameState)
    calculation = overall_calculator(finalGameState.overall_winner, end)
    p1 += calculation[0]
    p2 += calculation[1]
    calculation = overall_calculator(finalGameState.overall_loser, end)
    p1 += calculation[0]
    p2 += calculation[1]

    print()
    print("Overall scores: ")
    if p1 > p2:
        print(f"p1 comes in 1st with {p1} coins {first} {first} {first}")
        print(f"p2 comes in 2nd with {p2} coins {second} {second} {second}")
    else:
        print(f"p2 comes in 1st with {p2} coins {first} {first} {first}")
        print(f"p1 comes in 2nd with {p1} coins {second} {second} {second}")