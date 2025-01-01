
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import  Keys

#create Driver objcet
driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()))


driver.get("https://www.facebook.com/login/")

driver.find_element(By.NAME,"email").send_keys("chdharma412@gmail.com")

driver.find_element(By.ID,"pass").send_keys("8008461613")

driver.find_element(By.XPATH,"//a[starts-with(text(),'Forgotten')]").send_keys("993939u")

driver.find_element(By.LINK_TEXT,"Forgotten account?")

driver.find_element(By.PARTIAL_LINK_TEXT,"Forgotten").click()