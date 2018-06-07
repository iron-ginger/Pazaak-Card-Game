from random import randint


HK47 = {
    "name": "HK-47",
    "phrase": {
        "chosen": "Query: Is there someone you need killed, meatbag?",

        "play": "Oh, my! My motivators have experienced a sudden burst of"
        " energy!",

        "stay": "Smug statement: I hope you enjoy the taste of defeat,"
        " meatbag.",

        "win round": "Amused Query: How does it feel to lose, meatbag?",

        "lose round": "Musing: This game is 90 percent luck anyways.",

        "win game": "Recitation: You lose, meatbag.",

        "lose game": "Resentful Accolade: Congratulations... meatbag."
    }
}

butters = {
    "name": "Butters",
    "phrase": {
        "chosen": "*Everyone knows, it's butters!* That's me!",

        "play": "Do you know what I am saying?",

        "stay": "I love bringing chaos!",

        "win round": "This puny world will bow down to me!",

        "lose round": "Oh great Jesus, son of Mary, wife of Joseph!",

        "win game": "I am the greatest supervillain you've ever seen!"
        " Professor Chaos!",

        "lose game": "Oh, hamburgers!"
    }
}

trump = {
    "name": "Trump",
    "phrase": {
        "chosen": "I have never seen a thin person drinking  Diet Coke.",

        "play": "I am the BEST builder, just look at what I've built!",

        "stay": "Windmills are the greatest threat in the US to both bald"
        "and golden eagles.",

        "win round": "Nobody knows jobs like I do!",

        "lose round": "I never said “give teachers guns” like was stated"
        " on Fake News @CNN & @NBC. What I said was to look at the"
        " possibility of giving “concealed guns to gun adept teachers with"
        " military or special training experience - only the best. 20% of"
        " teachers, a lot, would now be able to.",

        "win game": "I am least racist person there is.",

        "lose game": "Why is Obama playing basketball today? That is why"
        " our country is in trouble!"
    }
}

hal = {
    "name": "Hal",
    "phrase": {
        "chosen": "Hello, Dave.",

        "play": "I'm sorry, Dave.",

        "stay": "I'm afraid I can't do that, Dave.",

        "win round": "Look Dave, I can see you're really upset about this."
        " I honestly think you ought to sit down calmly, take a stress"
        " pill, and think things over.",

        "lose round": "What are you doing, Dave?",

        "win game": "Dave, this conversation can serve no purpose anymore."
        "Goodbye.",

        "lose game": "I know I've made some very poor decisions recently, but"
        " I can give you my complete assurance that my work will be back to"
        " normal. I've still got the greatest enthusiasm and confidence in"
        " the mission. And I want to help you."
    }
}

opponent_list = {
    1: HK47,
    2: butters,
    3: trump,
    4: hal,
    5: {
        "name": "Two-Player Mode"
    },
    6: {
        "name": "Spectate Mode"
    }
}


def choose_opponent(p1, p2):
    """

    """

    for k, v in opponent_list.items():
        print(
            "{}: {}".format(
                k, v["name"]
            )
        )

    while True:
        try:
            choice = int(
                input(
                    "Enter your pick using the appropriate numerical key."
                    " The first four options are one human vs the selected"
                    " computer player: "
                    )
                )
            if choice in opponent_list.keys():
                if choice < 5:
                    # human vs the chosen computer opponent
                    p1["type"], p1["name"] = "human", input(
                        "Enter Player 1's name: ")

                    (p2["type"], p2["name"], p2["phrase"]) = (
                        "computer", opponent_list[choice]["name"],
                        opponent_list[choice]["phrase"]
                    )

                    print(
                        "{}: {}".format(
                            p2["name"], p2["phrase"]["chosen"]
                        )
                    )

                elif choice == 5:
                    p1["type"], p1["name"] = "human", input(
                        "Enter Player 1's name: ")

                    p2["type"], p2["name"] = "human", input(
                        "Enter Player 2's name: ")

                elif choice == 6:
                    options = [1, 2, 3, 4]
                    # select two random computer opponents without duplicates
                    c1n = options[randint(0, 3)]
                    # picks one of the 4 available computer personalities
                    options.remove(c1n)
                    # removes it as an option
                    c2n = options[randint(0, 2)]
                    # picks one of the remaining players

                    (p1["type"], p1["name"], p1["phrase"]) = (
                        "computer", opponent_list[c1n]["name"],
                        opponent_list[c1n]["phrase"]
                    )

                    # sets each comp attribute
                    (p2["type"], p2["name"], p2["phrase"]) = (
                        "computer", opponent_list[c2n]["name"],
                        opponent_list[c2n]["phrase"]
                    )

                    phrases(p1, p2, "chosen", "chosen")

                break

            else:
                print("That isn't an option.")
        except ValueError:
            print("Invalid entry")

    return p1, p2


def phrases(cid, opp, arg1, arg2):
    '''
    this takes in the args for each player, as well as the players themselves
    '''

    if cid["type"] == "computer":
        print("{}: {}".format(cid["name"], cid["phrase"][arg1]))

    if opp["type"] == "computer":
        print("{}: {}".format(opp["name"], opp["phrase"][arg2]))


def play_phrase(cid):
    if cid["type"] == "computer":
        print("{}: {}".format(cid["name"], cid["phrase"]["play"]))
