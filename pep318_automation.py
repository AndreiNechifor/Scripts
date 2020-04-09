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
        logging("Waiting time for {} excedeed".format(element_name),"Browser closed with error : %s" %(e)) 
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
    cpx('//*[@id="homepage"]','Python logo on main page',browser)
    search_box=cpx('//*[@id="id-search-field"]','Search form on python.org landing page',browser)
    go_button=cpx('//*[@id="submit"]','GO Button',browser)
    #Treat AttributeErrors
    try:   
        elements_list=['search_box','go_button']
        # Elements that could not have the requested attributes
        i=1
        search_box.send_keys('Decorator')
        logging('Fill the search box with querry terms','Decorator')
        i=2
        go_button.click()
        logging('Perform button action','Click')


    except AttributeError as e:
        logging('Error','Element %s does not have required attribute'%(elements_list[i-1]))
        browser.quit()
        logging('Browser quit','Error:%s'%(e))
        return 0
        
    else:
        try:
            search_page_header=cpx('//*[@id="content"]/div/section/h2','Search page header',browser)
            print(search_page_header.text)
            assert search_page_header.text =='Search Python.org'
            first_link=cpx('//*[@id="content"]/div/section/form/ul/li[1]/h3/a','Required link',browser)
            first_link.click()
            logging("URL CHANGED",browser.current_url)
            first_link_header=cpx('//*[@id="content"]/div/section/article/header/h1','Header of first link',browser)
            assert(first_link_header.text == 'PEP 318 -- Decorators for Functions and Methods')
        except exceptions.MaxRetryError:
            logging('Error','Host refused comunication request')
            browser.quit
            return 0       
            
        else:
            # Close the browser
            if(without_window==False):
                print("Browser will close in 5 seconds")
            browser.quit()
            return 1

# Testing
test_pages=['http://scratchpd.com','http://google.ro','http://python.org','http://www.bitacad.net']
succes_counter=0
for e in test_pages:
    succes_counter+=open_first_link(e,without_window=True)
succes_rate=(succes_counter/len(test_pages))*100
logging('Test finished','Succes rate : {0}%'.format(succes_rate))
print('Test finished')
