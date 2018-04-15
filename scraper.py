#Program that crawls the betting data website for relevant data regarding the Premier League and downloads it into csv files
import os
import sys
from bs4 import BeautifulSoup
import urlparse
import requests
import urllib2
import shutil

dirpath = "rawinput"

url= "http://www.football-data.co.uk/englandm.php" 
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)
links = soup.find_all('a')


#get root of url
parent = urlparse.urljoin(url, '/')

#season to start off with (works backwards to look at data for each season)
season = 17 


if os.path.exists(dirpath) and os.path.isdir(dirpath):
    shutil.rmtree(dirpath)
os.system('mkdir ' + dirpath)
os.chdir(os.getcwd() + '/' + dirpath)

#go through all links to see which have relevant info, then download it into csv files
for link in links:
	contents = str(link.contents[0])
	if "Premier League" in contents: #make sure only looking at Premier League data
		rel = link.attrs['href']
		full = parent + rel
		print(os.getcwd())
		os.system('wget -O'+ str(season)+'-'+str(season+1)+ '.csv %s' % full)

		if season == 13: #go until 13-14 season
			sys.exit(0)
		season -= 1

