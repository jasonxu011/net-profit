import requests
import urllib.request
import json
import re
from bs4 import BeautifulSoup
from scraper import scrape
from tqdm import tqdm
import pandas as pd

URL = "http://www.tennisabstract.com/charting/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

data = soup.find_all('a', href=True)
names = [a['href'] for a in data if a.text]
match_list = []

for i in tqdm(names[5:]):
	# check if female match
	if i.split("-")[1] == 'W':
		continue
	newURL = URL + i
	scraped = scrape(newURL)
	if scraped is None:
		continue
	match_list.extend(scraped)

df = pd.DataFrame.from_records(match_list, columns=['id', 'server', 'match_score', 'set_score', 'game_score', 'description'])
df.to_pickle("./matches.pkl")