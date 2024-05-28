from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
# create webdriver object
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.pavantestingtools.com/#")
driver.maximize_window()
driver.find_element_by_name("oauth2relay718575679")
driver.refresh()
driver.find_element_by_name("oauth2relay718575679")