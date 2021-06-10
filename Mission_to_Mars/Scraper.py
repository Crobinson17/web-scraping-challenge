from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import requests
import pymongo
import os
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)
    
    browser = init_browser()
   
def mars_news(browser):
    # Mars News URL 
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    
    article = soup(html, 'html.parser')
    # Most Recent Mars News
    article = soup.find("div", class_="list_text")
    news_title = article.find_all('div', class_='content_title')[0].text
    news_p = article.find_all('div', class_='article_teaser_body')[0].text
    news_date = article.find("div", class_="list_date").text


def featured_image(browser):    
    # Mars Image 
    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html
    browser.visit(images_url)
#Full Image
    full_image = browser.find_by_tag('button')[1]
    full_image.click()


    html = browser.html

    images_soup = soup(html, 'html.parser')
    
    
def Mars_Facts(): 
    # Mars facts to be scraped, converted into html table
    facts_url = 'http://space-facts.com/mars/'
    tables = pd.read_html(facts_url)

    Facts_df = tables[2]
    Facts_df.columns = ["Description", "Value"]
    
    mars_html_table = Facts_df.to_html()
    mars_html_table.replace('\n', '')
    
def hemisphere(browser):
    
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    hemisphere_image_urls = []

    # Get a List of All the Hemisphere
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        # Find Element on Each Loop
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()
    return hemisphere_image_urls

def scrape_hemisphere(html_text):
    hemisphere_soup = soup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere


def scrape_all():


    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)
    
    browser = init_browser()
    browser = init_browser()
    news_title, news_paragraph = mars_news(browser)


    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image,
        "fact_table": str(Mars_Facts),
        "hemisphere_images": hemisphere(browser)
    }

    return data

    if __name__ == "__main__":
        print(scrape_all())