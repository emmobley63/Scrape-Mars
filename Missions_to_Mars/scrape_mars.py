#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymongo
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[46]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[47]:


conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"


# In[48]:


response = requests.get(url)
soup = bs(response.text, 'html.parser')
soup


# In[49]:


result = soup.find('div', class_="slide")

news_title = result.find('div', class_="content_title").text

news_p = result.text

# news_p = result2.find('div', class_="list_text").text
# for result in results:
#     #title
#     news_title = result.find('a').text
    
#     news_p = result.find('div', class_="article_teaser_body").text
    
print(news_title, result)
print("-------------")
# print(result2)
print(news_p)


# In[50]:


splinter_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"


# In[51]:


browser.visit(splinter_url)


# In[13]:


browser.links.find_by_partial_text('FULL IMAGE').click()

html = browser.html
soup = bs(html, "html.parser")

image_url = soup.find('img', class_="fancybox-image")['src']

featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_url}"

print(featured_image_url)


# In[45]:


browser.quit()


# In[14]:


facts_url = "https://space-facts.com/mars/"


# In[15]:


tables = pd.read_html(facts_url)
tables


# In[23]:


type(tables)


# In[24]:


df = tables[0]
df.head(10)


# In[25]:


df.columns = ['Dimension', 'Measure']


# In[26]:


df.head()


# In[27]:


html_table = df.to_html(index=False, header=False)
print(html_table)


# In[65]:


mars_img_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
mars_url_local = "C:/Users/emmob/Downloads/Astropedia%20Search%20Results%20_%20USGS%20Astrogeology%20Science%20Center.html"


# In[37]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[68]:


browser.visit(mars_url_local)


# In[72]:


response = requests.get(mars_img_url).text

soup = bs(response, "html.parser")
soup


# In[73]:


img_href = soup.find_all('a', class_="itemLink product-item")
href_list = []
for x in img_href:
    href = x.get('href')
    href_list.append(href)
    print(href)


# In[74]:


hemisphere_image_urls = []
index_html = "https://astrogeology.usgs.gov"

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
# # for img in img_href:
# #     href = img.get('href')
# #     print(href)
# #     browser.click_link_by_href(href)

# # browser.links.find_by_css('span', class_="collapse::after").click()
# links = browser.links.find_by_href("/search/map/Mars/Viking/cerberus_enhanced")

# for x in links:
#     print(x)


# In[ ]:




