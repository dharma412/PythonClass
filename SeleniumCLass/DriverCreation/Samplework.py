import time
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("user-data-dir=C:\Users\Lenovo\AppData\Local\Google\Chrome\User Data")
driver=webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
from selenium.webdriver.chrome.options import Options
mywait=WebDriverWait(driver,10,ignored_exceptions=Exception)



driver.implicitly_wait(10)
driver.get("https://login.salesforce.com/?eco=1&ec=20037")
driver.maximize_window()
driver.find_element(By.XPATH,"//input[@id='username']").send_keys("tejach412-cnc8@force.com")
driver.find_element(By.XPATH,"//input[@id='password']").send_keys("Ericsson@412")
driver.find_element(By.XPATH,"//input[@id='Login']").click()
time.sleep(15)
ele=driver.find_element(By.XPATH,"//span[@class='slds-truncate'][normalize-space()='Leads']")
driver.execute_script("arguments[0].click();", ele )