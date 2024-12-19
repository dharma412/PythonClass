from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
# create webdriver object
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
driver.get("https://www.pavantestingtools.com/#")
driver.maximize_window()
driver.find_element_by_name("oauth2relay718575679")
driver.refresh()
driver.find_element_by_name("oauth2relay718575679")