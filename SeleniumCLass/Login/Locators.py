from selenium import webdriver
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
driver=webdriver.Chrome()
driver.get("http://www.google.com")
driver.maximize_window()
driver.find_element_by_name(name='q').send_keys("naveen automation")

optionsList = driver.find_elements(By.XPATH, '//span[contains(text(),"naveen automation")]//child::b')

print(len(optionsList))

for ele in optionsList:
    print(ele.text)





driver.get("https://www.youtube.com/")
driver.maximize_window()

driver.find_element(By.XPATH,"//input[@id='search']").send_keys("Python videos")

driver.find_element_by_xpath("//input[@id='search']").send_keys("Python videos")

driver.find_element_by_xpath("//button[@id='search-icon-legacy']").click()

from selenium import webdriver
from selenium.webdriver.common.by import By
import time




