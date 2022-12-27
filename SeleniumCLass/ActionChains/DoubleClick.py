#double click actions
from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import  Keys
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("http://testautomationpractice.blogspot.com/")
driver.maximize_window()
ele=driver.find_element(By.XPATH,"//button[contains(text(),'Copy Text')]")
act=ActionChains(driver)
act.double_click(ele).perform()
