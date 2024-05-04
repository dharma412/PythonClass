from selenium import webdriver
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
import time

driver=webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.amazon.in/")

driver.maximize_window()

driver.find_element(By.XPATH,"//span[contains(text(),'Account & Lists')]").click()

driver.implicitly_wait(5)

driver.find_element(By.XPATH,"//input[@name='email']").send_keys("8008461613")
driver.implicitly_wait(3)
driver.find_element(By.XPATH,"input[@name='password']").send_keys("Ericsson@412")

time.sleep(20)



