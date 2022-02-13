# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
# import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Scrape all function
def scrape_all():

    # print("Scrape All was reached")

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #the goal is to return the json that has all of the necessary data
    # Can be loaded into MongoDB
    
    # Get information from the news page
    news_title, news_paragraph = scrape_news(browser)

    # Build a dictionary
    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_paragraph,
        "featureImage": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": scrape_hemispheres(browser), 
        "lastUpdated": dt.datetime.now()
        }

    # Stop the webdriver
    browser.quit()

    # Display output
    return marsData

# Scrape the mars news page
def scrape_news(browser):
    # Go to Mars NASA news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    # Grabs the title
    news_title = slide_elem.find('div', class_='content_title').get_text()

    # Grabs the paragraph
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    # Return the title and paragraph
    return news_title, news_p

# Scrape through the featured image page
def scrape_feature_img(browser):
   
    # Visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click on full image button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Find the image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# Scrape through the facts page
def scrape_facts_page(browser):

    # Visit url
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    fact_soup = soup(html, 'html.parser')

    # Find the facts location
    factsLocation = fact_soup.find('div', class_="diagram mt-4")
    factsTable = factsLocation.find('table') # Grab the hteml code for the fact table

    # Create an emtpy string
    facts = ""

    # Add the text to the empy string then return
    facts += str(factsTable)

    return facts

# Scrape throught the hemisphere pages
def scrape_hemispheres(browser):

    #Base url
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Setup loop 
    for i in range(4):

        #Loops through each of the pages
        #hemisphere info dictionary
        hemisphereInfo = {}
    
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
    
        # Next, we find the Sample image anchor tag and extract the href
        sample = browser.links.find_by_text('Sample').first
        hemisphereInfo['img_url'] = sample['href']
    
        # Get Hemisphere title
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text

        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphereInfo)
    
        # Finally, we navigate backwards
        browser.back()

    # Return the hemisphere urls with the titles
    return hemisphere_image_urls

# Setup as a flask app
if __name__ == "__main__":
    print(scrape_all())

