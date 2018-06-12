from modules.tertiary.opponents import play_phrase
from data.data_tools import data_gather_play
from time import sleep
from random import randint, choice as rndchoice


def c_hand():
    """comp randomly selects from the available cards in the side deck"""
    hand = []
    side_deck = [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]
    for n in range(4):
        choice = rndchoice(side_deck)
        hand.append(choice)
        side_deck.remove(choice)
    return hand


def c_stay_check(computer, opponent, options):
    """comp logic to determine if they will stay. Returns the state depending

    on if they decided to stay or not."""

    yes = 0
    # will stay
    #  no = randint(15, 90) #will not stay (old way)

    if opponent['state'] == 'stay' and computer['rs'] >= opponent['rs'] and opponent['rs'] > 15:
        yes += 2
    elif opponent['state'] == 'stay' and computer['rs'] > opponent['rs']:
        yes += 2
    elif computer['rs'] >= opponent['rs'] and computer['rs'] >= 18:
        yes += 2
    elif computer['rs'] > 17 and opponent['state'] != 'stay':
        yes += 1
    elif computer['rs'] > 17 and opponent['rs'] >= 17:
        yes += 1

    if computer['gs'] < opponent['gs'] or opponent['gs'] > 1:
        yes += 1

    if options['debug']:
        print(
            "DEBUG in c_stay_check: {} rs, gs: {}, {} ; {} rs, gs, state: {},"
            "{}, {} ; Will Stay is: {}/2 required".format(
                computer['name'], computer['rs'], computer['gs'], opponent['name'], opponent['rs'],
                opponent['gs'], opponent['state'], yes
                )
            )

    if yes > 1:
        return 'stay'
    else:
        return computer['state']


def c_check_p_stay(computer, opponent, options):
    """If the player has stayed, the comp decides whether or not they will

    stay. Dependent upon the two scores. Comp will take a draw if it is too
    risky to continue playing."""

    if options['debug']:
        print(
            "DEBUG in c_check_p_stay: {} rs: {} ; {} rs, state: {}, {}".format(
                computer['name'], computer['rs'], opponent['name'], opponent['rs'], opponent['state']
                )
            )

    if opponent['state'] == 'stay' and computer['rs'] < 21:
        print(
            "*Console: Computer is checking Player's Stay..."
            )
        sleep(options['speed']/2)

        if computer['rs'] > opponent['rs']:
            print(
                "{} chooses to stay at a higher score than {} - {} Wins"
                .format(
                    computer['name'], opponent['name'], computer['name']
                    )
                )
            return 'stay'

        elif computer['rs'] == opponent['rs'] and opponent['rs'] > 17:
            print(
                "{} chooses to stay at {}'s score - Draw Game".format(
                    computer['name'], opponent['name']
                    )
                )
            return 'stay'

        else:
            print(
                "{} chooses to not stay, round continues".format(
                    computer['name']
                    )
                )
    return computer['state']


def c_hand_phase(computer, opponent, data, options):
    """allows computer to decide which card from hand to play to get closest

    to 20 based on current score, current wins/ losses for the game, and the
    cards in their hand"""

    print(
        "---{}'s Hand---\n  {} cards".format(
            computer['name'], len(computer['hand'])
            )
        )
    sleep(options['speed']/2)

    if computer['rs'] > 14:
        if computer['main']:
            card = choice_mod_n(computer, opponent, options)
        elif not computer['main']:
            card = choice_mod_o(computer, opponent, options)

        if card:
            yes = chance_mod(computer, card, options)
            yes += gs_mod(computer, opponent, options)
            yes -= hand_mod(computer, options)

            no = randint(40, 90)
            """#!!! I'd like to have the random value have a smaller
            range, and have things like hand_mod, which negatively
            impact yes, instead positively impact 'no'. This way it is
            much more formulaic and less random"""

            sleep(options['speed'])
            if yes > no:
                play_phrase(computer)
                computer['rs'] += card
                computer['hand'].remove(card)
                print(
                    "\nPlay: {} - Score: {}".format(
                        card, computer['rs']
                        )
                    )
                data = data_gather_play(computer, data)

                if options['debug']:
                    print(
                        "DEBUG in c_hand_phase: PLAY: {} hand, card, start rs,"
                        " end rs, yes, no: {}, {}, {}, {}, {}, {}".format(
                            computer['name'], computer['hand'], card, computer['rs']-card,
                            computer['rs'], yes, no
                            )
                        )

            else:
                print("No play")

                if options['debug']:
                    print(
                        "DEBUG in c_hand_phase: No Play: {} hand, card,"
                        " rs, yes, no: {}, {}, {}, {}, {}".format(
                            computer['name'], computer['hand'], card, computer['rs'], yes, no
                            )
                        )

        else:
            print("No suitable card for play")

            if options['debug']:
                print(
                    "DEBUG in c_hand_phase: No Suitable Card: {} hand,"
                    "card, rs: {}, {}, {}".format(
                        computer['name'], computer['hand'], card, computer['rs']
                        )
                    )

    sleep(options['speed'])

    return computer['rs'], computer['hand'], data


