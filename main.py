from modules.primary.pazaak import Pazaak
#from app_pazaak.pazaak_app import Pazaak_App
#from tkinter import Tk

'''
	What this program does:
	1) Tracks win/loss record across multiple games played and across multiple players
	2) Allows player to play against a computer which will make intelligent decisions based on the current scores (player and opponent), wins/ losses for the game, and the cards in their hand
		a) AI decisions built to run based on a check/ react tree.
	3) Allows player to choose to play a friend, or to play one of several NPC personalities

2.0 Release
Create a GUI Application with tkinter

Align with standards set in PEP8: https://www.python.org/dev/peps/pep-0008/
Package with PIP

Post to GitHub! and link on https://www.reddit.com/r/codereview/

Improve comp behavior by programming multiple paradigms and allowing a switch between them. I expect to see the computer players become more difficult to beat by tweaking the chances to stay and play to create the ideal weights for logical decision-makng.

Create the +1 -1 and tiebreaker cards

Future Ideas
-) Create a game board to show the cards (max # card slots 25, min probably 15)
-) use google Flutter for the app design (?)

-) https://riverbankcomputing.com/software/pyqt/intro
or
-) Tkinter

-) Use https://www.panda3d.org for the game (?)
-) Create a web app in Django (or REPL) to play it through, complete with cantina band music.

-x) Alternate game idea: Name: Sucker. Teams of two, similar draw/ play concept to pazaak, but with cards like a cross between Pazaak and Uno. The two players share 6 cards between them, and draw the cards anew each round. Once out of cards, they are left with only the option to stay after drawing from the deck. The goal is to play cards to get the opponent to lose. The cards they play can be played on either player, and whichever player's score reaches a certain threshold has the advantage, because once a team goes out, the players on the team with the most points each gets all the points their team won. The team that didn't get the most splits the points between them. The teams then flip. Whichever player reaches a certain amount first wins. It pays to play your teammate as a resource, and to keep your enemies close. (WIP CONCEPT)
'''



user = Pazaak()
user.game()