# 06/04/2020
# Andrei
# Get all releases from python.org -  FINISHED

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Browser options
opt = Options()
opt.headless = False
browser = webdriver.Chrome("chromedriver", options=opt)

# Requesting page
browser.get("https://www.python.org")
element = browser.find_element_by_id("downloads")
element.click()

# Finding the releases container
x = browser.find_elements_by_css_selector("ol li")

# Return the releases as shown in container
releases = [x.text for x in browser.find_elements_by_css_selector("ol li")]
print("Your query results :")
for item in x:
    print("{0}{1}".format("\t" * 2, item.text))
print("Latest release is :", releases[0])

# Close the browser
browser.quit()
