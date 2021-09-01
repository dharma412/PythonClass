import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.keys import  Keys
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

# get geeksforgeeks.org
driver.get("https://www.geeksforgeeks.org/")
driver.maximize_window()
# create action chain object
action = ActionChains(driver)

# move the cursor
action.move_by_offset(1400, 1200)

# perform the operation
action.perform()


driver.get("http://testautomationpractice.blogspot.com/")
driver.maximize_window()
#ele=driver.find_element_by_xpath("//button[contains(text(),'Copy Text')]")

act=ActionChains(driver)
time.sleep(10)
act.move_by_offset(200,200).perform()

#act.move_by_offset(200,400).perform()


# import webdriver
from selenium import webdriver

# import Action chains
from selenium.webdriver.common.action_chains import ActionChains

# create webdriver object


