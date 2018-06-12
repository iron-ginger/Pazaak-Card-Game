from modules.secondary.checks import state_check, stay_check
from modules.secondary.checks import stay_draw_check, game_check, win_check
from modules.secondary.cards import deck_phase, hand_phase, hand_reset
from modules.secondary.comp import c_check_p_stay, c_hand_phase
from modules.secondary.setters import reset, count_set, state_reset, coin_flip
from modules.secondary.setters import order_set, switch_order, record_set
from data.data_tools import data_gather_win, data_gather_stay
from modules.tertiary.opponents import phrases
from time import sleep


def game(player_1, player_2, data, options):
    """The game's loop, running until someone has won

    Order summary: Flip for who goes first. The rest of the function (until
    the very end) will refer to the players as p1 and p2, by order of play.
    Reset game count, hands, data for each player. Enter loop: increment
    game_count and reset turn_count, end_round, state attributes. Enter
    loop: Note current game scores in a list. Reset turn count, run rounds
    function for each player until someone loses. Break. Swap order so
    loser goes first. When the outer loop breaks, reset player order and
    check winner. Record score on player_1's attributes. Gather data. Return.

    Inputs: player_1 and player_2 attribute structures,
    data values and options.
    Outputs: Player_1 and player_2 attribute structures
    and data values
    """

    p1, p2 = coin_flip(player_1, player_2, options)
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

    while not game_check(p1['gs']) and not game_check(p2['gs']):
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

            if p1['state'] is None:
                p1, p2, end_round, data = rounds(p1, p2, data, options)
            # p1 turn
            else:
                print("{} is staying at {}".format(p1['name'], p1['rs']))
            if end_round:
                phrases(p1, p2, 'lose round', 'win round')
                break

            if p2['state'] is None:
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
    player_1, player_2 = order_set(p1, p2)
    winner = win_check(player_1, player_2)
    player_1 = record_set(player_1, winner)
    # determines winner, registers win in the player's record

    # data gather
    data = data_gather_win(player_1, winner, data)

    return player_1, player_2, data


def rounds(player, opponent, data, options):
    """
    Middle turn result handler for an individual player's turn.

    From here on, players are referred to as Player and Opponent.

    Order Summary: Call turns, check state. If bust, increment opponent's
    game score and return True. Else, Return False.

    Inputs: player and opponent attribute structures,
    data values and options.
    Outputs: Player and opponent attribute structures
    and data values, and True or False.
    """

    print("--------{}--------".format(player['name']))
    player, data = turns(player, opponent, data, options)

    if player['state'] == 'bust':
        print("{} busted!".format(player['name']))
        opponent['gs'] += 1
        return player, opponent, True, data

    else:
        return player, opponent, False, data


def turns(player, opponent, data, options):
    """
    Runs functions for handling gameplay in a turn

    Order Summary: Check state. 1) If state is none, run deck_phase and
    check state. If player isn't staying and the player is a computer, it
    checks to see if it wants to stay. Gather data. If player isn't staying
    and they have cards, runs hand_phase. Checks state. Gather data.
    2) Else, print and return.

    Inputs: player and opponent attribute structures,
    data values and options.
    Outputs: Player attributes and data values.
    """

    if player['state'] is None:
        player['deck'], player['rs'] = deck_phase(player, options)
        # draw part
        player['state'] = state_check(player, options)
        # check for stay or bust

        if player['state'] != 'stay' and player['type'] == 'computer':
            player['state'] = c_check_p_stay(player, player, options)
            # computer decides if it will stay against a player's stay
            data = data_gather_stay(player, data)

        if player['state'] != 'stay' and len(player['hand']) > 0:
            # as long as they have not stayed and have cards in hand
            if player['type'] == 'human':
                player['rs'], player['hand'] = hand_phase(player, data, options)
            elif player['type'] == 'computer':
                player['rs'], player['hand'], data = c_hand_phase(
                    player, player, data, options
                    )

        player['state'] = state_check(player, options)
        # updates state attribute
        if player['state'] is None:
            player['state'] = stay_check(player, player, options)
            # and allow for a stay at end of turn
            data = data_gather_stay(player, data)

    sleep(options['speed'])
    print(
        "--------Turn Summary--------\nScore is: {}\nState is: {}\nHand is: {} cards\n".format(
            player['rs'], player['state'], len(player['hand'])
            )
        )
    return player, data
