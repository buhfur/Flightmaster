#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import sys

''' reads a file full of links and outputs the github links from each page '''
''' Turns out the website has directory traversing enabled , you can view 

all the zip files on https://legacy-wow.com/uploads/addons/vanilla/'''


 
def search_for_links(list_of_links):
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

	for url in list_of_links:

		r = requests.get(url, headers=headers)
		soup = BeautifulSoup(r.content, 'html.parser')
		#TODO: change this to look for the onclick as not all pages have github links on them

		links = [anchors.get('onclick') for anchors in soup.find_all('a')]
		addon_name = url.split('/')[-1] # extract the addon name from the URL 
'''		for link in links: 
			if link: # Some entries are NoneType , need to filter them out 
				if "github" in link and addon_name in link and "zip" in link:
					# write out links to text file???
					print(link)

'''



def parse_link_file(file):
	print(f"\n\nReading URL's\n\n")
	addon_links = []
	with open(file, 'r', encoding='unicode escape') as f:
		[addon_links.append(url) for url in f.read().splitlines()]
			

	search_for_links(addon_links) # list of links from text file 

		
			
if __name__ == '__main__':
	if sys.argv[1]: # make sure an argument exists , doesn't check input 
		if sys.argv[1] == '-s': # ghetto arg parsing , I know 
			search_for_links(sys.argv[2:])
		elif sys.argv[1] == '-p':
			parse_link_file(sys.argv[2])

		else:
			sys.stderr("no arguments specified")


