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
'''


user = Pazaak()
user.game()
