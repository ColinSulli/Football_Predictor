import os
import sys

#Get a triple dict
HOME_TEAM = 1
AWAY_TEAM = 2
HOME_WEIGHTING = .6
AWAY_WEIGHTING = .4
weighting [.1, .2, .3, .4]
seasons = ['13-14', '14-15', '16-17', '17-18']

last_5 = {}

def recent_form(home, away):

	with open(folder + filename, 'rb') as csvfile:
    	csvreader = csv.reader(csvfile, delimiter=',')

    	for line in csvreader:
    		home = line[HOME_TEAM]
    		away = line[AWAY_TEAM]

    		if home not in last_5:
    			last_5[home] = []
    		if away not in last_5:
    			last_5[away] = []

    		# append data
    		last_5[home].append()
    		last_5[away].append()


			




