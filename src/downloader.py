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


        
        
def get_legacy_wow_addons(addon_name, client):

    url = "https://legacy-wow.com/uploads/addons"
    scraper = Scraper()
    req = scraper.get(url)
    found_results = []
    
    # search addons in the current directoy 
    search_by_home = difflib.get_close_matches(addon_name,req)
    if search_by_home != " ":
        try:
            found_results.append(search_by_home[0])
        except IndexError as e:
            print("No results found searching by home")

    # search addons using the first letter of it's name 
    search_by_letter = difflib.get_close_matches(addon_name[0],req) 
    if search_by_letter != "":
        try:
            found_results.append(search_by_letter[0])
        except IndexError as e:
            print("No results found searching by letter")

    # search addons using the expansion the addon is associated with 

    search_by_xpac = difflib.get_close_matches(client,req) 
    if search_by_xpac != "":
        try:
            found_results.append(search_by_xpac[0])
            url = url+"/"+client # concatenate url with client 

            

            
        except IndexError as e:
            print("No results found searching by xpac")


    #print(f"Found the following results : {found_results}")  
   

    











