from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
import os
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)
    
def scrape():
    browser = init_browser()
    mars_dict ={}

    # Mars News URL 
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    news_beatifulsoup = BeautifulSoup(html, 'html.parser')
    # Most Recent Mars News
    news_title = news_beatifulsoup.find_all('div', class_='content_title')[0].text
    news_p = news_beatifulsoup.find_all('div', class_='article_teaser_body')[0].text

    # Mars Image 
    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html
    images_beautiful_soup = BeautifulSoup(html, 'html.parser')
    # Retrieve featured image link
    relative_image_path = images_beautiful_soup.find_all('img')[3]["src"]
    featured_image_url = jpl_nasa_url + relative_image_path

    # Mars weather 
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    weather_html = browser.html
    weather_beautifulsoup = BeautifulSoup(weather_html, 'html.parser')
    # Retrieve latest tweet with Mars weather info
    mars_weather = weather_beautifulsoup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text

    # Mars facts to be scraped, converted into html table
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    Facts_df = tables[2]
    Facts_df.columns = ["Description", "Value"]
    
    mars_html_table = Facts_df.to_html()
    mars_html_table.replace('\n', '')
    
    # Mars hemisphere name and image to be scraped
    USGS_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_beautifulsoup = BeautifulSoup(hemispheres_html, 'html.parser')
   

    all_mars_hemispheres = hemispheres_beautifulsoup.find('div', class_='collapsible results')
    mars_hemisphere = all_mars_hemispheres.find_all('div', class_='item')
    hemisphere_image_urls = []
    # Iterate through each hemisphere data
    for i in mars_hemisphere:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(USGS_url + hemisphere_link)        
        image_html = browser.html
        image_beautiful_soup = BeautifulSoup(image_html, 'html.parser')        
        image_link = image_beautiful_soup.find('div', class_='downloads')

        image_url = image_link.find('li').a['href']

        # Dictionary 
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url        
        hemisphere_image_urls.append(image_dict)

    # Mars 
    data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
    }

    return data

    if __name__ == "__main__":
        print(scrape_all())