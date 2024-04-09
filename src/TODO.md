
# TODO markdown document of what needs to be implemented 


# Basic app flow 

1. add clients to your profile
2. search for addon 
3. install/remove addons 



# [x/] -  Sourcing the addons 


**This is the toughest part of the backend of the app which is deciding where to source the addons from**

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


**Trying option 1**

So far i've been able to get a list of all the addons on the adddons page on the legacy-wow.com website, the only tricks is that it's not too organized
addons are organized by name AND expansions,  therefore there may be some duplicates. Oh , and in addtion they are organized by first letter of their name too. So I can check just the addons page which WOULD work for classic as for some reason the classic addons are on the front page. However for this , I may need to search either in the alphabetically organized addons or the expansion they are associated with. The only problem is that some are missing from the alpha organized and the expansion. It flips, So I may just try to search both and hope it spits out the correct result. 


So far option 1 has been working , i've even made a cleaner solution to search for the addons. Instead , addons are ALWAYS searched using the first letter of the addons name AND the xpac it is asssociated with. This I believe should be 90% accurate of addons to search by.


For legacy wow addons , for tbc you might need to use the tbcClient/ directory 


# [x] -  Make testing python script 

Here i'm making a test script to automate some of the testing. For example I don't want to have to download all wow clients ( just yet ) for simply testing the profile.json file. Therefore i'm making a script which should make some directories that imitate the wow clients filestructure, which for most part, is unchanged for addons. 

All addons are always stored in 

> C:\something\wow\Interface\AddOns

or 

> /home/something/wow/Interface/AddOns 

# [ ] - FEATURE IDEA ( OPTIONAL ) Auto scan for private server clients 

Goal : implement a function in the utils.py to auto detect client versions on windows and linux systems.


# [x] - FEATURE IDEA ( OPTIONAL ) Change directory name to match the filename of the \*.toc 

Adding this would reduce the headache of having to change the folder name for some addons. World of Warcraft addons require that the parent foldername be identical to the filename of the \*.toc file , which describes basic information about the addon

# [x] - Add clients to json profile test 

Currently , i'm having an issue with an error in the test.py script. For some reason the json file is not saving the changes I make in the test script when the profile is populated. I feel like this issue is due to my lack of understanding of what data i'm trying to save and the methods to do so in the json module. Therefore i'm gonnna take a bit of time and use this oppertunity to learn a little more about the json module. Therefore toy.py will be the script i'm using to play around  


For some reason , when using json.dumps(s) in utils.py in the install_addon() function , the object returned from load() is a type string

I know I should use dumps() as i'm trying to get a python object deserialized. 

Note : I'm half tempted to just use yaml if I can't figure out this json shit 
Note : Could switch to yaml OR see if python can parse a \*.conf file

Note : now for some reason my logger module isn't producing a log file when for the test.py module when it was it was doing so previously....

I wonder if it's cause I have two loggers running , one in utils.py and one in test.py

I commented out the logger lines in utils.py and now the log in test.py is now working

**To fix this**

Just change logging.getLogger(__name__) to logging.getLogger("something") 

I think the main issue is that i'm importing the utils.py module , just gonna stick with 1 log file from now on using the logger in the utils.py script


Alright ! I got it working 

Now I gotta fix why yaml doesn't like adding PosixPaths to the profile, since the code keeps changing the format of the yaml file , i'm just going to use a spare profile.yml  named test\_profile.yml


Also adding a run.sh script since i'm tired of typing the whole run command out everytime. 

Finally got it working , nothing was wrong with the yaml , just needed to convert the paths from PosixPath objects to strings and now the file is being wrote to just fine. 

---
IMPORTANT NOTE : ON linux the paths for the install locations are PosixPath() objects. Remember this if you are having trouble installing the addon to the install location directory 
---



# [x] - Function to unzip the installed addons and remove the zip archives

Made the function for this already , also want to try changing the folder name to match the \*.toc file so there's no issues post installation

[x] - unzip files 
[x] - remove zip archives in addon installation directory 
[x] - check if directory name matches name of .toc file 



# [ ] - add client to profile function in utils.py

In this function I would like to detect whether the user provided the Interface/AddOns directory when attempting to add a client to profile.yml

My goal for this is to make the experience as easy as possible for the user , therefore the user should only have to provide the directory where they installed the client, rather than provide the Interface/AddOns directory.j

I'm not sure if it's confusing to allow the option to provide the parent OR the Interface/AddOns directory. The Addons directory would make sense but i'm worried some users might not be aware how addons are installed.

For the time being , the expected input is the directory where the addons are installed , so wow/Interface/AddOns

I'm assuming for the time being that all paths in the profile.yml are Path objects and not strings. 

Paths added to the profil.yml file should be strings.
# [ ] - Documentation goals 

[ ] - refactor variable names to make sense
[ ] - document each functions expected input and output in utils.py



