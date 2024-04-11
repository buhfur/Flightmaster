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

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/utils-log.txt',filemode='w',encoding='utf-8', level=logging.DEBUG)



''' 
Description : The scraper object can be used to get all links to addons on the legacy-wow.com website. The get() function returns a list of strings which are URL's to zip archives on the webpage 


Methods : 

    get(self, url) : 

        Description : Downloads a zipfile from legacy-wow.com , requires the use of cloudscraper to download.

        Arguments: 
            url:
                Type : <class 'str'>
                Description: Path to zip file in the form of a string
    
'''
class Scraper:


    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def get_addon_links(self,url):
        urls = []
        html = self.scraper.get(url).content
        logger.debug(f"url: {url}")
        soup = BeautifulSoup(html,'html.parser')
        for link in soup.find_all('a'):
            urls.append(link.get('href'))

        return urls


    def get_zip(self,filename, url):
        r = self.scraper.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        logging.debug(f"Installed ZIP file to : {filename}")

    # TODO : rewrite this function to inherit the get 
    def get(self,url):
        return self.scraper.get(url)



''' 
Description : Takes a path of the zipfile in the form of a string , extracts the zipfile in the directory it was installed. Finally , removes the zip file installed


Arguments : 

    addon_zip_path : 
        Type : <class 'str'>
        Description: Path to zip file in the form of a string
    
'''
def unzip_addon(addon_zip_path):

    zf = zipfile.ZipFile(addon_zip_path)
    install_directory =  os.path.dirname(addon_zip_path) 

    with zipfile.ZipFile(addon_zip_path, 'r') as zip_ref:
        zip_ref.extractall(install_directory)
        logger.debug(f"Unzipped {addon_zip_path} to {install_directory} ")


    # zip file without .zip extension
    folder_stem = pathlib.Path(addon_zip_path).stem 
    folder_path = os.path.join(install_directory, folder_stem)
    logger.debug(f'whole path : {folder_path}')
    
    # checks if file is a .toc file
    for file in os.listdir(folder_path):
        if file.endswith(".toc"):
            logger.debug(f'found {file}')
            file_stem = pathlib.Path(file).stem # zip name without .zip

            # Checks if folder name and TOC file differ
            if folder_stem != file_stem:
                logger.debug("Changing directory name to name of *.toc file")
            
                new_folder_name = os.path.join()
                os.rename(folder_path, os.path.join(install_directory, file_stem))


                logger.debug(f'renamed {folder_path} to {os.path.join(install_directory, file_stem) } ')


    #remove zip file 
    try:
        os.remove(addon_zip_path)
        logger.debug(f"Successfully removed {addon_zip_path}")
    except Exception as e :
        logger.debug(e)







''' 
Description : Takes client version and url for addon to install , returns path where addon was installed.Installs zip file url references to the directory where the clients addon directory is located , or as shown in the profile.yml


Arguments : 

    client : 
        Type : <class 'str'>
        Description: 
    url : 
        Type : <class 'str'>
        Description: 

'''
def install_addon(client,url):

    sc = Scraper()
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


''' 
Description: returns the URL of a zipfile for the searched addon

Arguments:

    addon_name : 
        Type : <class 'str'> 
        Description : String of the name of the addon to install 

    client : 
        Type : <class 'str'> 
        Description : String containing the name of the client to install the addon for , currently only : 'vanilla' , 'tbc', 'turtle', 'wotlk', 'epoch' is supported
'''
def get_legacy_wow_addons(addon_name, client):

    url = f"https://legacy-wow.com/uploads/addons/{client}/{addon_name[0].lower()}"
    logger.debug(f"URL HERE :{url}")
    sc = Scraper() 
    res = sc.get_addon_links(url)


    try:
        match = difflib.get_close_matches(addon_name, res)
        logger.debug(f'RETURN URL : {url+"/"+match[0]}')
        return url+"/"+match[0] # returns URL of addon to install 

    except IndexError as e: 
        logger.debug("No results found for the addon specified")


'''Adds world of warcraft client folder to profile.yml

Arguments : 

    client : 

        Type : <class 'str'>

        Description: String containing client version , for example "vanilla" for 1.12. HAS to match the string for the client in profile.yml.

    client_path : 

        Type : <class 'str'>

        Description : String that represents the clients installation directory, note that this is NOT the location of the addons, just the client directory itself


'''
def add_client_to_profile(client, client_path):

    with open("profile.yml") as f: 
        profile = yaml.safe_load(f)

        data = profile['install-directories']

        # Check if client version is valid
        if client in [*data]:
            logger.debug(f'Client : {client} is valid !')
            if os.path.exists(client_path):

                p_path = pathlib.Path(client_path).parent
                # Detect whether AddOns folder was provided
                if pathlib.PurePath(p_path).match("AddOns"):
                    logger.debug('AddOns directory was provided')
                    data[client] = client_path
                else:
                    logger.debug('Please include the AddOns directory in your path , you can ususally find it in the Interface/ folder where your World of Warcraft client was installed')

            else:
                logger.debug(f'directory {client_path} doesn\'t exist')
        else:
            logger.debug(f'Client : {client} is NOT valid ')



    with open("profile.yml", "w") as f:
        yaml.dump(profile, f, default_flow_style=False)
        logger.debug(f'Successfully added {client_path} to profile.yml')


'''
Description : Clears all directories out of the profile.yml file

'''
def reset_profile():

    with open('profile.yml') as f:

        profile = yaml.safe_load(f)
        install_directories = profile['install-directories']

        for x in install_directories.keys():
            install_directories[x] = ""

    with open('profile.yml', 'w') as f:

        yaml.dump(profile, f, default_flow_style=False)
        logger.debug(f'Reset profile.yml')
        logger.debug(f'{install_directories}')

'''

Description : Function that returns the description listed on the legacy-wow addons page for a specific addon. This function is meant to be use with the GUI when generating UI elements of available addons

Arguments:
    addon_name : 
        Type : <class 'str'>
    client:
        Type : <class 'str'>


Returns : <class 'str'>

'''

def get_addon_desc(addon_name, client):

    url = f'https://legacy-wow.com/{client}-addons/{addon_name}'
    logger.debug(f"URL HERE :{url}")
    sc = Scraper()
    res = sc.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    # Prints out data from paragraph tags on the site 
    for x in soup.find('div', {'id': 'content-div'}).findAll('p'):
        return x.text