def choice_mod_n(computer, opponent, options):
    """comp logic for picking a card to play. The ideal choice will be

    dependent upon the score it will get them to. If they have busted, the
    impetus to play a card to avoid a bust is higher and only dependent upon
    if the comp will be higher than the player if they play it. If the player
    has stayed at 20, they probably cant win at this point and would take a
    loss if they cannot also stay at 20 easily"""

    choice = None

    choice_options = list(
        filter(
            lambda x: x + computer['rs'] < 21 and x + computer['rs'] >= opponent['rs'],
            computer['hand']
            )
        )

    if computer['rs'] < 20:
        choice_options = list(
            filter(
                lambda x: x + computer['rs'] > 16 and x + computer['rs'] > computer['rs'],
                choice_options
                )
            )
        # not in danger

    elif computer['rs'] > 20:
        choice_options = list(
            filter(
                lambda x: x + computer['rs'] < computer['rs'], choice_options
                )
            )
        # danger

    for card in choice_options:
        best = 16
        test = card+computer['rs']
        if test > best:
            best, choice = test, card
        elif computer['rs'] > 20 and opponent['gs'] == 2:
            # if not playing means they lose the game
            best, choice = test, card

    if options['debug']:
        print(
            "\nDEBUG in choice_mod: {} choice options: {}".format(
                computer['name'], choice_options
                )
            )

    return choice


def choice_mod_o(computer, opponent, options):
    """

    """

    choice = None
    # if no card is chosen
    choice_round_count = 0
    best = 16
    # the best choice of card to play puts us above 16 (harder to stay over)
    for card in computer['hand']:
        # go through each card in the hand
        choice_round_count += 1
        test = card+computer['rs']
        # test is the result if the card is played
        if test < 21:
            # if the result does not make player bust
            if test > opponent['rs']:
                # and if the result puts us above the player's score

                if computer['rs'] < 20:
                    # if we are not in bust-range now
                    if test > best and test > computer['rs']:
                        # if result > current best and > current score
                        best, choice = test, card
                        # the card is chosen

                elif computer['rs'] > 20:
                    # if we are in bust-range now
                    if test > best and test < computer['rs']:
                        # if result > current best and < current score
                        best, choice = test, card
                        # the card is chosen

            elif test == opponent['rs']:
                # if the result is equal to player's score
                if test > best:
                    # if result is better than the current best
                    best, choice = test, card
                    # the card is chosen

            elif test < opponent['rs'] and computer['rs'] > 20:
                # if the result is < the player's score and comp is in danger
                if opponent['gs'] == 2:
                    # if comp has to play here to avoid losing game
                    best, choice = test, card
                    # play to prolong game and maybe win

        if options['debug']:
            print(
                "DEBUG in choice_mod round {}: {} choice, best: {},"
                "{}".format(
                    choice_round_count, computer['name'], choice, best
                    )
                )

    return choice


def chance_mod(computer, choice, options):
    """# returns the chance to play the hand card depending on the score it

    would result in if played"""

    result = choice + computer['rs']
    if computer['rs'] < 20:
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
    """for 'if computer['rs'] > 20: basically, as the hand function would never go
    through if the comp is at 20 already, if over 20 you definitely want to
    play"""

    if options['debug']:
        print(
            "DEBUG in chance_mod: {} chance, choice, rs: {}, {}, {}".format(
                computer['name'], chance, choice, computer['rs']
                )
            )
    return chance


def gs_mod(computer, opponent, options):
    """boosts chance of playing a card if their GS is higher"""

    if computer['gs'] == 2 or opponent['gs'] == 2:
        result = 15
    elif computer['gs'] == 1 or opponent['gs'] == 1:
        result = 10
    else:
        result = 5

    if options['debug']:
        print("DEBUG in gs_mod: {} result: {}".format(
            computer['name'], result
            )
        )
    return result


def hand_mod(computer, options):
    """lowers chance of playing a card relative to number of cards in hand"""

    if len(computer['hand']) == 3:
        result = 5
    elif len(computer['hand']) == 2:
        result = 10
    elif len(computer['hand']) == 1:
        result = 15
    else:
        result = 0

    if options['debug']:
        print(
            "DEBUG in hand_mod: {} hand length, result: {}, {}".format(
             computer['name'], len(computer['hand']), result
            )
        )

    return result
