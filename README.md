# web-scraping-challenge

For this project I wanted to create a webpage where you could find all the latest news on Mars. I used a few different websites to scrape the info and compile it onto the web-scraping-challenge page:

https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest

https://space-facts.com/mars/

https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html

In order to scrape the information I used a python application called "scrape_mars.py". In this application I define a function called scrape that uses Splinter and BeautifulSoup to read the html and css on the websites and pull my desired information. Within my function "scrape()" I stored all my scraped information into a dictionary called Mars_dict. In my python function "app.py" I import the scrape() function and Mars_dict from scrape_mars.py. It utilizes pymongo to store the dictionary into MongoDB as a nonrelational database and it uses flask to render my html page with the Mars_db in MongoDB.

For the front-end my html page uses CSS and Bootstrap to create a more asthetically appealing page. Our "Scrape New Data" button calls the scrape() function to find new data and add it to the database.
