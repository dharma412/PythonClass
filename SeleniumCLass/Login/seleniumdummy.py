# applictaion web , desktop, mobile, standalone,billing applictaion.

# selenium "web"
# selenium its packag eselenium IDE, Grid, Seleneium Webdriver,

# webdrivers java python C# perl

# selenium webdriver+python
# briwser dirver

from selenium import webdriver
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
driver=webdriver.Chrome()
driver.get("https://www.youtube.com/")
driver.maximize_window()

driver.find_element(By.XPATH,"//input[@id='search']").send_keys("Python videos")

driver.find_element_by_xpath("//input[@id='search']").send_keys("Python videos")

driver.find_element_by_xpath("//button[@id='search-icon-legacy']").click()


#locators in selenium
#ID, name, Link text, css selector, xpath
#driver.close()

#driver.close()