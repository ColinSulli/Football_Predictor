import os
import csv
from calcprobs import get_prob
path = os.getcwd()

def main():
	fixtures = open(path + '/processed/17-18_processed')
	csv_reader = csv.reader(fixtures)
	row_num = 1
	agency_score = 0.0
	our_score = 0.0
	for row in csv_reader:
		if row_num > 1:
			home = str(row[1])
			away = str(row[2])
			agency_h = float(row[6])
			agency_d = float(row[7])
			agency_a = float(row[8])
			our_h, our_d, our_a = get_prob(home,away)
			result = (row[5]).strip()
			appraise(our_score, our_h, our_d, our_a, result)
			appraise(agency_score, agency_h, agency_d, agency_a, result)
		row_num += 1
	print('US: ' + str(our_score))
	print('THEM: ' + str(agency_score))

def appraise(score, home, draw, away, result):
	max_prob = max(home, draw, away)

	if (max_prob == home):
		if (result == 'H'):
			score += home
		elif (result == 'D'):
			score -= (home - draw)
		else:
			score -= (home - away)

	elif (max_prob == draw):
		if (result == 'H'):
			score -= (draw - home)
		elif (result == 'D'):
			score += draw
		else:
			score -= (draw - away)

	elif (max_prob == away):
		if (result == 'H'):
			score -= (away - home)
		elif (result == 'D'):
			score -= (away - draw)
		else:
			score += away
	return