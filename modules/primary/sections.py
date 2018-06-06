from modules.secondary.checks import state_check, stay_check
from modules.secondary.checks import stay_draw_check, game_check, win_check
from modules.secondary.cards import deck_phase, hand_phase, hand_reset
from modules.secondary.comp import c_check_p_stay, c_hand_phase
from modules.secondary.setters import reset, count_set, state_reset, coin_flip
from modules.secondary.setters import order_set, switch_order, record_set
from data.data_tools import data_gather_win, data_gather_stay
from modules.tertiary.opponents import phrases
from time import sleep


def loop(pid, cid, data, options):
    '''

    '''

    p1, p2 = coin_flip(pid, cid, options)
    p1['gs'], p2['gs'], game_count = reset('game', options)
    # baselines game score attributes and game count for the new game
    p1['hand'], p2['hand'] = hand_reset(p1, options), hand_reset(p2, options)
    # resets hands to either default or player choice (random for computer)
    data['win']['p1'], data['stay']['p1']['g{}'.format(
            data['game_count']
        )], data['play']['p1']['g{}'.format(
            data['game_count']
        )] = reset('data', options)

    data['win']['p2'], data['stay']['p2']['g{}'.format(
            data['game_count']
        )], data['play']['p2']['g{}'.format(
            data['game_count']
        )] = reset('data', options)

    while not game_check(p1, p2):
        # while neither has a score of 3
        game_count = count_set(game_count, 'game', options)
        # increments the current game count to track which game it is on
        p1['rs'], p2['rs'], turn_count, end_round = reset('round', options)
        # baselines round score attributes and turn count for the new game
        p1['state'], p2['state'] = state_reset(options)
        # baselines player state attributes

        while True:
            # until a break
            scores = [p1['gs'], p2['gs']]
            turn_count = count_set(turn_count, 'turn', options)
            # increments current turn count

            if p1['state'] == 'none':
                p1, p2, end_round, data = rounds(p1, p2, data, options)
            # p1 turn
            else:
                print("{} is staying at {}".format(p1['name'], p1['rs']))
            if end_round:
                phrases(p1, p2, 'lose round', 'win round')
                break

            if p2['state'] == 'none':
                p2, p1, end_round, data = rounds(p2, p1, data, options)
            # p2 turn
            else:
                print("{} is staying at {}".format(p2['name'], p2['rs']))
            if end_round:
                phrases(p1, p2, 'win round', 'lose round')
                break

            p1['gs'], p2['gs'], end_round = stay_draw_check(p1, p2, options)
            if end_round:
                break

        sleep(options['speed'])
        print(
            "\n--------Round {}:--------\n {}: {}\n {}: {}".format(
                turn_count, p1['name'], p1['rs'], p2['name'], p2['rs']
                )
            )
        print(
            "\n--------Game {} Score--------\n {}: {}\n {}: {}".format(
                game_count, p1['name'], p1['gs'], p2['name'], p2['gs']
                )
            )
        p1, p2 = switch_order(p2, p1, scores)

    # after a player wins 3 games...
    pid, cid = order_set(p1, p2)
    winner = win_check(pid, cid)
    pid = record_set(pid, winner)
    # determines winner, registers win in the player's record

    # data gather
    data = data_gather_win(pid, winner, data)

    return pid, cid, data


def rounds(player, opponent, data, options):
    '''runs a player's turn function and checks for a bust, modifying the

    opponent's score, if so. Returns both players' info and True or False,
    depending on if the player busted or not. Player can mean either computer
    or human.'''

    print("--------{}--------".format(player['name']))
    player, data = turns(player, opponent, data, options)

    if player['state'] == 'bust':
        print("{} busted!".format(player['name']))
        opponent['gs'] += 1
        return player, opponent, True, data

    else:
        return player, opponent, False, data


def turns(ply, opp, data, options):
    '''#Input: player's stats and opponent's stats; Output: modified stats for

    player (deck, rs, state, hand) 'aid' parameter is 'any id'. This is the id
    of the current turn's player. The pid is for the player when the computer
    is making decisions, which are based on both players' stats'''
    
    if ply['state'] == 'none':
        ply['deck'], ply['rs'] = deck_phase(ply, options)
        # draw part
        ply['state'] = state_check(ply, options)
        # check for stay or bust

        if ply['state'] != 'stay' and ply['type'] == 'computer':
            ply['state'] = c_check_p_stay(ply, opp, options)
            # computer decides if it will stay against a player's stay
            data = data_gather_stay(ply, data)

        if ply['state'] != 'stay' and len(ply['hand']) > 0:
            # as long as they have not stayed and have cards in hand
            if ply['type'] == 'human':
                ply['rs'], ply['hand'] = hand_phase(ply, data, options)
            elif ply['type'] == 'computer':
                ply['rs'], ply['hand'], data = c_hand_phase(
                    ply, opp, data, options
                    )

        ply['state'] = state_check(ply, options)
        # updates state attribute
        if ply['state'] == 'none':
            ply['state'] = stay_check(ply, opp, options)
            # and allow for a stay at end of turn
            data = data_gather_stay(ply, data)

    sleep(options['speed'])
    print(
        "--------Turn Summary--------\nScore is: {}\nState is: {}\nHand is: {} cards\n".format(
            ply['rs'], ply['state'], len(ply['hand'])
            )
        )
    return ply, data
