# Create a function that scrapes from an html pages, based on the input html url and the xpath of the element to be scraped.
# The function should return a list of the scraped elements.
# The function should also handle the case where the element is not found on the page.
from urllib.request import urlopen, Request

import BeautifulSoup4 as BeautifulSoup4


def get_elements_from_html_page(html_url, xpath):
    # Create a list to store the elements
    elements = []
    # Create a Request object
    req = Request(html_url)
    # Get the html page
    html_page = urlopen(req).read()
    # Create a BeautifulSoup object
    soup = BeautifulSoup4(html_page, 'html.parser')
    # Get the elements from the page
    elements = soup.find_all(xpath)
    # Return the list of elements
    return elements
