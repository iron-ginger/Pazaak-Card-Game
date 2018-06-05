from csv import DictWriter, QUOTE_MINIMAL
from datetime import date


def data_build(pid, cid, data):
    '''packages the data from played games in this iteration into a format
see pep 257 on docstrings
    for export to a .csv file
    #1) player type, 3) length of player's hand
    # at end of game, # 4) win count 5) stay count,
    # 6) play count
    '''

    return {
        'date': date.today(),
        '1 paradigm': pid['paradigm'],
        '1 win': data['win']['p1'],
        '1 stay': data['stay']['p1']['g{}'.format(data['game_count'])],
        '1 play': data['play']['p1']['g{}'.format(data['game_count'])],
        '2 paradigm': cid['paradigm'],
        '2 win': data['win']['p2'],
        '2 stay': data['stay']['p2']['g{}'.format(data['game_count'])],
        '2 play': data['play']['p2']['g{}'.format(data['game_count'])]}


def data_export(data):
    '''https://stackoverflow.com/questions/42977363/python-csv-header-ignore-while-keep-appending-data-to-csv-file/42978214
    '''

    with open('data/game_data.csv', 'a', newline='') as csvfile:
        # open game_data.csv in append mode
        fieldnames = [
            'date', '1 paradigm', '1 win',
            '1 stay', '1 play', '2 paradigm',
            '2 win', '2 stay', '2 play'
            ]
        # establishes header names
        writer = DictWriter(
            csvfile, fieldnames=fieldnames,
            quotechar='|', quoting=QUOTE_MINIMAL
        )  # creates the writer object with the fieldnames above

        csvfile.seek(0, 2)  # goes to the end of the file
        if csvfile.tell() == 0:  # if it is empty:
            writer.writeheader()  # writes the header

        writer.writerow(data)  # writes


def data_gather_win(p1, winner, data):
    '''this is used to take the win data for each player and return

    whichever player won the game
    '''

    if winner == p1['name']:
        # if winner is the self.p on pazaak.py...
        data['win']['p1'] = 1
    else:
        # otherwise the second player's data gets the win
        data['win']['p2'] = 1

    return data


def data_gather_stay(ply, data):
    '''this is used to take the stay data for each player and increment the

    appropriate data for whichever player stayed at that point in the game.
    It is run following a state check, so if the player stays at that time,
    it triggers. this is only for intentional stays, not stays as a result of
    drawing or playing a card (in other words, not measuring an automatic
    stay at 20)
    '''

    if ply['state'] == 'stay':
        if ply['main'] == 'yes':
            data['stay']['p1']['g{}'.format(data['game_count'])] += 1

        elif ply['main'] == 'no':
            data['stay']['p2']['g{}'.format(data['game_count'])] += 1

    return data


def data_gather_play(ply, data):
    '''this is used to take the play data for each player and increment the

    appropriate data for whichever player played at that point of the game.
    It is run in the same function as the comp's hand function, so if the
    player plays at that time, it triggers.
    '''
    if ply['main'] == 'yes':
        data['play']['p1']['g{}'.format(data['game_count'])] += 1

    elif ply['main'] == 'no':
        data['play']['p2']['g{}'.format(data['game_count'])] += 1

    return data
