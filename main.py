from modules.primary.pazaak import Pazaak


'''
What this program does:
1) Tracks win/loss record across multiple games played and across
multiple players
2) Allows player to play against a computer which will make
intelligent decisions based on the current scores (player and
opponent), wins/
losses for the game, and the cards in their hand
    a) AI decisions built to run based on a check/ react tree.
3) Allows player to choose to play a friend, or to play one of
several NPC personalities

1) Redo and write docstrings for ALL functions

2) Create a usable DRY function for the debug lines scattered throughout the code which take in the player objects and then run the appropriate debug functions as needed, rather than having a clunky check at the end of various parts. You do that with Data, so do it with Debug too.

3) Allow the sleep speed modifier to be modified with the settings as well, ex sleep[speed]/2 should just be sleep[speed] which takes into account that modifier when it is set.

4) Re-write rules to break down the core concepts in the game a little more concisely.

5) Re-enable data tools to be turned off.

5) For "elif choice == 6" on opponents.py, change this to a function to randomly select two different numbers and return the results, that way it is cleaner.

4) Improve comp behavior by programming multiple paradigms and allowing a
switch between them. I expect to see the computer players become more
difficult to beat by tweaking the chances to stay and play to create the
ideal weights for logical decision-makng.

5) Create the +1 -1 and tiebreaker cards
'''


user = Pazaak()
user.game()
