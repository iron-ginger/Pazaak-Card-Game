from random import randint
from time import sleep


def switch_order(p1, p2, scores):
    """Swaps order of players depending on who won. 'Loser takes it out.'

    Order Summary: Check player scores versus scores set at beginning of
    the round.

    Inputs: player 1 and 2 attributes and scores previously noted
    Outputs: player attributes"""

    if p2['gs'] != scores[1]:
        return p1, p2
        # p1 plays first next round
    else:
        # if p1's score has changed from the start of the round
        #or if nobody won, reverse the order
        return p2, p1
        # p2 plays first next round


def coin_flip(player, opponent, options):
    """Sets play order with a coin toss"""

    print("\nFlipping for who plays first...")
    sleep(options['speed']/2)

    if randint(0, 1) == 1:
        print("{} goes first!".format(player['name']))
        return player, opponent
    else:
        print("{} goes first!".format(opponent['name']))
        return opponent, player


def order_set(player_1, player_2):
    """sorts the players into their original order for the game's end"""

    if player_1['main']:
        return player_1, player_2
    else:
        return player_2, player_1


def reset(arg, options):
    """baseline scores and counter based on the arg presented

    Inputs: string arg, options attributes
    Outputs: three zeros, boolean.

    arg = 'round': resets the end_round counter as well with the boolean
    arg = 'game' or 'data' resets the three counts.

    Prints based on arg presented
    """

    sleep(options['speed']/2)
    count = 0

    if arg == 'round':
        end_round = False
        print("*Console: Round scores have been reset")
        return count, count, count, end_round
    elif arg == 'game':
        print("*Console: Game scores and counters have been reset")
        return count, count, count
    elif arg == 'data':
        print("*Console: Data for game is baselined")
        return count, count, count


def count_set(count, level, options):
    """increments the count and prints the appropriate statement"""

    count += 1
    sleep(options['speed']/2)

    if level == 'game':
        print("\n\n--------Game {}--------".format(count))
    elif level == 'turn':
        print("\n--------Turn {}--------".format(count))

    return count


def state_reset(options):
    """'resets the game state for each player"""

    sleep(options['speed']/2)
    print("*Console: States have been reset")
    return None, None


def record_set(player, winner):
    """sets the player's win/ loss record if they won"""

    if winner == player['name']:
        player['record']['win'] += 1
    else:
        player['record']['loss'] += 1

    return player
