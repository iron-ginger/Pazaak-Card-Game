from modules.secondary.comp import c_hand
from data.data_tools import data_gather_play
from modules.tertiary.options import rules
from time import sleep
from random import shuffle


def hand_reset(ply, options):
    '''
    lets player pick a hand, go with the default, and runs computer's hand

    selection'''

    if ply['type'] == 'human':
        return p_hand(options)
    elif ply['type'] == 'computer':
        return c_hand()


def p_hand(options):
    '''
    player inputs which cards to choose for their hand based on

    available cards in side deck
    '''

    while True:
        choice = input(
            "Do you want to pick a new hand? If no hand is currently set,"
            " entering 'n' will go with the default hand of -3, -1, 1, and"
            " 2 cards. You can also enter 'rules' to print the rulebook: "
            )
        if choice.capitalize() == 'Y':
            hand = []
            side_deck = list(range(-6, 7))
            # current standard set for side-deck
            for n in range(4):
                print("Available Cards: {}".format(side_deck))
                print("Your Hand: {}".format(hand))
                while True:
                    try:
                        sleep(options['speed']/3)
                        choice = int(input(
                            "Which card? (include the sign, if needed): "
                            ))
                        if choice in side_deck:
                            hand.append(choice)
                            side_deck.remove(choice)
                            break
                        else:
                            print("That card isn't available, choose again.")
                    except ValueError:
                        print("Invalid selection, choose again.")
            break

        elif choice == 'rules':
            rules()
        else:
            hand = [-3, -1, 1, 2]
            break

    if options['debug']:
        print("DEBUG in p_hand: hand reset == True")

    return hand


def deck_phase(ply, options):
    '''
    '''

    if len(ply['deck']) == 0:
        ply['deck'] = list(range(1, 11)) * 4
        shuffle(ply['deck'])

    card = ply['deck'][len(ply['deck'])-1]  # draws card
    ply['rs'] += card  # applies score
    ply['deck'].pop(len(ply['deck'])-1)  # discards

    print(
        "Draw: {}; {}'s score is now {}".format(
            card, ply['name'], ply['rs']
            )
        )
    sleep(options['speed'])

    return ply['deck'], ply['rs']  # returns the modified deck and round score


def hand_phase(pid, data, options):
    '''
    allows the human player to select a card from their hand to play. This

    function modifies the hand based on the chosen card, if it is available for
    selection, then returns the modified score and hand, minus the played card.
    '''

    print(
        "---{}'s Hand---\n {}".format(pid['name'], pid['hand'])
        )
    sleep(options['speed'])

    choice = input("Do you want to play from your hand? y or n: ")
    if choice.capitalize() == 'Y':
        while True:
            try:
                choice = input(
                    "Which card? Include the sign, if needed."
                    "\n  (Enter c to cancel): "
                    )
                if choice.capitalize() == 'C':
                    return pid['rs'], pid['hand']

                elif int(choice) in pid['hand']:
                    '''#!!! This is where you should do the +1-1 card check. It would
                    have to check for a specific format of the card from the
                    choice variable's input, TBD. Probably just use a
                    separate function. How you get the comp to make that
                    decision is beyond me right now.
                    '''
                    pid['rs'] += int(choice)
                    pid['hand'].remove(int(choice))

                    print(
                        "{} played {} - their score is now {}.".format(
                            pid['name'], choice, pid['rs']
                            )
                        )
                    sleep(options['speed'])
                    data = data_gather_play(pid, data)
                    break

                else:
                    print("Invalid selection, choose again.")
            except ValueError:
                print("Invalid selection, choose again.")

    return pid['rs'], pid['hand']
