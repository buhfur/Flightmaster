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
import utils 


logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/log.txt',filemode='w',encoding='utf-8', level=logging.DEBUG)



# json object that represents the schema for the profile 

'''
profile_obj = {


        "client-addon-install-directories":[ 
        "vanilla": {
            "install-dir": ""
            },
        "tbc": {
            "install-dir": ""
            },
        "wotlk": {
            "install-dir": ""
            },
        "turtle": {
            "install-dir": ""
            },
        "epoch": {
            "install-dir": ""
            }

        ]
}
'''
# generates imitation file structure and returns map of paths and the xpac associated
def generate_structure():
    # temporary directories test/{vanilla/ , turtle/, epoch/, tbc/, wotlk/}
    # create directories in the temp windows directory
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

    logger.debug(f"path of vanilla : {v_path}")
    for x in path_map.values():
        if not os.path.exists(x):
            logger.debug(f"{x} path wasn't created")
        else:
            logger.debug(f"path: {x} was created ")

    return path_map 
   




    



# Adds fake client install directories to profile.yml
def test_populate_profile(path_map):


    with open("test_profile.yml") as f : 
        profile_data = yaml.safe_load(f)
        data = profile_data['install-directories']
        
        data["vanilla"] = path_map["vanilla"]
        data["tbc"] = path_map["tbc"]
        data["wotlk"] = path_map["wotlk"]
        data["turtle"] = path_map["turtle"]
        data["epoch"] = path_map["epoch"]

        if sys.platform.startswith("linux"):
            # Convert PosixPath to string ?
            for x in data.keys():
                logger.debug(f"Keys : {x}")
    
       
        logger.debug(f"{data}")
        logger.debug("Added clients to profile.yml")

'''
    with open("profile.yml", "w") as f:
        yaml.dump(profile_data, f, default_flow_style=False)
'''



        

# Test function to install addons to a directory listed in profile.yml
def test_install_addons():

    client="vanilla"
    url = utils.get_legacy_wow_addons("AtlasLoot",client)
    utils.install_addon(client,url)


    
def main():
    paths = generate_structure()
    test_populate_profile(paths)
    #test_install_addons()


if __name__ == '__main__':
    main()
