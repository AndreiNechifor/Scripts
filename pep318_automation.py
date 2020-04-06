# 06/04/2020
# Andrei Nechifor
# python.org > Search for pep 318 > assert search page > open first link > assert first link page

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from os import curdir

def logging(event,content):

    import time

    logger=open('logger.txt','a+')
    time_to_write=time.strftime(("%d-%m-%Y %H:%M:%S"))
    logger.writelines("{0} @ {1}{2}".format(event,time_to_write,"\n"))
    logger.writelines("\t"*3)
    logger.writelines(content)
    logger.write("\n")
    logger.close()


def open_first_link(without_window=False):
    # Browser options
    opt = Options()
    opt.headless = without_window
    browser = webdriver.Chrome('chromedriver', options=opt)

    # Requesting page
    browser.get('http://python.org')
    # Initial check.
    try: 
        main_page=WebDriverWait(browser,10).until(EC.title_is("Welcome to Python.org"))
        logging("Attempting to reach Python.org","Landed on Python.org main page")
    except Exception :
        logging("Attempting to reach Python.org","An error occured")
    else:
        search_box = browser.find_element_by_id("id-search-field")  # Search box
        
        # Filling the search box with query statement
        search_box.send_keys("Decorator")
        # Perform the search
        try:
            submit_button=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,"submit")))
            logging("Searching for submit button","Found the submit button")
            submit_button.click()
        except Exception :
            logging("Searching for submit button","An error occured")
        logging("URL CHANGED",browser.current_url)
        # Asure you landed on the query search page
        check = browser.find_element_by_tag_name("h2")
        assert check.text == "Search Python.org"


        # Navigating to first search resulted link
        first_link = browser.find_element_by_link_text(
            'PEP 318 -- Decorators for Functions and Methods')
        first_link.click()

        # Assure you landed on the first link page by matching the expected title with actual page title

        header = browser.find_element_by_class_name("page-title")
        assert(header.text == 'PEP 318 -- Decorators for Functions and Methods')
        logging("URL CHANGED",browser.current_url)
        logging("Search Results","Found <<{0}>>".format(header.text))
        print("Browser will close in 5 seconds")
        time.sleep(5)

        # Close the browser
        browser.quit()

open_first_link()

