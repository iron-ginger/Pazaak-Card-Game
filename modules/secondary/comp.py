from modules.tertiary.opponents import play_phrase
from data.data_tools import data_gather_play
from time import sleep
from random import randint, choice as rndchoice


def c_hand():
    '''comp randomly selects from the available cards in the side deck'''
    hand = []
    side_deck = [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]
    for n in range(4):
        choice = rndchoice(side_deck)
        hand.append(choice)
        side_deck.remove(choice)
    return hand


def c_stay_check(cid, opp, options):
    '''comp logic to determine if they will stay. Returns the state depending

    on if they decided to stay or not.'''

    yes = 0
    # will stay
    #  no = randint(15, 90) #will not stay (old way)

    if opp['state'] == 'stay' and cid['rs'] >= opp['rs'] and opp['rs'] > 15:
        yes += 2
    elif opp['state'] == 'stay' and cid['rs'] > opp['rs']:
        yes += 2
    elif cid['rs'] >= opp['rs'] and cid['rs'] >= 18:
        yes += 2
    elif cid['rs'] > 17 and opp['state'] != 'stay':
        yes += 1
    elif cid['rs'] > 17 and opp['rs'] >= 17:
        yes += 1

    if cid['gs'] < opp['gs'] or opp['gs'] > 1:
        yes += 1

    if options['debug']:
        print(
            "DEBUG in c_stay_check: {} rs, gs: {}, {} ; {} rs, gs, state: {},"
            "{}, {} ; Will Stay is: {}/2 required".format(
                cid['name'], cid['rs'], cid['gs'], opp['name'], opp['rs'],
                opp['gs'], opp['state'], yes
                )
            )

    if yes > 1:
        return 'stay'
    else:
        return cid['state']


def c_check_p_stay(cid, opp, options):
    '''If the player has stayed, the comp decides whether or not they will

    stay. Dependent upon the two scores. Comp will take a draw if it is too
    risky to continue playing.'''

    if options['debug']:
        print(
            "DEBUG in c_check_p_stay: {} rs: {} ; {} rs, state: {}, {}".format(
                cid['name'], cid['rs'], opp['name'], opp['rs'], opp['state']
                )
            )

    if opp['state'] == 'stay' and cid['rs'] < 21:
        print(
            "*Console: Computer is checking Player's Stay..."
            )
        sleep(options['speed']/2)

        if cid['rs'] > opp['rs']:
            print(
                "{} chooses to stay at a higher score than {} - {} Wins"
                .format(
                    cid['name'], opp['name'], cid['name']
                    )
                )
            return 'stay'

        elif cid['rs'] == opp['rs'] and opp['rs'] > 17:
            print(
                "{} chooses to stay at {}'s score - Draw Game".format(
                    cid['name'], opp['name']
                    )
                )
            return 'stay'

        else:
            print(
                "{} chooses to not stay, round continues".format(
                    cid['name']
                    )
                )
    return cid['state']


def c_hand_phase(cid, opp, data, options):
    '''allows computer to decide which card from hand to play to get closest

    to 20 based on current score, current wins/ losses for the game, and the
    cards in their hand'''

    print(
        "---{}'s Hand---\n  {} cards".format(
            cid['name'], len(cid['hand'])
            )
        )
    sleep(options['speed']/2)

    if cid['rs'] > 14:
        if cid['main'] == 'yes':
            card = choice_mod_n(cid, opp, options)
        elif cid['main'] == 'no':
            card = choice_mod_o(cid, opp, options)

        if card:
            yes = chance_mod(cid, card, options)
            yes += gs_mod(cid, opp, options)
            yes -= hand_mod(cid, options)

            no = randint(40, 90)
            '''#!!! I'd like to have the random value have a smaller
            range, and have things like hand_mod, which negatively
            impact yes, instead positively impact 'no'. This way it is
            much more formulaic and less random'''

            sleep(options['speed'])
            if yes > no:
                play_phrase(cid)
                cid['rs'] += card
                cid['hand'].remove(card)
                print(
                    "\nPlay: {} - Score: {}".format(
                        card, cid['rs']
                        )
                    )
                data = data_gather_play(cid, data)

                if options['debug']:
                    print(
                        "DEBUG in c_hand_phase: PLAY: {} hand, card, start rs,"
                        " end rs, yes, no: {}, {}, {}, {}, {}, {}".format(
                            cid['name'], cid['hand'], card, cid['rs']-card,
                            cid['rs'], yes, no
                            )
                        )

            else:
                print("No play")

                if options['debug']:
                    print(
                        "DEBUG in c_hand_phase: No Play: {} hand, card,"
                        " rs, yes, no: {}, {}, {}, {}, {}".format(
                            cid['name'], cid['hand'], card, cid['rs'], yes, no
                            )
                        )

        else:
            print("No suitable card for play")

            if options['debug']:
                print(
                    "DEBUG in c_hand_phase: No Suitable Card: {} hand,"
                    "card, rs: {}, {}, {}".format(
                        cid['name'], cid['hand'], card, cid['rs']
                        )
                    )

    sleep(options['speed'])

    return cid['rs'], cid['hand'], data


