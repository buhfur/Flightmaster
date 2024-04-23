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
import pyaml
import glob
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/utils-log.txt',filemode='w',encoding='utf-8', level=logging.DEBUG)


class Scraper:

    """ 
    Description
    -----------
    The scraper object can be used to get all links to addons on the legacy-wow.com website. The get() function returns a list of strings which are URL's to zip archives on the webpage 
   
    """


    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def get_addon_links(self,url):
        urls = []
        html = self.scraper.get(url).content
        soup = BeautifulSoup(html,'html.parser')
        for link in soup.find_all('a'):
            urls.append(link.get('href'))

        return urls

    """

    Description 
    -----------

    Downloads a zipfile from legacy-wow.com , requires the use of cloudscraper to download.

    Parameters
    -----------
    url: str

    """

    def get_zip(self,filename, url):
        r = self.scraper.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        logging.debug(f"Installed ZIP file to : {filename}")

    # TODO : rewrite this function to inherit the get 
    def get(self,url):
        return self.scraper.get(url)


def unzip_addon(addon_zip_path,client):

    """ 
    Description
    -----------

    Takes a path of the zipfile in the form of a string , extracts the zipfile in the directory it was installed. Finally , removes the zip file installed


    Parameters 
    -----------

    addon_zip_path : str

    Returns 
    -----------
    str or 0 if failed
        
    """

    if addon_zip_path is not None :

        zf = zipfile.ZipFile(addon_zip_path)
        install_directory =  os.path.dirname(addon_zip_path) 

        with zipfile.ZipFile(addon_zip_path, 'r') as zip_ref:
            zip_ref.extractall(install_directory)

        # zip file without .zip extension
        folder_stem = pathlib.Path(addon_zip_path).stem 
        folder_path = os.path.join(install_directory, folder_stem)

        try: 
            for file in os.listdir(folder_path):
                if file.endswith(".toc"):
                    file_stem = pathlib.Path(file).stem # zip name without .zip
                    # Checks if folder name and TOC file differ
                    if folder_stem != file_stem:
                        new_folder_name = os.path.join()
                        os.rename(folder_path, os.path.join(install_directory, file_stem))

        except Exception as e: 
            logger.debug(e)

        try:
            os.remove(addon_zip_path)
        except Exception as e :
            logger.debug(e)

    else:
        logger.debug("No client installation directory listed for {client}")
        return 0

def add_addon_to_profile(client, addon_name,install_filename):
 

    """
    Description 
    -----------

    Adds addon install directory to the users profile  , this function is meant to be called from install_addon().  

    This function also checks if an addon is already present in the users profile.yml

    """
    with open("profile.yml") as f:
        data = yaml.safe_load(f)
        installed_addons = data[1]["installed-addons"]
        for addon in installed_addons[client]:
            for addon_dict in addon:
                if addon_name in addon_dict.keys():
                    logger.debug('addon already present, skipping')
        else:
            installed_addons[client].append( { addon_name: str(pathlib.PurePath(install_filename).with_suffix(""))})


    with open("profile.yml",'w') as f:
        yaml.dump(data, f, default_flow_style=False)
        logger.debug("WIN: added addon to clients profile")



def install_addon(client,addon_name,url):

    """ 
    Description 
    -----------

    Takes client version and url for addon to install , returns path where addon was installed.Installs zip file url references to the directory where the clients addon directory is located , or as shown in the profile.yml


    Parameters 
    -----------

        client : str
        url : str

    Returns
    -----------
    str 
    """

    sc = Scraper()
    filename = url.rsplit('/', 1)[-1]
    with open("profile.yml") as f:
        data = yaml.safe_load(f)
        addon_dir = data[0]["install-directories"]

        if os.path.exists(addon_dir[client]): 
            install_filename = os.path.join(addon_dir[client], filename)
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0.'}
            sc.get_zip(install_filename,url)


            if os.path.isfile(install_filename):
                logger.debug(f"Addon successfully installed to : {install_filename}")
   
    
                add_addon_to_profile(client,addon_name,install_filename)
                return install_filename



def get_legacy_wow_addons(addon_name, client):

    """
    Description
    ------------

    returns the URL of a zipfile for the searched addon

    Parameters
    -----------

    addon_name : str
    client : str

    Returns 
    -----------

    str or int

    """

    url = f"https://legacy-wow.com/uploads/addons/{client}/{addon_name[0].lower()}"
    logger.debug(f'URL: {url}')
    sc = Scraper() 
    res = sc.get_addon_links(url) # contains list of urls to search
    try:
        match = difflib.get_close_matches(addon_name, res)
        logger.debug(f'MATCH: {match}')
        return url+"/"+match[0] # returns URL of addon to install 

    except IndexError as e: 
        return 0

def add_client_to_profile(client, client_path):

    """

    Description
    -----------
    Adds world of warcraft client folder to profile.yml

    Parameters  
    -----------

    client : str
    client_path : str
    
    Returns 
    -----------

    int : 1 if completed successfully
    """


    with open("profile.yml") as f: 
        profile = yaml.safe_load(f)
        data = profile[0]['install-directories']
        # Check if client version is valid
        if client in [*data]:
            if os.path.exists(client_path):
                p_path = pathlib.Path(client_path).parent
                # Detect whether AddOns folder was provided
                if pathlib.PurePath(p_path).match("Interface"):
                    data[client] = client_path

    with open("profile.yml", "w") as f:
        yaml.dump(profile, f, default_flow_style=False)

def get_addon_desc(addon_name, client):

    """

    Description
    ---------
    Function that returns the description listed on the legacy-wow addons page for a specific addon. This function is meant to be use with the GUI when generating UI elements of available addons

    Parameters
    ---------
        addon_name : str
        client: str


    Returns 
    --------
    tuple or int if failed

    """


    url = f'https://legacy-wow.com/{client}-addons/{addon_name}'
    sc = Scraper()
    res = sc.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    text = ""
    url = "" # url of picture 

    # Prints out data from paragraph tags on the site 
    try:

        for x in soup.find('div', {'id': 'content-div'}).findAll('p'):
            text = x.text

        # Gets the src url of the picture used 
        for x in soup.find('div', {'id': 'sidebar-div'}).findAll('a', {'class':'lightbox'}):
            url = f"{x['href']}"

    except AttributeError as e :
        return 0

    return (text, url)

    


def p_profile(profile='profile.yml'):
     
    """

    Function that pretty prints the contents of the profile.yml file 

    Input : 
        None 

    OUTPUT : 
        <class 'str'>

    """

    with open(profile) as f:
       yam = yaml.safe_load(f)
       print(pyaml.dump(yam))


def get_installed_addons():

    """

    Function that returns a list of all installed addons

    Input:
        None 

    Output :
        <class 'list'>

    """


    # iterate through all installed clients in profile.yml
    with open('profile.yml') as f:
        yam = yaml.safe_load(f)
        install_dir = yam[0]['install-directories']
        for x in install_dir.keys():
            if install_dir[x] != "":
                if os.path.exists(install_dir[x]):
                    # Search for installed addons in install_dir[x]
                    installed_addon_paths = [x for x in glob(f'install_dir[x]')]






