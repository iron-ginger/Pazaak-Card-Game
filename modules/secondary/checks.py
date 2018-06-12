from modules.secondary.comp import c_stay_check
from modules.tertiary.opponents import phrases


def game_check(score):
    """Returns true or false dependent on if game score is over two."""

    if score > 2:
        return True
    else:
        return False


def win_check(player, opponent):
    """checks game scores to return name of winner"""

    if player['gs'] == 3:
        phrases(player, opponent, 'win game', 'lose game')
        return player['name']

    elif opponent['gs'] == 3:
        phrases(player, opponent, 'lose game', 'win game')
        return opponent['name']


def replay_check():
    """allows player to play again"""
    choice = input("Do you want to play again? y or n: ")
    return choice.capitalize()


def state_check(player, options):
    """this function sets the player's state based on their current score.

    Otherwise, it allows them to manually stay, if their score was bust but
    has since been lowered below the threshold. Finally, it returns the state
    if there is no change"""

    if options['debug']:
        print(
            "DEBUG in state_check: {} rs: {}".format(
                player['name'], player['rs']
                )
            )

    if player['rs'] > 20:
        return 'bust'  # over 20 busts
    elif player['rs'] == 20:
        return 'stay'  # at 20 stays
    else:
        return None


def stay_draw_check(player, opponent, options):
    """If both players have stayed at the end of a turn, determines if one player

    has stayed higher than the other. If so, the higher player wins. If scores
    are the same, it is a draw with no winner.# checks if both players have
    stayed, if so determining if one of the player has won the round or if it
    is a tie"""

    if options['debug']:
        print(
            "DEBUG in stay_draw_check: {} state, score: {}, {} ; {} state,"
            " score: {}, {}".format(
                player['name'], player['state'], player['rs'], opponent['name'],
                opponent['state'], opponent['rs']
                )
            )

    if player['state'] == 'stay' and opponent['state'] == 'stay':
        if player['rs'] == opponent['rs']:
            # If both players have the same score, the game is a draw
            print("Both players have stayed at the same score. Tie Game!")
            return player['gs'], opponent['gs'], True

        else:
            # checks for the player with the higher score to determine winner
            if player['rs'] > opponent['rs']:
                print(
                    "\n{} stayed higher than {}: {} wins the round!".format(
                        player['name'], opponent['name'], player['name']
                        )
                    )
                phrases(player, opponent, 'win round', 'lose round')
                return player['gs']+1, opponent['gs'], True
            else:
                print(
                    "\n{} stayed higher than {}: {} wins the round!".format(
                        opponent['name'], player['name'], opponent['name']
                        )
                    )
                phrases(opponent, player, 'win round', 'lose round')
                return player['gs'], opponent['gs']+1, True

    else:
        return player['gs'], opponent['gs'], False  # scores unchanged, round continues


def p_stay_check():
    """allows player to choose to stay or not, returning a string or a bool"""

    choice = input("\nDo you want to stay? y or n: ")
    if choice.capitalize() == 'Y':
        return 'stay'
    else:
        return None


def stay_check(player, opponent, options):
    """runs the player-appropriate stay check function if rs is below 20"""

    if options['debug']:
        print("DEBUG in stay_check: {} rs: {}".format(player['name'], player['rs']))

    if player['rs'] < 20:
        if player['type'] == 'human':
            return p_stay_check()
        elif player['type'] == 'computer':
            return c_stay_check(player, opponent, options)
        else:
            return player['state']
