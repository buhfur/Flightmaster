import sys
import requests
import urllib.request 
import json
import downloader
from utils import install_addon

# Main script to hold the frontend components and for testing 




if __name__ == '__main__':
    url = downloader.get_legacy_wow_addons("AtlasLoot", "vanilla")
    install_addon("vanilla", url)
    
    





