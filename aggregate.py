import os
import sys

#Get a triple dict

HOME_WEIGHTING = .6
AWAY_WEIGHTING = .4
weighting [.1, .2, .3, .4]
seasons = ['13-14', '14-15', '16-17', '17-18']

#probs[season][home][away]

def get_prob(home, away):
	
	sum_probs = 0.0
	sum_weighting = 0
	for index in range(0, len(seasons)):
		curr_season = seasons[index]
		if home in matches[curr_season] and away in matches[curr_season][home]:
			sum_weighting += weighting[index]
			sum_probs += (weighting(index) * (HOME_WEIGHTING * matches[curr_season][home][away] + AWAY_WEIGHTING * matches[curr_season][away][home]))


	return float((sum_probs / sum_weighting))
			




