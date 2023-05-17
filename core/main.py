#!/usr/bin/env python3 
import requests
from bs4 import BeautifulSoup 
import sys

''' gets all links on the legacy-wow.com webpage '''
def get_anchors(url):
	headers = { 'Host': 'legacy-wow.com',
'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'Referer': 'https://legacy-wow.com/',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'DNT': '1',
'Sec-GPC': '1'}
#'If-Modified-Since': 'Tue, 16 May 2023 20:08:11 GMT'}

	home_page = requests.get(url, headers=headers)
	#print(home_page.status_code)
	soup = BeautifulSoup(home_page.content, 'html.parser')

	#all_links = soup.find_all('a') # list of links to most addons on the site
	for link in soup.find_all('a'):
		print(link.get('href')) # only prints out the links themselves 

	


	
	






if __name__ == '__main__':
	if sys.argv[1]:
		get_anchors(sys.argv[1])




