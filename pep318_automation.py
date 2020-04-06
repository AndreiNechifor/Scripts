# 06/04/2020
# Andrei Nechifor
# python.org > Search for pep 318 > assert search page > open first link > assert first link page

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def open_first_link(without_window=False):

    # Browser options
    opt = Options()
    opt.headless = without_window
    browser = webdriver.Chrome('chromedriver', options=opt)

    # Requesting page
    #browser.get('https://www.google.ro')
    print("Looking for Python.org")
    browser.get('http://python.org')
    try: # initial check.
        main_page=WebDriverWait(browser,10).until(EC.title_is("Welcome to Python.org"))
        print("Landed on Python main page")
    except Exception :
        print("Some error occured")
    else:
        search_box = browser.find_element_by_id("id-search-field")  # Search box
        
        # Filling the search box with query statement
        search_box.send_keys("Decorator")
        # Sending a letter every half second
        page=browser.current_url # get the initial page url and match it at line 41
        print(page) 
        # Perform the search
        try:
            submit_button=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,"submit")))
            print("Found the submit button")
            submit_button.click()
        except Exception :
            print("Some error occured")

        # Asure you landed on the query search page
        check = browser.find_element_by_tag_name("h2")
        assert check.text == "Search Python.org"


        # Navigating to first search resulted link
        first_link = browser.find_element_by_link_text(
            'PEP 318 -- Decorators for Functions and Methods')
        if(page!=browser.current_url):
            print("URL CHANGED TO ",browser.current_url)
        first_link.click()

        # Asure you landed on the first link page by matching the expected title with actual page title

        header = browser.find_element_by_class_name("page-title")
        assert(header.text == 'PEP 318 -- Decorators for Functions and Methods')
        print("We are in the right page")
        print("Browser will close in 5 seconds")
        time.sleep(5)

        # Close the browser
        browser.quit()

open_first_link()

