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



def get_recent_form(home_input, away_input):
	last_5 = {}
	csvfile = open(folder + filename, 'rb')
	csvreader = csv.reader(csvfile, delimiter=',')

	for line in csvreader:
		if "Date" in line:
			continue

		home = line[HOME_TEAM]
		away = line[AWAY_TEAM]
		result = line[RESULT].strip()

		if home == home_input and away == away_input: #stop when you reach the current app
			break

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

	home_recent_form = 0.0
	away_recent_form = 0.0

	#If less than 5 games have happened just exit out
	if home_input not in last_5 or len(last_5[home_input]) < 5:
		return "NONE", "NONE"

	for result in last_5[home_input]:
		home_recent_form += result
	for result in last_5[away_input]:
		away_recent_form += result

	return home_recent_form, away_recent_form
	


	