def choice_mod_n(cid, opp, options):
    '''comp logic for picking a card to play. The ideal choice will be

    dependent upon the score it will get them to. If they have busted, the
    impetus to play a card to avoid a bust is higher and only dependent upon
    if the comp will be higher than the player if they play it. If the player
    has stayed at 20, they probably cant win at this point and would take a
    loss if they cannot also stay at 20 easily'''

    choice = None

    choice_options = list(
        filter(
            lambda x: x + cid['rs'] < 21 and x + cid['rs'] >= opp['rs'],
            cid['hand']
            )
        )

    if cid['rs'] < 20:
        choice_options = list(
            filter(
                lambda x: x + cid['rs'] > 16 and x + cid['rs'] > cid['rs'],
                choice_options
                )
            )
        # not in danger

    elif cid['rs'] > 20:
        choice_options = list(
            filter(
                lambda x: x + cid['rs'] < cid['rs'], choice_options
                )
            )
        # danger

    for card in choice_options:
        best = 16
        test = card+cid['rs']
        if test > best:
            best, choice = test, card
        elif cid['rs'] > 20 and opp['gs'] == 2:
            # if not playing means they lose the game
            best, choice = test, card

    if options['debug']:
        print(
            "\nDEBUG in choice_mod: {} choice options: {}".format(
                cid['name'], choice_options
                )
            )

    return choice


def choice_mod_o(cid, opp, options):
    '''

    '''

    choice = None
    # if no card is chosen
    choice_round_count = 0
    best = 16
    # the best choice of card to play puts us above 16 (harder to stay over)
    for card in cid['hand']:
        # go through each card in the hand
        choice_round_count += 1
        test = card+cid['rs']
        # test is the result if the card is played
        if test < 21:
            # if the result does not make player bust
            if test > opp['rs']:
                # and if the result puts us above the player's score

                if cid['rs'] < 20:
                    # if we are not in bust-range now
                    if test > best and test > cid['rs']:
                        # if result > current best and > current score
                        best, choice = test, card
                        # the card is chosen

                elif cid['rs'] > 20:
                    # if we are in bust-range now
                    if test > best and test < cid['rs']:
                        # if result > current best and < current score
                        best, choice = test, card
                        # the card is chosen

            elif test == opp['rs']:
                # if the result is equal to player's score
                if test > best:
                    # if result is better than the current best
                    best, choice = test, card
                    # the card is chosen

            elif test < opp['rs'] and cid['rs'] > 20:
                # if the result is < the player's score and comp is in danger
                if opp['gs'] == 2:
                    # if comp has to play here to avoid losing game
                    best, choice = test, card
                    # play to prolong game and maybe win

        if options['debug']:
            print(
                "DEBUG in choice_mod round {}: {} choice, best: {},"
                "{}".format(
                    choice_round_count, cid['name'], choice, best
                    )
                )

    return choice


def chance_mod(cid, choice, options):
    '''# returns the chance to play the hand card depending on the score it

    would result in if played'''

    result = choice + cid['rs']
    if cid['rs'] < 20:
        if result == 20:
            chance = 100
        elif result == 19:
            chance = 80
        elif result == 18:
            chance = 50
        elif result == 17:
            chance = 20
        else:
            chance = 10
    else:
        chance = 100
    '''for 'if cid['rs'] > 20: basically, as the hand function would never go
    through if the comp is at 20 already, if over 20 you definitely want to
    play'''

    if options['debug']:
        print(
            "DEBUG in chance_mod: {} chance, choice, rs: {}, {}, {}".format(
                cid['name'], chance, choice, cid['rs']
                )
            )
    return chance


def gs_mod(cid, opp, options):
    '''boosts chance of playing a card if their GS is higher'''

    if cid['gs'] == 2 or opp['gs'] == 2:
        result = 15
    elif cid['gs'] == 1 or opp['gs'] == 1:
        result = 10
    else:
        result = 5

    if options['debug']:
        print("DEBUG in gs_mod: {} result: {}".format(
            cid['name'], result
            )
        )
    return result


def hand_mod(cid, options):
    '''lowers chance of playing a card relative to number of cards in hand'''

    if len(cid['hand']) == 3:
        result = 5
    elif len(cid['hand']) == 2:
        result = 10
    elif len(cid['hand']) == 1:
        result = 15
    else:
        result = 0

    if options['debug']:
        print(
            "DEBUG in hand_mod: {} hand length, result: {}, {}".format(
             cid['name'], len(cid['hand']), result
            )
        )

    return result
