import os
import sys

#Get a triple dict
HOME_TEAM = 1
AWAY_TEAM = 2
RESULT = 5
HOME_WEIGHTING = .6
AWAY_WEIGHTING = .4
#weighting [.1, .2, .3, .4]
seasons = ['13-14', '14-15', '16-17', '17-18']

last_5 = {}

def recent_form(home, away):
	
	with open(folder + filename, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')

    	for line in csvreader:
    		# skip first line
    		if "Date" in line[0]:
    			continue

    		home = line[HOME_TEAM]
    		away = line[AWAY_TEAM]
    		result = line[RESULT].strip()

    		if home not in last_5:
    			last_5[home] = []
    		if away not in last_5:
    			last_5[away] = []

    		# home team wins
    		print result
    		if result == "H":
    			last_5[home].append(1)
    			last_5[away].append(-1)
    		
    		# away team wins
    		elif result == "A":
    			last_5[home].append(-1)
    			last_5[away].append(1)
    		# draw
    		else:
	    		last_5[home].append(0)
	    		last_5[away].append(0)




