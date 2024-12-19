from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
opts = Options()
opts.add_experimental_option("detach", True)


driver=webdriver.Chrome(service=Service(ChromeDriverManager(url='https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/win64/chromedriver-win64.zip').install()),options=opts)

driver.get("https://www.rahulshettyacademy.com/AutomationPractice/")

driver.maximize_window()
time.sleep(5)
parent_handle=driver.current_window_handle
driver.find_element(By.XPATH,"//a[text()='Open Tab']").click()
time.sleep(5)

handles=driver.window_handles

for i in range(len(handles)):
    if handles[i] != parent_handle:
        driver.switch_to.window(handles[i])
        if driver.title=="QAClick Academy - A Testing Academy to Learn, Earn and Shine":
            print("I am window")
            driver.find_element(By.XPATH, "//a[text()='Courses']").click()
        break

driver.switch_to.window(handles[0])
time.sleep(4)
print(driver.title)
time.sleep(5)
driver.quit()

