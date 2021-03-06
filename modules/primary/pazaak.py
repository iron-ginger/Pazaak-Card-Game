from modules.tertiary.opponents import choose_opponent, opponent_list
from modules.tertiary.options import change_speed, rules, debug
from modules.tertiary.options import run_amount, data_switch
from modules.secondary.checks import replay_check
from modules.primary.sections import game
from data.data_tools import data_build, data_export


class Pazaak(object):
    def __init__(self):
        """Initializes the player, computer, data, and options for the game
        
        The key/ value pairs in the player_1 / 2
        dictionaries are referred to as attributes
        throughout the program.
        """
        self.player_1 = {
            'type': 'computer',
            'name': 'T3M4',
            'phrase': opponent_list[4]['phrase'],
            'record': {'win': 0, 'loss': 0},
            'gs': 0,
            'rs': 0,
            'deck': [],
            'hand': [-3, -1, 1, 2],
            'state': None,
            'main': True,
            'paradigm': 'new'
            }

        self.player_2 = {
            'type': 'computer',
            'name': opponent_list[4]['name'],
            'phrase': opponent_list[4]['phrase'],
            'gs': 0,
            'rs': 0,
            'deck': [],
            'hand': [-3, -1, 1, 2],
            'state': None,
            'main': False,
            'paradigm': 'old'
            }

        self.data = {
            'date': None,
            'game_count': 0,
            'run count': 0,
            'win': {'p1': 0, 'p2': 0},
            'stay': {'p1': {}, 'p2': {}},
            'play': {'p1': {}, 'p2': {}}
            }

        self.options = {
            'speed': 0,
            'debug': True,
            'data': True
            }

    def play(self):
        """Runs the game by calling a function based on user input"""
        while True:
            choice = input(
                "\nWhat would you like to do? Enter one of the following: "
                "\n Play a game: 'game'"
                "\n Change opponent, enable multiplayer, or run a Comp v."
                " Comp game: 'players'"
                "\n Change the speed: 'speed'"
                "\nDebug Mode: 'debug'"
                "\nRead the Rules: 'rules'"
                "\nTurn Big Data on/ off: 'data'"
                "\nExit Game: 'exit'"
                "\n "
                )

            if choice == 'game':
                for n in range(run_amount(self.player_1, self.player_2)):
                    self.data['game_count'] += 1

                    self.player_1, self.player_2, self.data = game(
                        self.player_1, self.player_2, self.data, self.options
                        )

                    if self.options['data']:
                        data_export(
                            data_build(
                                self.player_1, self.data
                                ), 
                            data_build(
                                self.player_2, self.data
                                )
                            )

                        print(
                            "\nGame Count: {}\n\n".format(
                                self.data['game_count']
                                )
                        )

                if self.player_1['type'] == 'human':
                    if replay_check() == 'Y':
                        loop(self.player_1, self.player_2, self.data, self.options)
                    else:
                        break

            elif choice == 'players':
                self.player_1, self.player_2 = choose_opponent(self.player_1, self.player_2)
            elif choice == 'speed':
                self.options['speed'] = change_speed(self.options)
            elif choice == 'rules':
                rules()
            elif choice == 'debug':
                self.options['debug'] = debug(self.options)
            elif choice == 'data':
                self.options['data'] = data_switch()
            elif choice == 'exit':
                exit()
            else:
                print("Sorry, I didn't get that.")
