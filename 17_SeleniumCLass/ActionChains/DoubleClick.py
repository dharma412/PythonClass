#double click actions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import  Keys
from webdriver_manager.chrome import ChromeDriverManager
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
driver.get("http://testautomationpractice.blogspot.com/")
driver.maximize_window()
ele=driver.find_element(By.XPATH,"//button[contains(text(),'Copy Text')]")
act=ActionChains(driver)
act.double_click(ele).perform()
