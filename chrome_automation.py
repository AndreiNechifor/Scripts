#04/03/2020
#Andrei
#Get all releases from python.org -  FINISHED

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
opt=Options()
opt.headless=True
browser=webdriver.Chrome('chromedriver',options=opt)
browser.get('https://www.python.org')
element=browser.find_element_by_id("downloads")
element.click()d
x=browser.find_elements_by_css_selector("ol li")
print("Your query results :")
releases=[x.text for x in browser.find_elements_by_css_selector("ol li")]
for item in x:
    print("{0}{1}".format("\t"*2,item.text))
print("Latest release is :",releases[0])
browser.quit()