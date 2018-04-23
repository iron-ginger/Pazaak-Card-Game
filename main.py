from modules.primary.pazaak import Pazaak

'''
	What this program does:
	1) Tracks win/loss record across multiple games played and across multiple players
	2) Allows player to play against a computer which will make intelligent decisions based on the current scores (player and opponent), wins/ losses for the game, and the cards in their hand
		a) AI decisions built to run based on a check/ react tree.
	3) Allows player to choose to play a friend, or to play one of several NPC personalities

1) Align with standards set in PEP8: https://www.python.org/dev/peps/pep-0008/

2) Improve comp behavior by programming multiple paradigms and allowing a switch between them. I expect to see the computer players become more difficult to beat by tweaking the chances to stay and play to create the ideal weights for logical decision-makng.

3) Create the +1 -1 and tiebreaker cards
'''



user = Pazaak()
user.game()
