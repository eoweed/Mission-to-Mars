# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
# from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller


# Set the executable path and initialize Splinter
# executable_path = {'executable_path': ChromeDriverManager().install()}
executable_path = {'executable_path': chromedriver_autoinstaller.install()}
browser = Browser('chrome', **executable_path, headless=False)


# ----------------------------------------------------------------
# Visit the NASA Mars News Site
# ----------------------------------------------------------------

def mars_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=10)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
        
    return news_title, news_p


# ----------------------------------------------------------------
# JPL Space Images Featured Image
# ----------------------------------------------------------------

def featured_image():
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ----------------------------------------------------------------
# Mars Facts
# ----------------------------------------------------------------

def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html()

# ----------------------------------------------------------------
# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ----------------------------------------------------------------

def mars_hemispheres():
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        hemisphere_container = img_soup.find_all('div', class_="description")

        for x in hemisphere_container:
            title = x.find('h3').text

            # click link to image
            browser.find_by_text(title).click()
            
            # parse html of new webpage
            html = browser.html
            img_soup = soup(html, 'html.parser')
            
            # get links to Full JPG image
            jpg = img_soup.find('li')
            partial_jpg_link = jpg.find('a').get('href')
            full_jpg_link = f'https://marshemispheres.com/{partial_jpg_link}'
            
            # add title and link to dictionary
            hemisphere_image_urls.append({'img_url': full_jpg_link,
                                        'title': title})
            
            # click back to home page
            browser.back()

    except:
        return None


    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls




