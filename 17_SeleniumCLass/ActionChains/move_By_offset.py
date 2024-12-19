import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.keys import  Keys
from webdriver_manager.chrome import ChromeDriverManager
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))

driver.get("http://www.uitestpractice.com/")
driver.maximize_window()
# create action chain object
action = ActionChains(driver)
time.sleep(10)
# move the cursor
action.move_by_offset(200, 200).context_click().perform()



