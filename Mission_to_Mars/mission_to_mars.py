from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)



# # Grab the latest news article from the website -'https://mars.nasa.gov/news/'
# ## store the title and paragraph description.

def scrape_latest_news():

    # set the URL 
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # print(soup.prettify())

    # Find the div class of 'slide'
    results = soup.body.find('div',class_='slide')

    # From here we can grab the description and the title of the latest news article.
    news_p = results.find('div',class_='rollover_description_inner').text
    news_title=results.find('div',class_='content_title').text

    # save this into a dictionary to store in MongoDB
    news = {'title' : news_title, 
            'text' : news_p}

    return (news)

# # Scrape the featured image from the website - https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
# ## Store the image and create an url to the image.

def scrape_feature_image():

    # initialize the browser
    browser = init_browser()

    # Go get the browser and click through to get the full image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Click on the 'Full Image' tag
    browser.click_link_by_partial_text('FULL IMAGE')

    # Click on the 'more info' tag.
    browser.click_link_by_partial_text('more info')

    # set up the page to be reviewed through Beauthiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    # Find the correct section to get the image
    results = soup.find('section',class_='content_page module').find('figure',class_='lede').find('a')['href']

    # We want the full URL
    feaured_image_url = {'url' : 'https://www.jpl.nasa.gov' + results}

    
    # Quite the browser after scraping
    browser.quit()

    return feaured_image_url


# # Scrape the Mars facts from https://space-facts.com/mars/
# ## Place them into a dataframe to store in an html file.

def scrape_mars_data():

    url = 'https://space-facts.com/mars/'

    # Read all the tables from the URL
    tables = pd.read_html(url)

    # Take the first table
    df = tables[0]

    # set the column names
    df = df.rename(columns= {0: '  ', 1 :'Mars Statistics'})
    df.set_index("  ", inplace=True)
    # Export the mars data into an html file
    df.to_html(open('Templates/mars_facts.html', 'w', encoding="utf-8"))

    # set the file name to data"
    data = 'mars_facts.html'

    return data


# # Scrape the website -  for the 4 urls images
# ## https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

def scrape_mars_hemi():
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # print(soup.prettify())
    # grab the list of hemispheres from the web page.
    results = soup.body.find_all('div',class_='item')

    browser = init_browser()

    # Initialze the variable to store the results
    hemisphere_image_urls = []

    # Loop through the items in the results variable.  Each one is an hemisphere.
    # Click on the link to get you to that page and pull the full image.

    for result in results:

        # Error handling
        try:
        
            # Identify and return title of listing
            title = result.find('div',class_='description').find('h3').text

            # set up the URL tl click to the next page
            browser.visit(url)
        
            time.sleep(1)

            # for each hemisphere click on the title / link to get to the next page.
            browser.click_link_by_partial_text(title)

            # grab the page to search through for the image
            html = browser.html
            soup = BeautifulSoup(html, 'lxml')

            # Grab the image from the page.
            link = soup.body.find('div',class_='container').find('div',class_='downloads').li.a['href']

            # Run only if title, and link are available
            if (title and link):

                # Dictionary to be inserted as a MongoDB document
                post = {
                    'title': title,
                    'url': link
                    }

                hemisphere_image_urls.append(post)
            
        except Exception as e:
            print(e)

        
        # This is repeated for each Hemisphere.

    
    # Quite the browser after scraping
    browser.quit()

    return hemisphere_image_urls



