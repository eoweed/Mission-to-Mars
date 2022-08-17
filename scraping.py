# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
# from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
import pandas as pd    # to use for mars facts scraping
import datetime as dt    # to show when the code was run in mongo

# Connect scraping results to Mongo
def scrape_all():
    # set up splinter
    executable_path = {'executable_path': chromedriver_autoinstaller.install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)

    # put all scraping results into a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# ----------------------------------------
# # Mars Planet Science: Article scraping
# ----------------------------------------
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # add try/except for error handling if html format changes over time
    try:
        # slide_elem will be our parent element that holds all the other elements with it
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributError:
        return None, None
    
    return news_title, news_p

# ----------------------------------------
# # Jet Propulsion Laboratory: image scraping
# ----------------------------------------
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button for the second 'button'
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # find the image url for the most recent image
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    # base url + partial url from above
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


# ----------------------------------------
# # Galaxy Facts: fact scraping
# ----------------------------------------
def mars_facts():
    try:
        # convert table from galaxy facts website to pd dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # convert the dataframe back into html so that we can use it in our app
    return df.to_html()

# run flask app as a script on local device
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())



