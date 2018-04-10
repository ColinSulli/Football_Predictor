import os
import sys
from bs4 import BeautifulSoup
import urlparse
import requests
import urllib2

current= "http://www.football-data.co.uk/englandm.php" 
page = urllib2.urlopen(current)
soup = BeautifulSoup(page)
links = soup.find_all('a')


#get root of url
parent = urlparse.urljoin(current, '/')

#season to start off with
season = 17

for link in links:
	contents = str(link.contents[0])
	if "Premier League" in contents: #check to see if betting data is for CSV files
		rel = link.attrs['href']
		full = parent + rel
		os.system('wget -O'+ str(season)+'-'+str(season+1)+ '.csv %s' % full)

		if season == 13: #go until 13-14 season
			sys.exit(0)
		season -= 1

