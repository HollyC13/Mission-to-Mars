# Import Splinter, BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemi(browser)
    }

    # Stop webdriver and return data
    browser.quit
    return data

# Create function
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and thenquit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ## JPL Space Images Featured Image

# Create function
def featured_image(browser):

    # Scrape image
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts

# Scrape Mars Facts
# Create function
def mars_facts():
    # Add try-txcept for error handling
    try:
        # Use 'read_html' to scrape first HTML table on webpage (galaxyfacts-mars.com) into Pandas DataFrame
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns to DataFrame
    df.columns=['description', 'Mars', 'Earth']

    # Set Description column as index
    df.set_index('description', inplace=True)

    # Convert DataFrame back to HTML, add bootstrap
    return df.to_html(classes="table table-striped table-bordered")

# Function to scrape the hemisphere data from Challenge file
def mars_hemi(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

        # 3. Write code to retrieve the image urls and titles for each hemisphere
    for hemi in range(4):
        hemispheres = {}
    
        # Find element and use it to navigate from main page to pages holding full-resolution images
        browser.find_by_css('h3')[hemi].click()

        # Parse the resulting html with soup
        html = browser.html
        hemi_soup = soup(html, 'html.parser')

        # Find image and extract <href>
        url_element = browser.find_link_by_text("Sample").first
        hemispheres["img_url"] = url_element["href"]

        # Find title and extract
        hemispheres['title'] = hemi_soup.find('h2', class_='title').text

        # Add extracted urls and titles to dictionary
        hemisphere_image_urls.append(hemispheres)

        # Navigate back to main page
        browser.back() 

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

# Tell Flask script is complete and "ready for action", print scraping results to terminal
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())