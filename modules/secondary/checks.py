from modules.secondary.comp import c_stay_check
from modules.tertiary.opponents import phrases


def game_check(score1, score2):
    '''
    checks to see either score is over 2. If someone reaches three, return

    False to end the game'''

    if score1['gs'] > 2 or score2['gs'] > 2:
        return True
    else:
        return False


def win_check(pid, cid):
    '''checks game scores to return name of winner'''

    if pid['gs'] == 3:
        phrases(pid, cid, 'win game', 'lose game')
        return pid['name']

    elif cid['gs'] == 3:
        phrases(pid, cid, 'lose game', 'win game')
        return cid['name']


def replay_check():
    '''#allows player to play again'''
    choice = input("Do you want to play again? y or n: ")
    return choice.capitalize()


def state_check(ply, options):
    '''this function sets the player's state based on their current score.

    Otherwise, it allows them to manually stay, if their score was bust but
    has since been lowered below the threshold. Finally, it returns the state
    if there is no change'''

    if options['debug']:
        print(
            "DEBUG in state_check: {} rs: {}".format(
                ply['name'], ply['rs']
                )
            )

    if ply['rs'] > 20:
        return 'bust'  # over 20 busts
    elif ply['rs'] == 20:
        return 'stay'  # at 20 stays
    else:
        return 'none'


def stay_draw_check(pid, cid, options):
    '''If both players have stayed at the end of a turn, determines if one player

    has stayed higher than the other. If so, the higher player wins. If scores
    are the same, it is a draw with no winner.# checks if both players have
    stayed, if so determining if one of the player has won the round or if it
    is a tie'''

    if options['debug']:
        print(
            "DEBUG in stay_draw_check: {} state, score: {}, {} ; {} state,"
            " score: {}, {}".format(
                pid['name'], pid['state'], pid['rs'], cid['name'],
                cid['state'], cid['rs']
                )
            )

    if pid['state'] == 'stay' and cid['state'] == 'stay':
        if pid['rs'] == cid['rs']:
            # If both players have the same score, the game is a draw
            print("Both players have stayed at the same score. Tie Game!")
            return pid['gs'], cid['gs'], True

        else:
            # checks for the player with the higher score to determine winner
            if pid['rs'] > cid['rs']:
                print(
                    "\n{} stayed higher than {}: {} wins the round!".format(
                        pid['name'], cid['name'], pid['name']
                        )
                    )
                phrases(pid, cid, 'win round', 'lose round')
                return pid['gs']+1, cid['gs'], True
            else:
                print(
                    "\n{} stayed higher than {}: {} wins the round!".format(
                        cid['name'], pid['name'], cid['name']
                        )
                    )
                phrases(cid, pid, 'win round', 'lose round')
                return pid['gs'], cid['gs']+1, True

    else:
        return pid['gs'], cid['gs'], False  # scores unchanged, round continues


def p_stay_check():
    '''allows player to choose to stay or not'''

    choice = input("\nDo you want to stay? y or n: ")
    if choice.capitalize() == 'Y':
        return 'stay'
    else:
        return 'none'


def stay_check(ply, opp, options):
    '''runs the player-appropriate stay check function if the rs is below 20'''

    if options['debug']:
        print("DEBUG in stay_check: {} rs: {}".format(ply['name'], ply['rs']))
    if ply['rs'] < 20:
        if ply['type'] == 'human':
            return p_stay_check()
        elif ply['type'] == 'computer':
            return c_stay_check(ply, opp, options)
        else:
            return ply['state']
