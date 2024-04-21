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

    # zip file without .zip extension
    folder_stem = pathlib.Path(addon_zip_path).stem 
    folder_path = os.path.join(install_directory, folder_stem)

    # checks if file is a .toc file
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

    #remove zip file 
    try:
        os.remove(addon_zip_path)
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



Returns: 
    str:filename -> returns the filename of the addon downloaded 
'''
def install_addon(client,addon_name,url):

    sc = Scraper()
    filename = url.rsplit('/', 1)[-1]
    installed = False
    with open("profile.yml") as f:
        data = yaml.safe_load(f)
        addon_dir = data["install-directories"]
        # Checks if the addon_dir[client] directory string is a real path
        if os.path.exists(addon_dir[client]): 
            install_filename = os.path.join(addon_dir[client], filename)
            #logger.debug(f'FILENAME: {pathlib.PurePath(install_filename).with_suffix("")}')
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0.'}

            sc.get_zip(install_filename,url)

            # Verify addon was actually installed 
            if os.path.isfile(install_filename):
                logger.debug(f"Addon successfully installed to : {install_filename}")
                #TODO: add installed addons  name and path to profile.yml
                installed = True

            return install_filename

        else:
            logger.debug("Path does not exist")
    
        # Adds the addon to the profile under the installed-addons

    with open("profile.yml", "w") as f:
        data = yaml.safe_load(f)
        clients = data['installed-addons']
        clients[client] = { addon_name: pathlib.PurePath(install_filename).with_suffix("")}


''' 
Description: returns the URL of a zipfile for the searched addon

Arguments:

    addon_name : 
        Type : <class 'str'> 
        Description : String of the name of the addon to install 

    client : 
        Type : <class 'str'> 
        Description : String containing the name of the client to install the addon for , currently only : 'vanilla' , 'tbc', 'turtle', 'wotlk', 'epoch' is supported

    Returns : 

        Returns string of a URL to a zip file , this string will should be passed to install_addon(client, url) with the string name of the client given and the url to download the file from

        if 0 is returned the search failed 
'''
def get_legacy_wow_addons(addon_name, client):

    url = f"https://legacy-wow.com/uploads/addons/{client}/{addon_name[0].lower()}"
    sc = Scraper() 
    res = sc.get_addon_links(url) # contains list of urls to search
    try:
        match = difflib.get_close_matches(addon_name, res)
        return url+"/"+match[0] # returns URL of addon to install 

    except IndexError as e: 
        return 0


'''

Adds world of warcraft client folder to profile.yml

Arguments : 

    client : 

        Type : <class 'str'>

        Description: String containing client version , for example "vanilla" for 1.12. HAS to match the string for the client in profile.yml.

    client_path : 

        Type : <class 'str'>

        Description : String that represents the clients installation directory, note that this is NOT the location of the addons, just the client directory itself
Returns : 

    int : 0 or 1 , 1 if completed successfully

'''
def add_client_to_profile(client, client_path):

    with open("profile.yml") as f: 
        profile = yaml.safe_load(f)
        data = profile['install-directories']
        # Check if client version is valid
        if client in [*data]:
            if os.path.exists(client_path):
                p_path = pathlib.Path(client_path).parent
                # Detect whether AddOns folder was provided
                if pathlib.PurePath(p_path).match("Interface"):
                    data[client] = client_path

    with open("profile.yml", "w") as f:
        yaml.dump(profile, f, default_flow_style=False)



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

'''

Description : Function that returns the description listed on the legacy-wow addons page for a specific addon. This function is meant to be use with the GUI when generating UI elements of available addons

Arguments:
    addon_name : 
        Type : <class 'str'>
    client:
        Type : <class 'str'>


Returns: 
    <class 'tuple'> (text, url) 

    text : Text description of the addon searched 
    url : url of the image to be used 

if 0 is returned this means no description was able to be fetched

'''

def get_addon_desc(addon_name, client):

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

    


'''

Function that pretty prints the contents of the profile.yml file 

Input : 
    None 

OUTPUT : 
    <class 'str'>

'''


def p_profile(profile='profile.yml'):
    with open(profile) as f:
        yam = yaml.safe_load(f)
        print(pyaml.dump(yam))


'''

Function that returns a list of all installed addons

Input:
    None 

Output :
    <class 'list'>


'''


def get_installed_addons():

    # iterate through all installed clients in profile.yml
     with open('profile.yml') as f:
            yam = yaml.safe_load(f)
            install_dir = yam['install-directories']
            

            for x in install_dir.keys():
                if install_dir[x] != "":
                    if os.path.exists(install_dir[x]):
                        # Search for installed addons in install_dir[x]
                            installed_addon_paths = [x for x in glob(f'install_dir[x]')]
                        





