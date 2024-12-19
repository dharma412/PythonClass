#double click actions
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import  Keys
from webdriver_manager.chrome import ChromeDriverManager
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
driver.get("https://swisnl.github.io/jQuery-contextMenu/demo.html")
driver.maximize_window()
act=ActionChains(driver)
time.sleep(15)
act.context_click(driver.find_element(By.XPATH,"//span[contains(text(),'right click me')]")).perform()