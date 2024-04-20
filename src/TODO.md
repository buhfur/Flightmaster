
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



# [x] - add client to profile function in utils.py

In this function I would like to detect whether the user provided the Interface/AddOns directory when attempting to add a client to profile.yml

My goal for this is to make the experience as easy as possible for the user , therefore the user should only have to provide the directory where they installed the client, rather than provide the Interface/AddOns directory.j

I'm not sure if it's confusing to allow the option to provide the parent OR the Interface/AddOns directory. The Addons directory would make sense but i'm worried some users might not be aware how addons are installed.

For the time being , the expected input is the directory where the addons are installed , so wow/Interface/AddOns

I'm assuming for the time being that all paths in the profile.yml are Path objects and not strings. 

Paths added to the profil.yml file should be strings.

# [ ] - function to return data about each addon available to be downloaded
This function is meant to be used with the GUI to generate UI elements of all possible addons to be installed. This is similar to how CurseForge presents you with popular addons to download in the UI.

To do this , I will make a function get_available_addons(url) which takes a url string as input and displays info about the addon. 

- Find URL for addon page using the zipfile install link 
- Scrape Addon page for description
- return dictionary of addons name , page url , install url , and description
- addons are searched by the client they are apart of , for the frontend i'm thinking of a singular tab for each client. Therefore the "vanilla" tab will show all available 1.12.1 addons to install and so forth

For example let's take the bagnon addon: 

**The ZIP link for the addon is:**

`https://legacy-wow/uploads/addons/vnailla/b/Bagnon.zip`

**The addon page for the addon is :**

https://legacy-wow.com/vanilla-addons/bagnon


So it's safe to assume that all addon pages are going to use the "https://legacy-wow.com/vanilla-addons/" prefix


It looks like the only tag of it's type on the page

The addon description is contained within a \<p\> tag on the page

After checking it looks like the site always uses the  

Schema for searching for url data 

`https://legacy-wow.com/{client}-addons/{addon-name} `


# [ ] - (OPTIONAL) rewrite "Scraper" class to directly inherit the cloudscraper class 

requires rewrite of the class


# [ ] - GUI time , the frontend of the app 

I'm not entirely certain the app is ready for a user interface , but given how the app now has the functionality of adding users profiles, and installing addons from the legacy-wow.com site to install these addons. I believe the app is now ready for an interface to do so. For the time being of course the interface won't be pretty , all it needs to do right now is work. I will develop the interface for the linux users on my spare VM on my hypervisor and develop the windows portion on my windows distro at home. 

But now comes the greatest question , which UI framework am I gonna use ?  

The only shitty thing is that I now have to switch work environments to the terminal on my spare vm lol


Ok  so far i've got the base layout setup and ready to go , now I just need
to piece the logic together and interweave it with the existing codebase.  

First objective is to get the "Adding clients" section of the ui done and over with. For this all that needs to happen is I should be able to select one of the radio buttons and a folder selection prompt should appear. A message should specifiy that the directory HAS to be the Interface AddOns folder of the client or else addons are going to installed in a location that might get lost to the user and never be seen again....Therefore I would like to avoid this. Alot of this frontend work has me thinking entirely differently. Writing the code for this project so far has been a blast from the past for sure, yet now I actually need to be thinking of how the user is actually going to use my program. It's very new to me and i'm sure I have alot to learn. However for the time being I feel like a monkey hacking together UI elements to make something at least 10% usable 


# [ ] - Documentation goals 

[ ] - refactor variable names to make sense
[ ] - document each functions expected input and output in utils.py


---

# Frontend TODO 



[x] - find out why fs[0] client path in add_client_button and add_client_to profile, for some reason the path supplied is always a slash "/" and I have no idea why. Try to figure this out when you're sober.
[x] - button that allows you to select the install location for clients 
[x] - Populate table with addon name and description and download using button

[x] -  Fix the scrollBar from  overlapping the search bar

[x] - Change addon widget to look more user friendly

[ ] - Add layout with widgets that present info about already installed clients

[ ] - Change radio buttons to dropdown selection
# Backend todo 

[ ] - use a placeholder photo in the event an addon picture cannot be found

[ ] - get intall button working for the searched addon on the addon widget

[ ] - Write replacement function for get\_addons\_desc() to pull the description text from the smaller description text on the searched addons page 


[ ] - find out whatever is going on with the difflib search in  addonWidget


# [ ] - Add addon to client in GUI 


Ok for some reason i've noticed that some data is not being  processed as well in other parts of the application. It seems like there is some code I didn't test or some input I was not expecting.  I will note here what the issue is as I investigate


When testing the install\_addon() function , it seems like the app isn't seeing the path listed for the user in the temporary populated profile.yml. Ah the  reason for this is my install location for the addons in my profile.yml. For testing i'm currently putting all directories in the /tmp/ directory on linux. A quick run of the generate\_structure function should do the trick.

Yep, that did the trick.

I wonder if that's why the button hasn't been working this entire time....

Nope , for some reason I keep getting an error from difflib. Saying there's a NoneType being passed into the function. Which doens't make sense as I have a test script which feeds the function the same input that the GUI would give...

Just tested it again , except this time with pfQuest , it installs without issue. I have no idea where  this difflib error is coming from. I've triggered it in the past using the .lower()  function on a string. I wonder if  there's anywhere in the app where  this is happening 

I just noticed the expansion is upper case when it's supposed to be lowercase, gonna  lower it and see what happens

I do believe this may be the cause , after doing that i'm now starting to get KeyError's from other function ,referencing "Vanilla"

**FIX: changing the expansion name to lowercase was the solution here

Now I just gotta verify that the  addon installed , and then unzip the zip file , unless  this just did it for me 
