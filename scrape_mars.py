

import pandas as pd
import requests as rs
from bs4 import BeautifulSoup as bs
from splinter import Browser
import nbconvert


def scrape():
    # create place to store data
    scraped_dict = {}

    # ### NASA Mars News
    r = rs.get("https://mars.nasa.gov/news/")
    soup = bs(r.text, 'html.parser')
    title = soup.find('div', class_='content_title').find('a').get_text()
    p = soup.find('div', class_='rollover_description_inner').get_text()
    title =title[1:-1]
    p =p[1:-1]


    # ### JPL Mars Space Images - Featured Image
    browser = Browser('chrome', headless=False)
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    baseurl = 'https://www.jpl.nasa.gov'
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')
    img = soup2.find('a', attrs={'id': 'full_image', 'data-fancybox-href': True}).get('data-fancybox-href')
    featured_image_url= baseurl + img
    featured_image_url


    # ### Mars Weather
    browser = Browser('chrome', headless=False)
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html3 = browser.html
    soup3 = bs(html3, 'html.parser')
    twitter = soup3.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    tweet = twitter.get_text()


    # ### Mars Facts
    facts = pd.read_html('http://space-facts.com/mars/')
    df= facts[0]
    df.columns=['Measure','Qty']
    print(df.to_html())


    # ### Mars Hemisperes
    browser = Browser('chrome', headless=False)
    hemisperes = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisperes)
    html4 = browser.html
    soup4 = bs(html4, 'html.parser')

    Cerberus = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
    Schiaprelli = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'
    Syrtis = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
    Valles = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'

    img_urls =[Cerberus,Schiaprelli,Syrtis,Valles]
    imgTitles = soup4.find_all('h3')
    imgTitles = [h3.text.strip() for h3 in imgTitles]
    hemisphere_images = [{'title': imgTitle, 'img_url': img_url} for imgTitle, img_url in zip(imgTitles,img_urls)]

    # ## Step 2 - MongoDB and Flask Application
    scraped_dict = {"news_title":title, "news_text":p, "weather_tweet":tweet, "facts":df, "featured_image":featured_image_url, "hehemisphere_images":hemisphere_images
    }

    return scraped_dict

scrape

