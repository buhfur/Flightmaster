import json
import os
import sys
import pathlib
import tempfile
import shutil
import pprint
import yaml
import logging
import utils 
import cloudscraper
import requests
from bs4 import BeautifulSoup
import difflib

# backend for the GUI 
                

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/utils-log.txt',filemode='w',encoding='utf-8', level=logging.DEBUG)



# Takes client version and url for addon to install
def install_addon(client,url):

    # Parse yml file and determine if there's an install location associated 
    logger.debug(f"install_addon({client}, {url})")
    with open("profile.yml") as f:
        data = yaml.safe_load(f)
        addon_dir = data["install-directories"]
        logger.debug(f'addon_dir[client] : {addon_dir[client]}')
        filename = url.rsplit('/', 1)[-1]
        logger.debug(f'name of addon to be installed : {filename}')
        
        install_path = os.path.join(addon_dir[client], filename)
        logger.debug(f"{install_path}")
        # Checks if the addon_dir[client] directory string is a real path
        
        if os.path.exists(addon_dir[client]): 
            # TODO : Install addon from url
            
            install_filename = os.path.join(addon_dir[client], filename)
            logger.debug(f"install_filename : {install_filename}")
            with open(install_filename, "wb") as f: 

                headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0.'}

                res = requests.get(url, headers=headers)
                logger.debug(f"retrieving : {url}\ninstalling as {install_filename} ")
                f.write(res.content)
            logger.debug("Downloading : {url} ")


            # Verify addon was actually installed 
            if os.path.isfile(install_filename):
                logger.debug(f"Addon successfully installed to : {install_filename}")



            



# returns the list of links given a URL 
class Scraper:

    def get(self,url):
        urls = []
        reqs = cloudscraper.create_scraper()
        html = reqs.get(url).content
        logger.debug(f"url: {url}")
        soup = BeautifulSoup(html,'html.parser')
        for link in soup.find_all('a'):
            urls.append(link.get('href'))

        return urls


# ex.) get_legacy_wow_addons("AtlasLoot", "vanilla")
def get_legacy_wow_addons(addon_name, client):

    url = f"https://legacy-wow.com/uploads/addons/{client}/{addon_name[0].lower()}"
    sc = Scraper() 
    res = sc.get(url)

    try:
        match = difflib.get_close_matches(addon_name, res)
        return url+"/"+match[0] # returns URL of addon to install 

    except IndexError as e: 
        logger.debug("No results found for the addon specified")



