from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.keys import  Keys
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("http://www.dhtmlgoodies.com/scripts/drag-drop-custom/demo-drag-drop-3.html")
driver.maximize_window()

sourceelemt=driver.find_element_by_xpath("//*[contains(text(),'Rome')][2]")
target=driver.find_element_by_xpath("//*[contains(text(),'Italy')][1]")

act=ActionChains(driver)

act.drag_and_drop(sourceelemt,target).perform()