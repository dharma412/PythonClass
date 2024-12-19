#NoSuchAttributeException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
# create webdriver object
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))
# get ide.geeksforgeeks.org
driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()
#driver.switch_to_alert()
ele=driver.find_element_by_xpath("//input[@name='checkBoxOption1']")
(ele.get_attribute('class'))
driver.close()