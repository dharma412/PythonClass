import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import  Keys
from webdriver_manager.chrome import ChromeDriverManager
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))

# get geeksforgeeks.org
driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")

driver.maximize_window()
# get element
element = driver.find_element(By.XPATH,"//button[@id='mousehover']")

time.sleep(10)

# create action chain object
action = ActionChains(driver)

# perform the operation
action.move_to_element_with_offset(element, 25, 35).click().perform()
