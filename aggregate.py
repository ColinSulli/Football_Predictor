import os
import sys
import csv

#Get a triple dict
HOME_TEAM = 2
AWAY_TEAM = 3
RESULT = 6
HOME_WEIGHTING = .6
AWAY_WEIGHTING = .4
#weighting [.1, .2, .3, .4]
# seasons = ['13-14', '14-15', '16-17', '17-18']

folder = 'rawinput/'
filename = '17-18.csv'

def recent_form():
	last_5 = {}
	csvfile = open(folder + filename, 'rb')
	csvreader = csv.reader(csvfile, delimiter=',')

	for line in csvreader:
		if "Date" in line:
			continue

		home = line[HOME_TEAM]
		away = line[AWAY_TEAM]
		result = line[RESULT].strip()

		if home not in last_5:
			last_5[home] = []
		if away not in last_5:
			last_5[away] = []

		if result == "H":
			last_5[home].append(1)
			last_5[away].append(-1)
		elif result == "A":
			last_5[home].append(-1)
			last_5[away].append(1)
		else:
			last_5[home].append(0)
			last_5[away].append(0)

		for team in last_5:
			if len(last_5[team]) > 5:
				last_5[team] = last_5[team][-5:]

	return last_5
print recent_form()






