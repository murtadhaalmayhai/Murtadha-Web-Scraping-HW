from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import time
import re

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

# NASA Mars News
def mars_news_title():
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = bs(html, "html.parser")
    latest_news_container = soup.find('div', class_= "image_and_description_container")
    latest_news_text = latest_news_container.find('div', class_ ="list_text")
    news_title = latest_news_text.find('div', class_ = 'content_title').text

    return news_title

def mars_news_p():
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = bs(html, "html.parser")
    latest_news_container = soup.find('div', class_= "image_and_description_container")
    latest_news_text = latest_news_container.find('div', class_ ="list_text")
    news_p = latest_news_text.find('div',class_= 'article_teaser_body').text

    return news_p

# JPL Mars Space Images - Featured Image
def mars_featured_image():
    url = 'https://www.jpl.nasa.gov'
    images = '/spaceimages/?search=&category=Mars'
    browser.visit(url+images)
    time.sleep(3)

    button = browser.find_by_id('full_image')
    button.click()
    html = browser.html
    time.sleep(3)
    soup = bs(html, 'html.parser')
    featured_image = soup .find('a', class_= "button fancybox")['data-fancybox-href']
    featured_image_url = url + featured_image

    return featured_image_url

# Mars Weather
def mars_weather():
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find(string=re.compile("Sol"))
    mars_weather

    return mars_weather

# Mars Facts
def mars_profile():
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')
    table = soup.find('table')

    mars_planet_profile = pd.read_html(str(table))[0]
    mars_planet_profile = mars_planet_profile.rename(columns={0: 'Description', 1: 'Value'}).set_index('Description')
    mars_profile_html = mars_planet_profile.to_html(index = True, header =True)

    return mars_profile_html

# Mars Hemisphere
def mars_hemispheres():
    url = 'https://astrogeology.usgs.gov'
    enhanced = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url+enhanced)
    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')
    hemispheres = soup.find_all('div', class_ = 'item')

    hemisphere_image_urls = [] 

    for hemisphere in hemispheres:
    
        hemisphere_title = hemisphere.find('h3').text
        title = hemisphere_title.replace('Enhanced','')
    
        hemisphere_url = hemisphere.find('a')['href']
    
        browser.visit(url + hemisphere_url)
        html = browser.html
        soup = bs(html, 'html.parser')
    
        downloads = soup.find('div', class_='downloads')
        image_url = downloads.find('a')['href']
    
        hemisphere_image_urls.append({'title': title,'image_url': image_url})

    return hemisphere_image_urls

# Scrape Function
def scrape():
    mars_data={}

    mars_data["news_title"] = mars_news_title()
    mars_data["news_p"] = mars_news_p()
    mars_data["featured_image_url"] = mars_featured_image()
    mars_data["weather"] = mars_weather()
    mars_data["profile"] = mars_profile()
    mars_data["hemisphere_urls"] = mars_hemispheres()

    return mars_data