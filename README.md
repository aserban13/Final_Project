# Final_Project
Final_Project for by SI 206 class 

# Data sources used
Using the PRAW wrapper, I was able to access Reddits data and use it to extract the data from Reddit. Reddit requires an OAUTH2  authentication. You are able to access Reddit's API by providing some information about your Reddit account including: the client secret, the client Id, your username and your password. 

To access this information, these are the steps the user must follow: 
1. the user must log into Reddit on https://www.reddit.com/prefs/apps 
2. Click on developer, and make an app
3. Then change the type to Script App. 
4. And then you should be provided the ClientId and ClientSecret to continue with authentication. 

For more help to find thing this information, follow this url: 
https://github.com/reddit-archive/reddit/wiki/OAuth2

# Any additional information needed to run:
Will need to put in the authentication for the program to work. 
In order to get access to the credentials, make sure you are not on campus (for some reason it won't let you access that page). 






# How the code is structured: 
The code starts at the top with the authentication to Reddit, in order to access the API data. And then what follows are the functions that help out with scraping data from the page (searching_data(), and caching_data()). 
After this is the DB class which consists of functions that create the database, and insert values. 

# Most important functions: 
The functions that are important to this code are: caching_data(search), the DB class which have three main functions [insert value(search) , access_query(search), access_url(search)]

The DB class is in charge of creating the database, inserting values in the table and running search values. 

Below is a brief description of each of these functions: 

# caching_data(search):
This is the official caching functions used later on to make these searches
Parameter: the search term, query
Returns: the cached data whether or not it was cached or not.


# insert value(search):
Add values in the table using caching_data
Parameter: A search term for it to gather data and add onto the two tables
Returns: Will insert data into two tables: Title and Details. No return


# access_query(search):
Finds the information (url and title) using the Title of the article
Parameter:a search key word
Returns: the results of all the outcomes of the search (url and Title)


# access_url(search):
Will look for the url that is linked to the tile of the subreddit
Parameter: the title of the subreddit
Returns: the url associated with the Title


