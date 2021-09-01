from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

driver=webdriver.Chrome(ChromeDriverManager().install())

driver.get("http://demo.guru99.com/test/login.html#")
driver.maximize_window()
driver.find_element_by_xpath("//a[contains(text(),'Agile Project')]").click()
driver.refresh()