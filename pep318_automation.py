# 06/04/2020
# Andrei Nechifor
# python.org > Search for pep 318 > assert search page > open first link > assert first link page

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common import action_chains,keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from urllib3 import poolmanager,exceptions
def logging(event,content):

    import time

    logger=open('logger.txt','a+')
    time_to_write=time.strftime(("%d-%m-%Y %H:%M:%S"))
    logger.writelines("{0} @ {1}{2}".format(event,time_to_write,"\n"))
    logger.writelines("\t"*3)
    logger.writelines(content)
    logger.write("{0}{1}{2}".format("\n","-"*50,"\n"))
    logger.close()

def check_presence_by_xpath(xpath,element_name,browser):

    try:
        x=WebDriverWait(browser,5).until(EC.presence_of_element_located((By.XPATH,xpath)))
        logging('Looking for %s on %s page.' %(element_name,browser.current_url),'Continuing the script')

    except TimeoutException as e:
        logging("Waiting time for {} excedeed".format(element_name),"Browser closed")  
        browser.quit()
    except Exception:
        logging('Unkown error',"")
        browser.quit()
    else:
        return x   

def open_first_link(url,without_window=False):
    
    cpx=check_presence_by_xpath # shortcut
    # Browser options
    opt = Options()
    opt.headless = without_window
    browser = webdriver.Chrome('chromedriver', options=opt)

    # Requesting page
    try:
        browser.get(url)
        r=poolmanager.PoolManager()
        r.request('GET',url)

    except exceptions.MaxRetryError as e:
        logging('Connection ERROR:\n%s'%(str(e)),'Connection could not be esteablished')
        browser.quit()
        return 0
    logging("URL CHANGED",browser.current_url)

    # Assert landing on main page
    logo = cpx('//*[@id="touchnav-wrapper"]/header/div/h1/a/img','python logo',browser)

    try:
        # Looking for search box and fill with querry term
        search_box = cpx('//*[@id="id-search-field"]','search-box',browser)
        search_box.send_keys('Decorator')
        
        # Searching for GO button and click it
        submit_button=cpx('//*[@id="submit"]','GO Button',browser)   
        submit_button.click()
        logging("URL CHANGED",browser.current_url)
        
        # Asure you landed on the query search page
        check = browser.find_element_by_tag_name("h2")
        assert check.text == "Search Python.org"


        # Navigating to first search resulted link
        first_link = browser.find_element_by_xpath('//*[@id="content"]/div/section/form/ul/li[1]/h3/a')
        first_link.click()
        logging("URL CHANGED",browser.current_url)

        # Assure you landed on the first link page by matching the expected title with actual page title
        header = browser.find_element_by_class_name("page-title")
        assert(header.text == 'PEP 318 -- Decorators for Functions and Methods')
        logging("URL CHANGED",browser.current_url)
        logging("Search Results","Found <<{0}>>".format(header.text))
        if(without_window==False):
            print("Browser will close in 5 seconds")
            time.sleep(5)
    except AttributeError as Error:
        logging('One of the requested elements does not belong to this page.','Code error %s' % Error)
        browser.quit()
        logging('Browser quit.',"")
        return 0
    finally:
        # Close the browser
        browser.quit()
        return 1
#open_first_link('C:\\Users\\AMnechifor\\Desktop\\py\\Welcome to Python.org.html')
# Testing
test_pages=['http://scratchpd.com','http://google.ro','http://python.org','http://www.bitacad.net']
succes_counter=0
for e in test_pages:
    succes_counter=open_first_link(e,without_window=True)
succes_rate=float(succes_counter)/len(test_pages)*100
logging('Test finished','Succes rate : {0}%'.format(succes_counter))
print('Test finished')
