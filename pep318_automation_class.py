  
# 13/04/2020
# Andrei Nechifor
# Test pages testing improoved

import os
import sys
import time
from selenium import webdriver
from multiprocessing import Pool
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3 import poolmanager,exceptions,PoolManager,HTTPConnectionPool,HTTPSConnectionPool

sys.path.append(os.curdir)

class AccesPep318():
    """This class is designed to acces "PEP 318 -- Decorators for Functions and Methods" article from Python.org. 
        It tests to find out specific elements of pages that are required to be navigated until the final destination
        METHODS :
            INIT(self,withoud_window)
            LOGGING(event,content)
            CPX(xpath,element_name)
            REQUEST_URL(url)
            FIRST_PAGE()
            OPEN_SEARCH_PAGE()
        ATTRIBUTES :
            -hostname
            -url
            -browser
            -webdriver
            -searh_box
            -go_button
            -search_page_header
                        ...
        """

    def __init__(self,without_window=False):
        self.without_window=without_window
        self.opts=Options()
        self.opts.headless=self.without_window
        self.browser=webdriver.Chrome('chromedriver',options=self.opts)
        self.webdriver=None
        self.r=poolmanager.PoolManager()
        self.check_sum=0
        
    @staticmethod
    def logging(event,content):
        """Writing events into the file after formating as Event-Content@Time"""


        logger = open('logger.txt','a+')
        time_to_write  = time.strftime(("%d-%m-%Y %H:%M:%S"))
        logger.writelines("{0} @ {1}{2}".format(event,time_to_write,"\n"))
        logger.writelines("\t"*3)
        logger.writelines(content)
        logger.write("{0}{1}{2}".format("\n","-"*50,"\n"))
        logger.close()
        
    def cpx(self,xpath,element_name):
        """CPX stands for Check Presence By Xpath. 
            This method requires two parameters, as strings, trying to find the x-path located element."""

            
        try:
            self.webdriver=WebDriverWait(self.browser,5).until(EC.presence_of_element_located((By.XPATH,xpath)))
            self.logging('Looking for %s on %s page.' %(element_name,self.browser.current_url),'Continuing the script')
        except TimeoutException as e:
            self.logging("Waiting time for {} excedeed".format(element_name),"self.browser closed with error : %s" %(e)) 
            self.browser.quit()
            return False
        except Exception:
            self.logging('Unkown error',"")
            self.browser.quit()
            return False
        else:
            return self.webdriver   

    # Request the url
    def request_url(self,url):


        """ This method request the url, and treats the errors that are suposed to appear"""
        self.host_name=url[url.find("//")+2:]
        self.logging('Test started for host :',self.host_name)
        try:    
                self.r.request('GET',url)
                self.browser.get(url)
                self.logging("Requesting url ",url)
                self.logging("URL CHANGED",self.browser.current_url)

        except exceptions.MaxRetryError as e:
                self.logging('Connection ERROR:\n%s'%(str(e)),'Connection could not be esteablished')
                self.browser.quit()
                self.logging("Browser exited with error","")
                self.succes=0
                return False
        self.logging("Finished request for",url)
        return True # No error occured.
    
    # First page method
    def first_page(self):
        """ This method request first page objects, namely Python.org home-page and submit their specific actions"""


        self.cpx('//*[@id="homepage"]','Python logo on main page')
        search_box = self.cpx('//*[@id="id-search-field"]','Search form on python.org landing page')
        go_button = self.cpx('//*[@id="submit"]','GO Button')
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
            self.logging('Error: %s'%(e.args),'Element %s does not have required attribute'%(str(actions[i])))
            self.browser.quit()
            self.logging('Browser quit','Error:%s'%(e))
            self.succes=0
            return False
        self.succes=1
        return True
    # Search page method 
    def open_search_result(self):
        """ This method request search objects, namely Search Python.org page and submit their specific actions"""

         
        try:
            search_page_header = self.cpx('//*[@id="content"]/div/section/h2','Search page header')
            assert search_page_header.text =="Search Python.org"
            first_link = self.cpx('//*[@id="content"]/div/section/form/ul/li[1]/h3/a','Required link')
            first_link.click()
            self.logging("URL CHANGED",self.browser.current_url)
            first_link_header = self.cpx('//*[@id="content"]/div/section/article/header/h1','Header of first link')
            assert(first_link_header.text == 'PEP 318 -- Decorators for Functions and Methods')
        except exceptions.MaxRetryError:
            self.logging('Error','Host refused comunication request')
            self.browser.quit()
            self.succes = 0
            return False
        except AttributeError as e:
            self.logging('Element does not have the required element',str(e))
            self.logging('Browser exited with error',"")
            self.browser.quit()
            self.succes = 0 
            return False

        else:
            # Close the browser
            if(self.without_window == False):
                print("Browser will close in 5 seconds")
                time.sleep(5)
            self.browser.quit()
            self.logging('Succesfuly finished the test','Browser closed with no error code !')
        return True
    
    # Reseting browser and webdriver@search
    def update_navigators(self):
        """This method reset the navigator for the next testing page, and also increment the check_sum 
        which is used in mesuring the succes rate for each individual test"""
        self.browser=webdriver.Chrome('chromedriver',options=self.opts)
        self.webdriver=None       
        self.check_sum=0

    # Testing method is calling all the methods defined previously
    def test_method(self,url):
        """This is the method that calls all the previously declared methods"""
        self.update_navigators()
        if not(self.request_url(url)):
            return 0                
        if not(self.first_page()):    
            return 0
        if not(self.open_search_result()):
            return 0
        else:          
            return "Test passed"




