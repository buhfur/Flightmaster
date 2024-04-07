
# TODO markdown document of what needs to be implemented 


# Basic app flow 

1. add clients to your profile
2. search for addon 
3. install/remove addons 



# [x/] -  Sourcing the addons 


*This is the toughest part of the backend of the app which is deciding where to source the addons from *

Now I could source it from the legacy-wow.com addons site which allows you to view the whole directory of where it's getting it's addons 
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

I didn't think of this either , but I could also source the addons from newer addon sites like felbyte 


[ ] - attempt to scrape the legacy-wow.com/uploads/addons page for links to addons to install ,  could use beautifulsoup4 and requests in a python 
script to do this real quick. 


Here I will list a few approaches on where to get the addon install links from 

1. Scraping other sites that have addons listed, compiling a list or urls which the client will use to source the addons from. 
2. Manually add links from github of popular addons,  which would work but this is very inefficient


## Trying option 1 : 

So far i've been able to get a list of all the addons on the adddons page on the legacy-wow.com website, the only tricks is that it's not too organized
addons are organized by name AND expansions,  therefore there may be some duplicates. Oh , and in addtion they are organized by first letter of their name too. So I can check just the addons page which WOULD work for classic as for some reason the classic addons are on the front page. However for this , I may need to search either in the alphabetically organized addons or the expansion they are associated with. The only problem is that some are missing from the alpha organized and the expansion. It flips, So I may just try to search both and hope it spits out the correct result. 


So far option 1 has been working , i've even made a cleaner solution to search for the addons. Instead , addons are ALWAYS searched using the first letter of the addons name AND the xpac it is asssociated with. This I believe should be 90% accurate of addons to search by.




# [ ] -  Make testing python script 

Here i'm making a test script to automate some of the testing. For example I don't want to have to download all wow clients ( just yet ) for simply testing the profile.json file. Therefore i'm making a script which should make some directories that imitate the wow clients filestructure, which for most part, is unchanged for addons. 

All addons are always stored in 

> C:\something\wow\Interface\AddOns

or 

> /home/something/wow/Interface/AddOns 



# [ ] - FEATURE IDEA ( OPTIONAL ) Auto scan for private server clients 


- implement a function in the utils.py to auto detect client versions on windows and linux systems


# [ ] - FEATURE IDEA ( OPTIONAL ) Change directory name to match the filename of the \*.toc 

Adding this would reduce the headache of having to change the folder name for some addons. World of Warcraft addons require that the parent foldername be identical to the filename of the *.toc file , which describes basic information about the addon
