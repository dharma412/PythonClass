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
print(driver.current_window_handle)
driver.find_element(By.XPATH,"//button[text()='Open Window']").click()
time.sleep(5)

# driver.switch_to.new_window("window")
#
# driver.find_element(By.XPATH,"//a[text()='Courses']").click()
#
# time.sleep(5)

#allwindows=driver.window_handles
# print(len(allwindows))
# print(type(allwindows))
#
# driver.switch_to.window(allwindows[1])
#
# driver.find_element(By.XPATH,"//a[text()='Courses']").click()
#
# time.sleep(5)

