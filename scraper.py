import requests
import urllib.request
import json
import re
from bs4 import BeautifulSoup
import pandas as pd

# Takes in a dirty point string, returns a list of 4 columns of point description
def point_trim(point_dirt):
	dirt = re.sub(r"\</*b\>", '', point_dirt)
	dirt = re.sub(r"&#8209;", '-', dirt)
	dirt = re.sub(r"\<[^\\<]*\>", '%', dirt)
	dirt = re.sub(r"&nbsp;", " ", dirt)
	dirt = [x.strip() for x in re.split(r"%*", dirt) if x.strip() != '']
	return dirt


# Takes in the generated URL, returns a dataframe of 
def scrape(URL):
	point_list = []

	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')

	p = re.compile('var pointlog = .*')
	m = p.findall(soup.prettify())
	if len(m) < 1:
		return None
	point_dirty = m[0].split("<tr>")

	for point in point_dirty:
		point_t = point_trim(point)
		if len(point_t) < 5:
			continue
		if len(point_t) > 5:
			point_t = point_t[:-1]
		point_t.insert(0, URL.split("/")[-1].split(".")[0])
		point_list.append(point_t)
	return point_list
