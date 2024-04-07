#!/usr/bin/env python3 
import json
import os
import sys
import logging
import pathlib
import tempfile
import shutil
import pprint
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logging/log.txt',filemode='w',encoding='utf-8', level=logging.DEBUG)


# generates imitation file structure and returns map of paths and the xpac associated
def generate_structure():
    # temporary directories test/{vanilla/ , turtle/, epoch/, tbc/, wotlk/}

    # also just playing around with  python3 os module here 

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
def test_populate_profile(dir):

    with open("profile.json") as f : 
        data = json.load(f)
        
        data["vanilla"] = dir["vanilla"]
        data["tbc"] = dir["tbc"]
        data["wotlk"] = dir["wotlk"]
        data["turtle"] = dir["turtle"]
        data["epoch"] = dir["epoch"]
    
        logger.debug(f'{data}')
        logger.debug("profile.json has been populated")
    



if __name__ == '__main__':
    paths = generate_structure()
    test_populate_profile(paths)
