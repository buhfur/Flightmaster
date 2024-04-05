import requests
import urllib



# Script to download addons for multiple clients from different sources
# This is the toughest part of the backend of the app which is deciding where to source the addons from 

'''
now I could source it from the legacy-wow.com addons site which allows you to view the whole directory of where it's getting it's addons 
from , however some of them are inaccurate or unused as some may just have a link to the github page of these addons. 

So it will be challenged on whether to pull the addons from github or the legacy wow addons site. Github would make the most sense
however searching for them by using some github cli tool is unlikely. There may be other software under the same name as an addon and this 
would cause issues. 

What might be best is for me to compile an entire list of addons from github and manually add them there. The other option would be to 
grab the addons from that site. 

Or what I could do is host a server with the addons from legacy-wow.com and add in some of the special addons from github. To do this I could have a database that stores all the items and use that. Since on the flip side most addons from the older clients haven't received updates in years , so there may not be a need to accomadate those addons for older clients. However Vanilla + clients is where the issue begins. With project epoch releasing in the nearby 
future , people may be looking for addons that are custom to the version of the game they are playing , for instance turtle wow has it's own versions of 
pfQuest & Atlas loot. Therefore simply having one way references to addons might not be suitable for more custom clients. In this case having links to 
github would be best as these addons are more likely to receive newer updates. However the older addons for the untouched client may still work on custom
clients. 


I could also host a website for addon developers to submit their addons to in order to have them automatically added to the addon installer 


'''

