import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.implicitly_wait(10)
driver.get("https://www.tutorialspoint.com/selenium/selenium_automation_practice.htm")
driver.maximize_window()
droplist=driver.find_element(By.NAME,"selenium_commands")
sel=Select(droplist)
sel.select_by_visible_text("WebElement Commands")
ele=driver.find_element(By.XPATH,"//button[normalize-space()='Button']")
driver.execute_script("arguments[0].click();", ele )
myalert=driver.switch_to.alert
myalert.accept()
print("sucussfull")
driver.quit()