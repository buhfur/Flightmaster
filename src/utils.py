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
import zipfile

# backend for the GUI 
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/utils-log.txt',filemode='w',encoding='utf-8', level=logging.DEBUG)



# returns the list of links given a URL 
class Scraper:


    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    ''' Method returns list of strings which are URLs to addons'''
    def get(self,url):
        urls = []
        html = self.scraper.get(url).content
        logger.debug(f"url: {url}")
        soup = BeautifulSoup(html,'html.parser')
        for link in soup.find_all('a'):
            urls.append(link.get('href'))

        return urls


    '''Method installs a zip file from a given url, filename is a full path'''
    def get_zip(self,filename, url):
        r = self.scraper.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        logging.debug(f"Installed ZIP file to : {filename}")




#TODO : ( OPTIONAL ) If the *.toc file and the folder of the addon don't match , change them so.

'''Takes path of zipfile , unzips the folder and removes the *.zip file

INPUT : addon_zip_path <str> 
'''
def unzip_addon(addon_zip_path):
    zf = zipfile.ZipFile(addon_zip_path)

    with zipfile.ZipFile(addon_zip_path, 'r') as zip_ref:
        install_directory =  os.path.dirname(addon_zip_path)
        zip_ref.extractall(install_directory)
        logger.debug(f"Unzipped {addon_zip_path} to {install_directory} ")

    #remove zip file 
    try:
        os.remove(addon_zip_path)
        logger.debug(f"Successfully removed {addon_zip_path}")
    except Exception as e :
        logger.debug(e)






''' Takes client version and url for addon to install , returns path where addon was installed.Installs zip file url references to the directory where the clients addon directory is located , or as shown in the profile.yml

INPUT : client <str> , url <str>
OUTPUT : install_filename <list>
'''


def install_addon(client,url):

    # Scraper instance for retrieving the zip file from the url given
    sc = Scraper()
    # Parse yml file and determine if there's an install location associated 
    logger.debug(f"install_addon({client}, {url})")
    with open("profile.yml") as f:
        data = yaml.safe_load(f)
        addon_dir = data["install-directories"]
        filename = url.rsplit('/', 1)[-1]
        # Checks if the addon_dir[client] directory string is a real path
        logger.debug(f'{os.path.relpath(filename)}')
        if os.path.exists(addon_dir[client]): 
            install_filename = os.path.join(addon_dir[client], filename)
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0.'}

            sc.get_zip(install_filename,url)
            logger.debug("calling sc.get_zip(url)")

            # Verify addon was actually installed 
            if os.path.isfile(install_filename):
                logger.debug(f"Addon successfully installed to : {install_filename}")

            return install_filename


''' returns the URL of a zipfile for the searched addon'''
def get_legacy_wow_addons(addon_name, client):

    url = f"https://legacy-wow.com/uploads/addons/{client}/{addon_name[0].lower()}"
    logger.debug(f"URL HERE :{url}")
    sc = Scraper() 
    res = sc.get(url)


    try:
        match = difflib.get_close_matches(addon_name, res)
        logger.debug(f'RETURN URL : {url+"/"+match[0]}')
        return url+"/"+match[0] # returns URL of addon to install 

    except IndexError as e: 
        logger.debug("No results found for the addon specified")



