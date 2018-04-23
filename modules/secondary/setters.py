from random import randint
from time import sleep


def switch_order(p1, p2, scores): #takes in both players' data and the original scores they had at the beginning of the round. Whoever didn't score that round is returned as p1, with the winner as p2.
	if p1['gs'] != scores[0]: #if p1's score has changed from the start of the round
		return p2, p1 #p2 plays first next round
	elif p2['gs'] != scores[1]: #alternatively, if p2's score changed from the start of the round
		return p1, p2 #p1 plays first next round
	else: return p2, p1 #if nobody won (draw game), reverse the order
#
def coin_flip(pid, cid, options): #sets the order for each player to play dependent upon a random coin toss
	print("\nFlipping for who plays first...")
	sleep(options['speed']/2)
	if randint(0,1) == 1:	
		print("{} goes first!".format(pid['name']))
		return pid, cid
	else: 
		print("{} goes first!".format(cid['name']))
		return cid, pid
#
def order_set(p1, p2): #sorts the players in order for a return to their order for the game's end
	if p1['main'] == 'yes':	return p1, p2
	else: return p2, p1
#
def reset(arg, options): #baseline scores and counter, printing which has been reset based on the arg and, if it is a round arg, also resets the end_round test
	sleep(options['speed']/2)
	count = 0
	
	if arg == 'round': 
		end_round = False
		print("*Console: Round scores have been reset")
		return count, count, count, end_round
	elif arg == 'game':
		print("*Console: Game scores and counters have been reset")
		return count, count, count
	elif arg == 'data':
		print("*Console: Data for game is baselined")
		return count, count, count

#
def count_set(count, level, options): #increments the count, printing the appropriate statement based on the level passed as a parameter
	count += 1
	sleep(options['speed']/2)
	if level == 'game':	print("\n\n--------Game {}--------".format(count))
	elif level == 'turn': print("\n--------Turn {}--------".format(count))
	
	return count
#
def state_reset(options): #resets the game state for each player
	sleep(options['speed']/2)
	print("*Console: States have been reset")
	return 'none', 'none'
#
def record_set(pid, winner): #sets the player's win/ loss record based on the passed name of the winner
	if winner == pid['name']: pid['record']['win'] += 1
	else: pid['record']['loss'] += 1
	
	return pid