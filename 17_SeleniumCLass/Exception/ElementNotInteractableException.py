#ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
# create webdriver object
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.google.com/")
driver.maximize_window()
driver.find_element_by_xpath("//*[contains(text(),'Google apps')]").click()