from selenium import webdriver
from selenium.webdriver.common.by import By

driver=webdriver.Chrome(executable_path='chromedriver.exe')

driver.get("https://www.facebook.com/login/")

driver.find_element(By.NAME,"email").send_keys("chdharma412@gmail.com")

driver.find_element(By.ID,"pass").send_keys("8008461613")

driver.find_element(By.XPATH,"//a[starts-with(text(),'Forgotten')]").send_keys("993939u")

driver.find_element(By.LINK_TEXT,"Forgotten account?")

driver.find_element(By.PARTIAL_LINK_TEXT,"Forgotten").click()