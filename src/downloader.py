import cloudscraper
import difflib
from bs4 import BeautifulSoup

# Scrape legacy wow addons website for all downloadable links 
# client MUST be a string containing either ["vanilla", "turtle", "tbc", "wotlk"]


# Custom class so I can make new scrapers 
class Scraper:

    # returns the list of links 
    def get(self,url):
        urls = []
        reqs = cloudscraper.create_scraper()
        html = reqs.get(url).content
        print(f"url: {url}")
        soup = BeautifulSoup(html,'html.parser')
        for link in soup.find_all('a'):
            urls.append(link.get('href'))

        return urls


        
        
# returns urls to addons to install from legacy-wow.com
def get_legacy_wow_addons(addon_name, client):

    url = f"https://legacy-wow.com/uploads/addons/{client}/{addon_name[0].lower()}"

    # search addons using the first letter of it's name 
    # search by /xpac/first_letter 
    # for example : /uploads/addons/vanilla/a

    sc = Scraper() 
    res = sc.get(url)

    try:
        match = difflib.get_close_matches(addon_name, res)
        return url+"/"+match[0]

    except IndexError as e: 
        print("No results found for the addon specified")
   

    











