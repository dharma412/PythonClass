from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
driver.get("https://www.amazon.in/")
driver.maximize_window()
print(driver.title)
time.sleep(5)

driver.get("https://www.pavantestingtools.com/")
print(driver.title)
time.sleep(5)

driver.back()  #will navigate to amzon
print(driver.title)
time.sleep(10)

driver.forward()  # will navigate to pavantestingtools again.
print(driver.title)