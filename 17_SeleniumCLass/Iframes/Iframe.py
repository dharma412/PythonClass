from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
opts = Options()
opts.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opts)

driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()

time.sleep(5)
driver.switch_to.frame("courses-iframe")


value=driver.find_element(By.XPATH,"//li[text()=' contact@rahulshettyacademy.com']").text

print(value)

#driver.find_element(By.XPATH,"//a[@href='/consulting']").click()
driver.switch_to.default_content()
print(driver.find_element(By.XPATH,"//h1[text()='Practice Page']").text)
time.sleep(5)
driver.close()

