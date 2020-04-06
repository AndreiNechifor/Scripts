# 06/04/2020
# Andrei Nechifor
# python.org > Search for pep 318 > assert search page > open first link > assert first link page

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def open_first_link(without_window=False):

    # Browser options
    opt = Options()
    opt.headless = without_window
    browser = webdriver.Chrome('chromedriver', options=opt)

    # Requesting page
    browser.get('https://www.python.org')
    search_box = browser.find_element_by_id("id-search-field")  # Search box
    
    # Filling the search box with query statement
    # Sending a letter every half second
    page=browser.current_url # get the initial page url and match it at line 41
    print(page)
    for e in "Decorator":
        time.sleep(0.5)
        search_box.send_keys(e)
    # Perform the search
    submit_button = browser.find_element_by_id("submit")
        #Check if the search_box was filled up with "keys".
    if(search_box.get_attribute!=""):
        time.sleep(10)
    submit_button.click()
    # Asure you landed on the query search page

    check = browser.find_element_by_tag_name("h2")
    assert check.text == "Search Python.org"
    time.sleep(2)

    # Navigating to first search resulted link
    first_link = browser.find_element_by_link_text(
        'PEP 318 -- Decorators for Functions and Methods')
    if(page!=browser.current_url):
        time.sleep(5)
        print("URL CHANGED TO ",browser.current_url)
    first_link.click()

    # Asure you landed on the first link page by matching the expected title with actual page title

    header = browser.find_element_by_class_name("page-title")
    print(header.text)
    assert(header.text == 'PEP 318 -- Decorators for Functions and Methods')
    print("We are in the right page")
    print("Browser will close in 5 seconds")
    time.sleep(5)

    # Close the browser
    browser.quit()

open_first_link()

