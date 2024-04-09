#!/usr/bin/env python3 
import json
import os
import sys
import pathlib
import tempfile
import shutil
import pprint
import yaml
import logging
import requests
from utils import *

from bs4 import BeautifulSoup


# generates imitation file structure and returns map of paths and the xpac associated
def generate_structure():
    parent_dir = os.path.join(tempfile.gettempdir(),"addons")

    v_path = pathlib.Path(f'{parent_dir}/vanilla/Interface/AddOns')
    t_path = pathlib.Path(f'{parent_dir}/tbc/Interface/AddOns')
    w_path = pathlib.Path(f'{parent_dir}/wotlk/Interface/AddOns')
    tu_path = pathlib.Path(f'{parent_dir}/turtle/Interface/AddOns')
    ep_path = pathlib.Path(f'{parent_dir}/epoch/Interface/AddOns')

    v_path.mkdir(parents=True, exist_ok=True)
    t_path.mkdir(parents=True, exist_ok=True)
    w_path.mkdir(parents=True, exist_ok=True)
    tu_path.mkdir(parents=True, exist_ok=True)
    ep_path.mkdir(parents=True, exist_ok=True)

    path_map = {"vanilla" : v_path, "tbc": t_path, "wotlk": w_path, "turtle": tu_path, "epoch":ep_path}

    for x in path_map.values():
        if not os.path.exists(x):
            logger.debug(f"{x} path wasn't created")
        else:
            logger.debug(f"path: {x} was created ")

    return path_map 
   
    



# Adds fake client install directories to profile.yml
def test_populate_profile(path_map):

    with open("profile.yml") as f : 
        profile_data = yaml.safe_load(f)
        data = profile_data['install-directories']

        if sys.platform.startswith("linux"):
            # Convert PosixPath to string ?
            for x in data.values():
                logger.debug(f"Keys : {x}")
                # Convert paths to strings and add to profile.yml
                data["vanilla"] = str(path_map["vanilla"])
                data["tbc"] = str(path_map["tbc"])
                data["wotlk"] = str(path_map["wotlk"])
                data["turtle"] = str(path_map["turtle"])
                data["epoch"] = str(path_map["epoch"])
       
        logger.debug(f"{data}")
        logger.debug("Added clients to profile.yml")

    with open("profile.yml", "w") as f:
        yaml.dump(profile_data, f, default_flow_style=False)
        logger.debug("Saved changes to profile.yml")



        

# Test function to install addons to a directory listed in profile.yml , returns path of addon install directory with filename
def test_install_addons():
    client="vanilla"
    url = get_legacy_wow_addons("AtlasLoot",client)
    return install_addon(client,url)


def test_get_legacy_addons(name):
    url = get_legacy_wow_addons(name,"vanilla")


def test_add_client_to_profile():
    # Generate test directory 

    t_path = pathlib.Path(f'{tempfile.gettempdir()}/something/AddOns')
    t_path.mkdir(parents=True, exist_ok=True)

    client = "vanilla"
    add_client_to_profile(client, str(t_path))

    with open("profile.yml") as f: 
        profile = yaml.safe_load(f)
        logger.debug(f'{profile}')

def test_reset_profile():
   reset_profile() 



# Test function to be later implemented in utils.py
def test_get_addon_desc(addon_name, client):

    url = f'https://legacy-wow.com/{client}-addons/{addon_name}'
    logger.debug(f"URL HERE :{url}")
    sc = Scraper()
    res = sc.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')

    # Prints out data from paragraph tags on the site 
    for x in soup.find('div', {'id': 'content-div'}).findAll('p'):
        return x.text

    




    
def main():
    '''
    paths = generate_structure()
    test_populate_profile(paths)
    test_get_legacy_addons()
    zip_path = test_install_addons()
    logger.debug(f"Returned addon install path: {os.path.dirname(zip_path)}")
    unzip_addon(zip_path)
   

    test_add_client_to_profile()
    '''

    test_get_addon_desc("Bagnon","vanilla")


if __name__ == '__main__':
    main()

