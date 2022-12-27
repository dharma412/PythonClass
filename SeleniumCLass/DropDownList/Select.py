from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from webdriver_manager.chrome import  ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.select import Select
driver = webdriver.Chrome(ChromeDriverManager().install())
#driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe")
driver.implicitly_wait(0.5)
driver.get("https://www.tutorialspoint.com/selenium/selenium_automation_practice.htm")
# identify dropdown with Select class

driver.maximize_window()
element=driver.find_element(By.XPATH,"//select[@name='continents']")

sel=Select(element)
sel.select_by_index(5)
#sel.select_by_visible_text("Asia")
sel.deselect_by_index(5)
sel.select_by_value("option1")
#sel.select_by_visible_text("Europe")
time.sleep(0.8)
#select by select_by_index() method

sel.deselect_all()
#driver.close()