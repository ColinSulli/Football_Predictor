import os
import sys

#Get a triple dict

weighting [.1, .2, .3, .4]

#probs[home][away][season]

def get_prob(home, away):
	if home not in probs or home[away] not in probs:
		return #no data in the past (newly promoted team)
	
	#if less than 4 season
	if len(home[away]) == 2:
		




