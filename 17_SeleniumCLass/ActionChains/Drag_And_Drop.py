from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import  Keys
from webdriver_manager.chrome import ChromeDriverManager
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))

driver.get("http://www.dhtmlgoodies.com/scripts/drag-drop-custom/demo-drag-drop-3.html")
driver.maximize_window()

sourceelemt=driver.find_element(By.XPATH,"//*[contains(text(),'Rome')][2]")
target=driver.find_element(By.XPATH,"//*[contains(text(),'Italy')][1]")

act=ActionChains(driver)
act.drag_and_drop(sourceelemt,target).perform()