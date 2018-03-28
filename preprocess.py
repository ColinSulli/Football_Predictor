import csv
import os
import sys

DATE_INDEX = 1
HOME_TEAM = 2
AWAY_TEAM = 3
FTHG = 4
FTAG = 5
FTR = 6

BETTING_START = 23
BETTING_END = 43

folder = "rawinput/"

os.mkdir("processed")

for filename in os.listdir("rawinput/"):
	sys.stdout = open("processed/" + filename.replace(".csv", "") + "_processed.csv", 'w') 

	with open(folder + filename, 'rb') as csvfile:
	    csvreader = csv.reader(csvfile, delimiter=',', quotechar=',')

	    for line in csvreader:
	    	try:
	    		print line[DATE_INDEX] + ",",
	    	except Exception:
	    		continue
	    	print line[HOME_TEAM] + ",",
	    	print line[AWAY_TEAM] + ",",
	    	print line[FTHG] + ",",
	    	print line[FTAG] + ",",
	    	print line[FTR] + ",",

	    	avg_home_odds = 0.0
	    	avg_draw_odds = 0.0
	    	avg_away_odds = 0.0
	    	home_index = BETTING_START
	    	draw_index = home_index + 1
	    	away_index = draw_index + 1

	    	try:
		    	while(home_index <= BETTING_END):
		    		avg_home_odds += float(line[home_index])
		    		avg_draw_odds += float(line[draw_index])
		    		avg_away_odds += float(line[away_index])

		    		#increment index
		    		home_index += 3
		    		draw_index += 3
		    		away_index += 3
		    	
		    	avg_home_odds /= int(float(BETTING_END + 1 - BETTING_START) / 3)
		    	avg_draw_odds /= int(float(BETTING_END + 1 - BETTING_START) / 3)
		    	avg_away_odds /= int(float(BETTING_END + 1 - BETTING_START) / 3)

		    	avg_home_prob = (avg_away_odds) / (avg_home_odds + avg_draw_odds + avg_away_odds)
		    	avg_draw_prob = (avg_draw_odds) / (avg_home_odds + avg_draw_odds + avg_away_odds)
		    	avg_away_prob = (avg_home_odds) / (avg_home_odds + avg_draw_odds + avg_away_odds)

		    	print str(avg_home_prob) + ",",
		    	print str(avg_draw_prob) + ",",
		    	print str(avg_away_prob) + ",",
		    	print
	    	except ValueError:
	    		print "AVGHOMEPROB,",
	    		print "AVGDRAWPROB,",
	    		print "AVGAWAYPROB",
	    		print
	    		continue
	sys.stdout = sys.__stdout__ 
