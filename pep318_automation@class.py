# 06/04/2020
# Andrei Nechifor
# python.org > Search for pep 318 > assert search page > open first link > assert first link page
# Class edit

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common import action_chains,keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from urllib3 import poolmanager,exceptions

class AccesPep318():
    
    def __init__(self,url,without_window=False):
        self.url=url
        self.without_window=without_window
        self.host_name=url[url.find("//")+2:]
        self.opts=Options()
        self.opts.headless=self.without_window
        self.browser=webdriver.Chrome('chromedriver',options=self.opts)
        self.succes=0
        self.webdriver=None

    @staticmethod
    def logging(event,content):
        logger = open('logger.txt','a+')
        time_to_write  = time.strftime(("%d-%m-%Y %H:%M:%S"))
        logger.writelines("{0} @ {1}{2}".format(event,time_to_write,"\n"))
        logger.writelines("\t"*3)
        logger.writelines(content)
        logger.write("{0}{1}{2}".format("\n","-"*50,"\n"))
        logger.close()
        
    def cpx(self,xpath,element_name):
        try:
            self.webdriver=WebDriverWait(self.browser,5).until(EC.presence_of_element_located((By.XPATH,xpath)))
            AccesPep318.logging('Looking for %s on %s page.' %(element_name,self.browser.current_url),'Continuing the script')

        except TimeoutException as e:
            AccesPep318.logging("Waiting time for {} excedeed".format(element_name),"self.browser closed with error : %s" %(e)) 
            self.browser.quit()
        except Exception:
            AccesPep318.logging('Unkown error',"")
            self.browser.quit()
        else:
            return self.webdriver   

    def open_first_link(self):
        
        self.logging('Test started for host :',self.host_name)

        # Requesting page
        try:
            self.browser.get(self.url)
            r = poolmanager.PoolManager()
            r.request('GET',self.url)

        except exceptions.MaxRetryError as e:
            AccesPep318.logging('Connection ERROR:\n%s'%(str(e)),'Connection could not be esteablished')
            self.browser.quit()
            self.succes=0
            return 0
        AccesPep318.logging("URL CHANGED",self.browser.current_url)

        # Assert landing on main page
        self.cpx('//*[@id="homepage"]','Python logo on main page')
        search_box=self.cpx('//*[@id="id-search-field"]','Search form on python.org landing page')
        go_button=self.cpx('//*[@id="submit"]','GO Button')
        # Treat AttributeErrors on main page
        try:
            actions = [search_box,go_button]
            for action in actions:
                i=actions.index(action)
                if(action.tag_name == 'input'):
                    action.send_keys('Decorator')
                else:
                    action.click()
                


        except AttributeError as e:
            AccesPep318.logging('Error: %s'%(e.args),'Element %s does not have required attribute'%(str(actions[i])))
            self.browser.quit()
            AccesPep318.logging('Browser quit','Error:%s'%(e))
            self.succes=0
            return 0
        # Treat AttributeErrors on search page
        try:
            search_page_header = self.cpx('//*[@id="content"]/div/section/h2','Search page header')
            assert search_page_header.text
            first_link = self.cpx('//*[@id="content"]/div/section/form/ul/li[1]/h3/a','Required link')
            first_link.click()
            AccesPep318.logging("URL CHANGED",self.browser.current_url)
            first_link_header = self.cpx('//*[@id="content"]/div/section/article/header/h1','Header of first link')
            assert(first_link_header.text == 'PEP 318 -- Decorators for Functions and Methods')
        except exceptions.MaxRetryError:
            AccesPep318.logging('Error','Host refused comunication request')
            self.browser.quit
            self.succes=0
            return 0        
        else:
            # Close the browser
            if(self.without_window == False):
                print("Browser will close in 5 seconds")
                time.sleep(5)
            self.browser.quit()
            self.succes=1
            return 1

# Testing
test_pages = ['http://scratchpd.com','http://google.ro','http://python.org','http://www.bitacad.net']
succes_counter = 0
for e in test_pages:
    e=AccesPep318(e,without_window=True)
    e.open_first_link()
    succes_counter+=e.succes
succes_rate = (succes_counter/len(test_pages))*100
AccesPep318.logging('Test finished','Succes rate : {0}%'.format(succes_rate))
print('Test finished')
