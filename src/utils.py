#!/bin/env python3 
import os 
import requests
import json


# Adds new client to profile.json , this should be done after initial setup as there should be at least one client configured 
def add_client_to_profile(client,client_path):
    # add the client path to the profile.json file
    with open("profile.json") as f:
        data = json.load(f)
        data[client] = client_path
        if os.path.exists(client_path):
            data[client] = client_path
            print(f'updated path for {client} to {client_path}')
        else:
            print("Could not add new path for client, please double check the path info")



# Takes client version and url for addon to install
# client is a string = ["vanilla","turtle", "epoch", "tbc","wotlk"]
def install_addon(client,url):
    # Parse json file and determine if there's an install location associated 

    with open("profile.json") as f:
        data = json.load(f)
        filename = url.rsplit('/', 1)[-1]
        install_path = os.path.join(data[client], filename)
        print(install_path)
        if os.path.exists(data[client]): 
            # TODO : Install addon from url

                

# Takes a client path and the client version , adds path to profile.json
def add_client_to_profile(client_version ,client_path):
    
    with open("profile.json") as f:
        data = json.load(f)
        if os.path.exists(data[client]): 
            # add client
            print("adding client")
        else:

            print("can't add client , path no valid")





