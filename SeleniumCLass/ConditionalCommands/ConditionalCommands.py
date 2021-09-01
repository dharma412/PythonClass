from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.facebook.com/")
ele=driver.find_element_by_xpath("//input[@type='text']")
print(ele.is_displayed())
