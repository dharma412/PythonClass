#NoSuchAttributeException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
# create webdriver object
driver = webdriver.Chrome(ChromeDriverManager().install())
# get ide.geeksforgeeks.org
driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()
#driver.switch_to_alert()
ele=driver.find_element_by_xpath("//input[@name='checkBoxOption1']")
(ele.get_attribute('class'))
driver.close()