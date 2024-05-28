#1. driver.get() vs driver.navigateTo()
#return type of get is void
#return type of navogaion is naigate interface it has history

import os
from selenium import webdriver
from selenium.webdriver.common.alert import Alert

# create webdriver object
driver = webdriver.Chrome(executable_path="../Drivers/chromedriver.exe")
s=driver.get("https://www.geeksforgeeks.org/selenium-python-tutorial/")
e=driver.find_element_by_xpath()

print(s)
driver.get_screenshot_as_png()
driver.switch_to
