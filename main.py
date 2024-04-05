#!/bin/env python3 
import os 
import sys
import requests
import urllib.request 
import json

# Script to install addons for older World of Warcraft Clients 
# Should be crossplatform between windows and linux 
# Read the profile.json file to find the install location for addons 



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



# Installs addons for a selected client with an addon of a specified name
def get_addons(client,name):
    # Parse json file and determine if there's an install location associated 
    with open("profile.json") as f:
        data = json.load(f)
        if not os.path.exists(data[client]): 
            print("NO path for selected client, please configure a path for this client ")

        else:
            print(f"path for {client} has been found at {data[client]}")






def main(): 

    client = '1.12.1'
    get_addons(client, '') 

    




if __name__ == '__main__':
    main()

