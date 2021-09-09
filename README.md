# sea-shanty-api
This is a public API that allows users to receive titles and lyrics from a large collection of sea shanties, and use them in their projects, programs or for whatever reason!

# Homepage
The API homepage can be found at http://sea-shanty-api.herokuapp.com. Feel free to head over there and find some cool shanties!

# Database
The collection of sea shanties is deployed on a MongoDB database. It was created by scraping the website http://mainsailcafe.com which contains the lyrics to hundreds of sea shanties. The scraping was done with a Python script, using mainly the 'requests' and 'BeautifulSoup' modules. The script can be found in this repository. Since the lyrics on the website are not all formatted in the same way HTML-wise, some manual cleaning and tweaking of the database was required after the initial scrape.

# What this project contains
Working on this project helped me explore many technologies and languages:
* JavaScript + Node.js - The API homepage and endpoints were created using Node.js and Express.js
* HTML + CSS - I created and designed the homepage from scratch using these.
* Python - Web scraping, creating the shanty database and further functionality testing of API calls
* Git, GitHub and Heroku - Tracking changes and updates to the code, and deploying the API online in order to make it available to the world
* MongoDB - Deploying the created shanty database online for querying by the API
