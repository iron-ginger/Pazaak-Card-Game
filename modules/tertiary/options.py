from time import sleep


def change_speed(options):
    """

    """

    while True:
        try:
            choice = int(
                input(
                    "How slow would you like to messages to appear? 0, 1,"
                    " 2, or 3 (3 is slowest): "
                    )
                )
            if choice in range(0, 4):
                print("Speed is now: {}".format(choice))
                sleep(options['speed']/2)
                return choice

            else:
                print("That is not an option, Leroy. Choose again")
                sleep(options['speed']/2)

        except ValueError:
            print("Invalid input. Choose again: ")


def rules():
    """

    """
    with open("reads/rules.txt", 'r') as rulebook:
        print("\n{}\n\n".format(rulebook.read()))


def debug(options):
    """

    """
    while True:
        try:
            choice = input(
                "Would you like to turn debug mode 'on' or 'off': "
            )
            if choice.capitalize() == 'On':
                print("Debug mode: ON")
                sleep(options['speed']/2)
                return True

            elif choice.capitalize() == 'Off':
                print("Debug mode: OFF")
                sleep(options['speed']/2)
                return False

            else:
                print("That is not an option, Leroy. Choose again")
                sleep(options['speed']/2)

        except ValueError:
            print("Invalid Input")


def run_amount(player_1, player_2):
    """

    """

    if player_1['type'] == 'computer' and player_2['type'] == 'computer':
        while True:
            try:
                return int(
                    input(
                        "How many times would you like to run the sim?"
                        )
                    )
            except ValueError:
                ("Invalid Input")
    else:
        return 1


def data_switch():
    """

    """

    choice = input("Do you want to enable data tools? Enter y or n: ")
    if choice.capitalize() == 'Y':
        print("Data tools: enabled")
        return True

    else:
        print("Data tools: disabled")
        return False
