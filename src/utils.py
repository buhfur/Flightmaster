#!/bin/env python3 
import os 
import requests
import json
import cloudscraper
import difflib
from bs4 import BeautifulSoup
import logging
import urllib 
# Adds new client to profile.json , this should be done after initial setup as there should be at least one client configured 
def add_client_to_profile(client,client_path):
    # add the client path to the profile.json file
    with open("profile.json") as f:
        data = json.load(f)
        data[client] = client_path
        if os.path.exists(client_path):
            data[client] = client_path
            logger.debug(f'updated path for {client} to {client_path}')
        else: logger.debug("Could not add new path for client, please double check the path info")



                

'''
# Takes a client path and the client version , adds path to profile.json
def add_client_to_profile(client_version ,client_path):

    with open("profile.json") as f:
        data = json.load(f)
        if os.path.exists(data[client_version]): 
            # add client
            logger.debug("adding client")
        else:

            logger.debug("can't add client , path not valid")

'''


# Takes client version and url for addon to install
# client is a string = ["vanilla","turtle", "epoch", "tbc","wotlk"]
def install_addon(client,url):
    # Parse json file and determine if there's an install location associated 

    logger.debug(f"install_addon({client}, {url})")
    with open("profile.json") as f:
        data = json.load(f)
        logger.debug(f'{data}')
        filename = url.rsplit('/', 1)[-1]
        '''
        install_path = os.path.join(data[client], filename)
        logger.debug(f"{install_path}")
        if os.path.exists(data[client]): # checks to see if the directory in the profile exists 
            # TODO : Install addon from url
            urllib.request.urlretrieve(url)

        '''
        logger.debug(f"output of data[client]: {data} ")



            



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



