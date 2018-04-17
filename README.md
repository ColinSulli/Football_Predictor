# FootballProject: 

A model to predict outcomes of English Premier League football matches, as part of a final project for EECS 486.

Order of Execution on Terminal/Command Line:
1. Run scraper.py to get the raw csv files in rawinput folder (python scraper.py)
2. Run preprocess.py to process the data and have output in processed folder (python preprocess.py)
3. 

#scraper.py
Program that crawls the betting data website for relevant data regarding the Premier League and downloads it into csv files. Output folder directory is hardcoded in the file. Needs internet access to run. Caveat: needs requests, urllib, etc.

#preprocess.py
#Reads from the csv files in rawinput and pre-processes them accordingly. Spits output to the processed folder.
#calcprobs.py

#aggregate.py


Data:
#Rawinput
- Gets the raw output from scraper.py


Your project will have to include a complete implementation of your approach.  The software will have to be written in Python, and it will have to run on a Linux platform.  You can use external libraries as needed(provided they do not make the project trivial).  The grade for this part will be based on the quality of yourimplementation (which includes code documentation and a complete README file).  Please also include allthe datasets used in the project, including raw and annotated data (depending on the project).