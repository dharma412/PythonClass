from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
driver = webdriver.Firefox()
driver.get('url')

select = Select(driver.find_element_by_id('fruits01'))

# select by visible text
select.select_by_visible_text('Banana')

# select by value
select.select_by_value('1')

from selenium import webdriver
from selenium.webdriver.support.select import Select
driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe")
driver.implicitly_wait(0.5)
driver.get("https://www.tutorialspoint.com/selenium/selenium_automation_practice.htm")
# identify dropdown with Select class
sel = Select(driver.find_element_by_xpath("//select[@name='continents']"))
#select by select_by_visible_text() method
sel.select_by_visible_text("Europe")
time.sleep(0.8)
#select by select_by_index() method
sel.select_by_index(0)
driver.close()