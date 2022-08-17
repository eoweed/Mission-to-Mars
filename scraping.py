# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
# from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
import pandas as pd    # to use for mars facts scraping

# set up splinter
executable_path = {'executable_path': chromedriver_autoinstaller.install()}
browser = Browser('chrome', **executable_path, headless=False)


# ----------------------------------------
# # Mars Planet Science: Article scraping
# ----------------------------------------
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')

# slide_elem will be our parent element that holds all the other elements with it
slide_elem = news_soup.select_one('div.list_text')

# get the article title from slide_elem
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ----------------------------------------
# # Jet Propulsion Laboratory: image scraping
# ----------------------------------------
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button for the second 'button'
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the image url for the most recent image
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel    # shows the partial url

# Use the base URL to create an absolute URL
# base url + partial url from above
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ----------------------------------------
# # Galaxy Facts: fact scraping
# ----------------------------------------
# convert table from galaxy facts website to pd dataframe
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# convert the dataframe back into html so that we can use it in our app
df.to_html()

browser.quit()



