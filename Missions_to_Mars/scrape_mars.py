
import pymongo
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template


app = Flask(__name__)

@app.route("/scrape")
def scrape():

    # Starting up the Browser

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[3]:


    # Establishing the MongoDB connection

    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)

    # url to scrape newest news title and description

    url = "https://mars.nasa.gov/news/"


    # In[7]:


    # Open browser and convert into html for beautiful soup to read/parse

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')


    # In[9]:


    # Find the slide class to then pull the text from the content_title and article_teaser_body

    result = soup.find('div', class_="slide")

    news_title = result.find('div', class_="content_title").text

    news_p = soup.find('div', class_="article_teaser_body").text


    # In[18]:


    # New url to scrape and click through

    splinter_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"


    # In[19]:


    # Open splinter_url in the browser

    browser.visit(splinter_url)


    # In[20]:


    # Finding the featured image url 
    # Click the FULL IMAGE text button

    browser.links.find_by_partial_text('FULL IMAGE').click()

    # Open browser and convert into html for beautiful soup to read/parse

    html = browser.html
    soup = bs(html, "html.parser")

    # finding the src of the image by it's class

    image_url = soup.find('img', class_="fancybox-image")['src']

    featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_url}"


    # In[21]:


    # New url to scrape

    facts_url = "https://space-facts.com/mars/"


    # In[22]:


    # Using pandas to read in the data as a list

    tables = pd.read_html(facts_url)
    tables


    # In[24]:


    # Creating a dataframe from the first item in the tables list

    df = tables[0]
    df.head(10)


    # In[25]:


    # Rename the columns

    df.columns = ['Description', 'Mars']

    # In[27]:


    # Converting the tables to a dataframe

    html_table = df.to_html(index=False, header=True)


    # In[27]:


    # New urls to scrape. One local file of the html for splinter

    mars_img_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    mars_url_local = "C:/Users/emmob/Downloads/Astropedia%20Search%20Results%20_%20USGS%20Astrogeology%20Science%20Center.html"


    # In[30]:


    # Open browser and convert into html for beautiful soup to read/parse

    browser.visit(mars_url_local)


    # In[31]:


    response = requests.get(mars_img_url).text

    soup = bs(response, "html.parser")


    # In[33]:


    # Finding all of the image url's and appending them to href_list

    img_href = soup.find_all('a', class_="itemLink product-item")
    href_list = []
    for x in img_href:
        href = x.get('href')
        href_list.append(href)
        print(href)


    # In[34]:


    # New list to append dictionaries to and base index url

    hemisphere_image_urls = []
    index_html = "https://astrogeology.usgs.gov"

    # Looping through each page of the photo's urls to pull their src and title

    for x in href_list:
        url= f"{index_html}{x}"
        browser.visit(url)
        browser.click_link_by_id("wide-image-toggle")
        fig_expanded_url = browser.url
        response1 = requests.get(fig_expanded_url).text
        soup = bs(response1, "html.parser")
        
        fig1_src = soup.find('img', class_="wide-image").get('src')
        
        fig_src = f"{index_html}{fig1_src}"
        
        fig_title = soup.find('h2').text
        title = fig_title[:-9]
        
        hemisphere_image_urls.append({"titles": title, "img_url": fig_src})

    print(hemisphere_image_urls)


    # In[35]:


    # Close the browser

    browser.quit()

if __name__ == "__main__":
    app.run(debug=True)