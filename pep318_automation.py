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
from selenium.common.exceptions import NoSuchElementException,TimeoutException

def logging(event,content):

    import time

    logger=open('logger.txt','a+')
    time_to_write=time.strftime(("%d-%m-%Y %H:%M:%S"))
    logger.writelines("{0} @ {1}{2}".format(event,time_to_write,"\n"))
    logger.writelines("\t"*3)
    logger.writelines(content)
    logger.write("\n")
    logger.close()

def check_presence_by_xpath(xpath,browser):
    try:
        x=WebDriverWait(browser,3).until(EC.presence_of_element_located((By.XPATH,xpath)))
        
    except TimeoutException:
        logging("Erorr 01.","Waiting time exceeded")
        browser.quit()
    else:
        return x

cpx=check_presence_by_xpath # shortcut


def open_first_link(url,without_window=False):

    # Browser options
    opt = Options()
    opt.headless = without_window
    browser = webdriver.Chrome('chromedriver', options=opt)

    # Requesting page
    browser.get(url)

    # Initial check.
    logo = check_presence_by_xpath('//*[@id="touchnav-wrapper"]/header/div/h1/a/img',browser)
    
    search_box = cpx('//*[@id="id-search-field"]',browser)
        
    # Filling the search box with query statement
    search_box.send_keys("Decorator")
    
    # Perform the search
    submit_button=cpx('//*[@id="submit"]',browser)
    submit_button.click()
    logging("URL CHANGED",browser.current_url)
    
    # Asure you landed on the query search page
    check = browser.find_element_by_tag_name("h2")
    assert check.text == "Search Python.org"


    # Navigating to first search resulted link
    first_link = browser.find_element_by_xpath('//*[@id="content"]/div/section/form/ul/li[1]/h3/a')
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

open_first_link('http://python.org')

