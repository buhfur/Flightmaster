#!/usr/bin/env python3 
import json
import os
import sys
import logging
import pathlib
import tempfile
import shutil
import pprint
import utils 

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/log.txt',filemode='w',encoding='utf-8', level=logging.DEBUG)


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
   




    



# Populates the profile.json file using temporary directories, takes map of addon install paths as input
def test_populate_profile(path_map):

    w_data = ""

    with open("profile.json") as f : 

        logger.debug(f'{type(f)}')
        data = json.load(f)
        #w_data = str(data)
        '''
        data["vanilla"] = path_map["vanilla"]
        data["tbc"] = path_map["tbc"]
        data["wotlk"] = path_map["wotlk"]
        data["turtle"] = path_map["turtle"]
        data["epoch"] = path_map["epoch"]
    
        '''
        logger.debug("profile.json has been populated")
        f.close()
        logger.debug("f is now closed")

    
    fp = open("profile.json",'w')
    json.dump(w_data,fp) # save changes to json file 
    logger.debug("Changes were saved to file")
    
    fp.close()

        

def test_install_addons():

    client="vanilla"
    url = utils.get_legacy_wow_addons("AtlasLoot",client)
    utils.install_addon(client,url)


    


if __name__ == '__main__':
    paths = generate_structure()
    test_populate_profile(paths)
    test_install_addons()
