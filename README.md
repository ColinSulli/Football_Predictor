# FootballProject:

A model to predict outcomes of English Premier League football matches.

Before you run our programs on caen, type the following commands into the command line in order to import the proper libraries:
        module load python
        python
        >>> from bs4 import BeautifulSoup
        >>> import urlparse
        >>> import requests
        >>> import urllib2
        >>> import shutil
        >>> exit()

Order of Execution on Terminal/Command Line:
1. Run scraper.py to get the raw csv files in rawinput folder (python scraper.py)
2. Run preprocess.py to process the data and have output in processed folder (python preprocess.py)
3. Run calcprobs.py to calculate the probabilites for every match that has been played in the current 2017/18 season (python calprobs.py)

## Python Files
#scraper.py
Program that crawls the betting data website for relevant data regarding the Premier League and downloads it into csv files. Output folder directory is hardcoded in the file. Needs internet access to run. Caveat: needs requests, urllib, etc.

#preprocess.py
Reads from the csv files in rawinput and pre-processes them accordingly. Spits output to the processed folder.

#calcprobs.py
This is the main python file that calulcates the probabilities for every match that has been played in the current 2017/18 season. This function outputs the probabilities to a csv file called output.csv located in the folder called final.

#aggregate.py
Is run when calcprobs.py is called. This function determines a team's recent form, i.e. how the team has been perforiming over the past 5 games played. The function then takes this data and adjusts the 3-way probabilites for the match.

## Data Folders/Files
#Rawinput
Gets the raw output from scraper.py. These are 5 csv files, one for each Premier League season.

#Processed
Folder that contains all of the processed csv files (once again 5 csv files, one fore each Premier League season).

#Final
Folder that contains the final output after calcprobs.py is run

#Analysis.xls is the output file (from above), with some conditional formatting to highlight the results. This file splits the season into thirds, and compares our performance with the other betting agencies. At each third we look at the median performance (for a random game how will does each agency do) and the sum (how well each model did cumulatively across the third of that season). The higher the score in either case, the better the model's performance. 


